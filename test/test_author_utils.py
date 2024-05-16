import pytest

from rocrate_upload.authors import get_orcid_id_or_none, get_author_details


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
