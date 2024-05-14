import pytest

from rocrate.model.person import Person

from ro_crate_uploader.authors import (
    get_orcid_id_or_none,
    get_author_details,
    get_formatted_author_name,
)
from ro_crate_uploader.upload import (
    build_zenodo_creator_list,
)

people = {
    # person with id as ORCID
    "id-orcid": {
        "identifier": "https://orcid.org/0000-0000-0000-0000",
        "properties": {
            "affiliation": "Test University",
            "name": "ORCID Person",
        },
    },
    # person with id as URI
    "id-uri": {
        "identifier": "https://example.org",
        "properties": {
            "affiliation": "Test University",
            "name": "URI Person",
        },
    },
    # person with id as local identifier
    "id-local": {
        "identifier": "#local_person",
        "properties": {
            "affiliation": "Test University",
            "name": "Local Person",
        },
    },
    # person with id as a name, and no other info
    "id-name": {"identifier": "Named Person"},
    # person with id as blank node identifier
    "id-blank-node": {
        "identifier": "_:blank_person",
    },
    # person with international characters in their name
    "name-intl-chars": {
        "identifier": "https://orcid.org/0000-0000-0000-0001",
        "properties": {
            "affiliation": "Test University",
            "name": "Ãệïøù Person",
        },
    },
    # person with given and family names
    "name-family-given": {
        "identifier": "https://orcid.org/0000-0000-0000-0002",
        "properties": {
            "affiliation": "Test University",
            "givenName": "Given",
            "familyName": "Family",
        },
    },
    # person with only family name
    "name-family-only": {
        "identifier": "https://orcid.org/0000-0000-0000-0003",
        "properties": {
            "affiliation": "Test University",
            "familyName": "Family",
        },
    },
    # person with only given name
    "name-given-only": {
        "identifier": "https://orcid.org/0000-0000-0000-0004",
        "properties": {
            "affiliation": "Test University",
            "givenName": "Given",
        },
    },
}

formatted_names = {
    "id-orcid": "ORCID Person,",
    "name-family-given": "Family, Given",
    "name-family-only": "Family, ",
    "name-given-only": ", Given",
}


@pytest.mark.parametrize(
    "person_dict",
    list(people.values()),
)
def test_get_author_details(person_dict):
    person = Person(None, **person_dict)

    id = person.get("@id")
    expected = {
        "name": get_formatted_author_name(person),
        "affiliation": person.get("affiliation", None),
        "orcid": get_orcid_id_or_none(id),
    }

    # Act
    result = get_author_details(person)

    # Assert
    assert expected == result


@pytest.mark.parametrize(
    "person_dict, expected",
    [
        (people[key], formatted_names[key])
        for key in [
            "id-orcid",
            "name-family-given",
            "name-family-only",
            "name-given-only",
        ]
    ],
)
def test_get_formatted_author_name(person_dict, expected):
    person = Person(None, **person_dict)

    result = get_formatted_author_name(person)

    assert expected == result


def test_build_zenodo_creator_list__multiple_authors():
    # Arrange
    person_list = [Person(None, **p) for p in people.values()]
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
    person = Person(None, **people["id-orcid"])
    details = get_author_details(person)
    details.update({"gnd": None})
    expected = [details]

    # Act
    result = build_zenodo_creator_list(person)

    # Assert
    assert len(expected) == len(result)
    for i in range(len(expected)):
        assert expected[i] == result[i].model_dump()
