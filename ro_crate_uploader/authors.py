from __future__ import annotations

import json
import re

from pydantic_core import ValidationError
from rocrate.model.person import Person
from rocrate.rocrate import ROCrate
from zenodo_client import Creator, Metadata, ensure_zenodo

ORCID_REGEX = r"https:\/\/orcid\.org\/(?P<id>([0-9]{4}-){3}[0-9]{3}[0-9X])"


def build_zenodo_creator_list(authors: list[Person] | Person) -> list[Creator]:
    """Given an RO-Crate author or list of authors, build a list of "creators"
    to use in Zenodo upload."""
    if isinstance(authors, list):
        return [Creator(name=a["name"]) for a in authors]
    else:
        # single author
        return [Creator(name=authors["name"])]


def get_author_details(person: Person) -> dict:
    """Collects details from a Person entity and returns them using Creator fields"""
    # check if @id is an ORCID
    raise NotImplementedError
    id = person["@id"]
    if id:
        pass


def get_orcid_id_or_none(str: str) -> str | None:
    match = re.match(ORCID_REGEX, str)
    if match:
        return match.group("id")
    else:
        return None
