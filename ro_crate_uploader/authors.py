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
    if not isinstance(authors, list):
        authors = [authors]
    return [Creator(**get_author_details(a)) for a in authors]


def get_author_details(person: Person) -> dict:
    """Collects details from a Person entity and returns them using Creator fields"""
    # check if @id is an ORCID
    id = person["@id"]
    orcid_id = get_orcid_id_or_none(id)

    # if no name present, fall back on id
    # TODO handle case where only a name is provided as @id but rocrate adds a #
    name = person.get("name", id)

    affiliation = person.get("affiliation", None)
    if affiliation:
        affiliation = str(affiliation)

    return {"name": name, "orcid": orcid_id, "affiliation": affiliation}


def get_orcid_id_or_none(str: str) -> str | None:
    match = re.match(ORCID_REGEX, str)
    if match:
        return match.group("id")
    else:
        return None
