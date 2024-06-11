import json
import pytest

from rocrate.rocrate import ContextEntity

from rocrate_upload.upload import (
    get_license,
)

with open("test/test_data/licenses.json") as licenses_file:
    LICENSES_TO_TEST = json.load(licenses_file)["licenses"]


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_spdx_reference(license):
    # Arrange
    id = license["licenseId"].lower()
    reference = license["reference"]

    # Act & Assert
    res = get_license(reference)
    assert res == id


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_fails_with_non_spdx_string(license):
    # Arrange
    name = license["name"]

    # Act & Assert
    with pytest.raises(ValueError):
        res = get_license(name)


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_entity(license):
    # Arrange
    entity = ContextEntity(
        None, license["reference"], properties={"name": license["name"]}
    )

    # Act
    res = get_license(entity)

    # Assert
    assert res == license["licenseId"].lower()


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_entity_fails_if_no_spdx_uri(license):
    """Just the SPDX id will not be used - as creates false positives with local ids"""
    # Arrange
    entity = ContextEntity(
        None, license["licenseId"], properties={"name": license["name"]}
    )

    # Act & Assert
    with pytest.raises(ValueError):
        res = get_license(entity)
