import pytest
from unittest import TestCase

from rocrate.model.person import Person

from ro_crate_uploader.authors import get_orcid_id_or_none, get_author_details
from ro_crate_uploader.upload import (
    build_zenodo_creator_list,
)

people = [
    # person with id as ORCID
    {
        "identifier": "https://orcid.org/0000-0000-0000-0000",
        "properties": {
            "affiliation": "Test University",
            "name": "ORCID Person",
        },
    },
    # person with id as URI
    {
        "identifier": "https://example.org",
        "properties": {
            "affiliation": "Test University",
            "name": "URI Person",
        },
    },
    # person with id as local identifier
    {
        "identifier": "#local_person",
        "properties": {
            "affiliation": "Test University",
            "name": "Local Person",
        },
    },
    # person with id as a name, and no other info
    {"identifier": "Named Person"},
    # person with id as blank node identifier
    {
        "identifier": "_:blank_person",
    },
    # person with international characters in their name
    {
        "identifier": "https://orcid.org/0000-0000-0000-0001",
        "properties": {
            "affiliation": "Test University",
            "name": "Ãệïøù Person",
        },
    },
]


@pytest.mark.parametrize(
    "person_dict",
    [*people],
)
def test_get_author_details(person_dict):
    person = Person(None, **person_dict)

    id = person.get("@id")
    expected = {
        "name": person.get("name", id),
        "affiliation": person.get("affiliation", None),
        "orcid": get_orcid_id_or_none(id),
    }

    # Act
    result = get_author_details(person)

    # Assert
    assert expected == result


def test_build_zenodo_creator_list__multiple_authors():
    # Arrange
    person_list = [Person(None, **p) for p in people]
    expected = []
    for person in person_list:
        details = get_author_details(person)
        details.update({"gnd": None})
        expected.append(details)

    # Act
    result = build_zenodo_creator_list(person_list)

    # Assert
    assert len(expected) == len(result)
    for i in range(len(expected)):
        assert expected[i] == result[i].model_dump()


def test_build_zenodo_creator_list__single_author():
    # Arrange
    person = Person(None, **people[0])
    details = get_author_details(person)
    details.update({"gnd": None})
    expected = [details]

    # Act
    result = build_zenodo_creator_list(person)

    # Assert
    assert len(expected) == len(result)
    for i in range(len(expected)):
        assert expected[i] == result[i].model_dump()
