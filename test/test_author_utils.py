import pytest

from rocrate.model.contextentity import ContextEntity
from rocrate_upload.authors import (
    get_orcid_id_or_none,
    get_ror_id_or_none,
    get_affiliation_name_or_id,
)

organizations = {
    # organization with id as ROR
    "id-ror": {
        "identifier": "https://ror.org/0abcdef12",
        "properties": {
            "name": "ROR Organization",
        },
    },
    # organization with id as URI
    "id-uri": {
        "identifier": "https://example.org",
        "properties": {
            "name": "URI Organization",
        },
    },
    # organization with id as local identifier
    "id-local": {
        "identifier": "#local_organization",
        "properties": {
            "name": "Local Organization",
        },
    },
    # organization with id as a name, and no other info
    "id-name": {"identifier": "Named Organization"},
    # organization with id as blank node identifier
    "id-blank-node": {
        "identifier": "_:blank_organization",
    },
    # organization with international characters in their name
    "name-intl-chars": {
        "identifier": "Ãệïøù Organization",
        "properties": {
            "name": "Ãệïøù Organization",
        },
    },
}


@pytest.mark.parametrize(
    "input, expected",
    [
        ("https://orcid.org/0000-0002-1825-0097", "0000-0002-1825-0097"),
        ("https://orcid.org/0000-0002-1825-009X", "0000-0002-1825-009X"),
        ("0000-0002-1825-0097", None),
        ("not an ORCID", None),
    ],
)
def test_get_orcid_id(input, expected):
    # Act
    result = get_orcid_id_or_none(input)

    # Assert
    assert expected == result


@pytest.mark.parametrize(
    "input, expected",
    [
        ("https://ror.org/02mhbdp94", "02mhbdp94"),
        ("02mhbdp94", None),
        ("not an ROR", None),
    ],
)
def test_get_ror_id(input, expected):
    # Act
    result = get_ror_id_or_none(input)

    # Assert
    assert expected == result


@pytest.mark.parametrize(
    "input, expected",
    [
        ("https://ror.org/02mhbdp94", "02mhbdp94"),
        ("02mhbdp94", None),
        ("Test University", None),
    ],
)
def test_get_ror_id(input, expected):
    # Act
    result = get_ror_id_or_none(input)

    # Assert
    assert expected == result


@pytest.mark.parametrize(
    "org_key, expected",
    [
        ("id-ror", "0abcdef12"),
        ("id-uri", "URI Organization"),
        ("id-local", "Local Organization"),
        ("id-name", "Named Organization"),
        ("name-intl-chars", "Ãệïøù Organization"),
    ],
)
def test_get_formatted_author_name(org_key, expected):
    org_dict = organizations[org_key]
    org = ContextEntity(None, **org_dict)

    result = get_affiliation_name_or_id(org)

    assert expected == result
