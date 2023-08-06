from dataclasses import dataclass
from typing import Dict, List, Union

import requests
from lektor.pluginsystem import Plugin
from lektor.context import get_ctx


@dataclass
class Publication:
    raw: Dict[str, str]
    title: str
    hal_id: str
    authors: List[str]
    date: str
    type: str

    @staticmethod
    def from_entry(publi_dict: Dict[str, Union[str, list[str]]]):
        return Publication(
            raw=publi_dict,
            title=publi_dict["title_s"][0],
            hal_id=publi_dict["halId_s"],
            authors=publi_dict["authFullName_s"],
            date=publi_dict["producedDate_s"],
            type=publi_dict["docType_s"],
        )

    @property
    def link(self):
        return f"https://hal.archives-ouvertes.fr/{self.hal_id}"

    @property
    def where(self):
        return self.raw.get("journalTitle_s") or self.raw.get("conferenceTitle_s")


class HalPlugin(Plugin):
    name = "hal"
    description = "Fetches publications from HAL"

    def on_setup_env(self, **extra):
        req = get_request(self.get_config()["query"])
        self.env.jinja_env.globals.update(
            hal_publications=get_publications(req),
            hal_request=req.url,
            volatile=volatile,
        )


def volatile():
    """Set the dirty flag on the artifact currently being built."""
    # credit: dairiki
    # https://github.com/lektor/lektor-website/pull/346#issuecomment-1194168763
    ctx = get_ctx()
    ctx.artifact.set_dirty_flag()
    return ""


def get_request(query):
    return requests.get(
        url="https://api.archives-ouvertes.fr/search/",
        params={
            "q": query,
            "sort": "producedDate_tdate desc",
            "fl": "title_s,label_s,docid,authFullName_s,"
            "journalTitle_s,conferenceTitle_s,publisher_s,"
            "halId_s,producedDate_s,docType_s",
        },
    )


def get_publications(req):
    return [Publication.from_entry(p) for p in req.json()["response"]["docs"]]
