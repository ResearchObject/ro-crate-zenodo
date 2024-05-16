from __future__ import annotations

import re
import logging

from rocrate.model.person import Person
from rocrate.model.contextentity import ContextEntity
from zenodo_client import Creator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ORCID_REGEX = r"https:\/\/orcid\.org\/(?P<id>([0-9]{4}-){3}[0-9]{3}[0-9X])"
ROR_REGEX = r"https:\/\/ror\.org\/(?P<id>0[a-hj-km-np-tv-z|0-9]{6}[0-9]{2})"


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
    orcid = get_orcid_id_or_none(id)

    name = get_formatted_author_name(person)

    affiliation = person.get("affiliation", None)
    if affiliation:
        affiliation = get_affiliation_name_or_id(affiliation)

    return {"name": name, "orcid": orcid, "affiliation": affiliation}


def get_formatted_author_name(person: Person) -> str:
    """Get an author's name and format it for the Zenodo API.

    Zenodo has 2 name fields: family name and given name.
    RO-Crate (via https://schema.org/Person) supports these,
    but also has a single 'name' field which is used more often.
    """
    # first try to use given and/or family names
    given_name = person.get("givenName", "")
    family_name = person.get("familyName", "")
    if given_name or family_name:
        name = f"{family_name}, {given_name}"
    else:
        # try `name` field
        # if still no name is found, fall back on id
        try:
            name = person["name"]
        except KeyError:
            id = person["@id"]
            logger.warning(f"Author {id}: No `name` field found, falling back on `@id`")
            name = id.lstrip("#")
        # append comma if needed
        # this puts the whole name into the Zenodo family name field
        if "," not in name:
            logger.warning(
                f'Could not separate family and given names for author "{name}". '
                "Verify name is correctly entered in Zenodo before publishing. "
                "To remove this warning, set `givenName` and `familyName` for this "
                "author in the RO-Crate metadata document."
            )
            name += ","

    return name


def get_affiliation_name_or_id(organization: ContextEntity | str) -> str:
    # if it's free text, return as-is
    if type(organization) == str:
        return organization

    # otherwise, we should have a ContextEntity object
    assert isinstance(organization, ContextEntity)

    # use the ROR if there is one
    id = organization["@id"]
    ror = get_ror_id_or_none(id)
    if ror:
        return ror

    # if no ROR, use the name, or the id as a last resort
    id = id.lstrip("#")
    name = organization.get("name", id)
    return name


def get_orcid_id_or_none(str: str) -> str | None:
    match = re.match(ORCID_REGEX, str)
    if match:
        return match.group("id")
    else:
        return None


def get_ror_id_or_none(str: str) -> str | None:
    match = re.match(ROR_REGEX, str)
    if match:
        return match.group("id")
    else:
        return None
