import pytest
from unittest import TestCase

from rocrate.model.person import Person

from ro_crate_uploader.authors import get_orcid_id_or_none, get_author_details
from ro_crate_uploader.upload import (
    build_zenodo_creator_list,
)

person_with_id_orcid = {
    "identifier": "https://orcid.org/0000-0000-0000-0000",
    "properties": {
        "affiliation": "Test University",
        "name": "ORCID Person",
    },
}

person_with_id_uri = {
    "identifier": "https://example.org",
    "properties": {
        "affiliation": "Test University",
        "name": "URI Person",
    },
}

person_with_id_local = {
    "identifier": "#local_person",
    "properties": {
        "affiliation": "Test University",
        "name": "Local Person",
    },
}

person_with_id_name = {"identifier": "Named Person"}

person_with_id_blank = {
    "identifier": "_:blank_person",
}

person_with_intl_chars = {
    "identifier": "https://orcid.org/0000-0000-0000-0001",
    "properties": {
        "affiliation": "Test University",
        "name": "Ãệïøù Person",
    },
}


@pytest.mark.parametrize(
    "person_dict",
    [
        person_with_id_orcid,
        person_with_id_uri,
        person_with_id_local,
        person_with_id_name,
        person_with_id_blank,
        person_with_intl_chars,
    ],
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
    person_dict_list = [
        person_with_id_orcid,
        person_with_intl_chars,
        person_with_id_name,
    ]
    person_list = [Person(None, **p) for p in person_dict_list]
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
    person = Person(None, **person_with_id_orcid)
    details = get_author_details(person)
    details.update({"gnd": None})
    expected = [details]

    # Act
    result = build_zenodo_creator_list(person)

    # Assert
    assert len(expected) == len(result)
    for i in range(len(expected)):
        assert expected[i] == result[i].model_dump()
