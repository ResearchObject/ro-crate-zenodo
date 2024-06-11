from unittest import TestCase

import json
import requests
import pytest

from rocrate.model.person import Person
from rocrate.rocrate import ROCrate, ContextEntity

from rocrate_upload.upload import (
    build_zenodo_creator_list,
    build_zenodo_metadata_from_crate,
    get_license,
)

SPDX_LICENSES = requests.get(
    "https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json"
).json()["licenses"]

ZENODO_LICENSES = requests.get(
    "https://raw.githubusercontent.com/zenodo/zenodo-rdm/e477db5dad2c35edd3e6549c8725e1d67fab4ba2/app_data/vocabularies/licenses.csv",
).content
ZENODO_LICENSES = str(ZENODO_LICENSES)

SPDX_LICENSES_IN_ZENODO = [
    l for l in SPDX_LICENSES if f'{l["licenseId"].lower()},' in ZENODO_LICENSES
]

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
def test_get_license_from_spdx_name(license):
    # Arrange
    name = license["name"]

    # Act & Assert
    res = get_license(name)
    assert res == name


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_urls(license):
    # Arrange
    urls = license["seeAlso"]

    # Act
    res = [get_license(url) for url in urls]

    # Assert
    for r, u in zip(res, urls):
        assert r == u


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_entity__id_spdx_uri(license):
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
def test_get_license_from_entity__id_spdx_id(license):
    """Just the SPDX id will not be used - as creates false positives with local ids"""
    # Arrange
    entity = ContextEntity(
        None, license["licenseId"], properties={"name": license["name"]}
    )

    # Act
    res = get_license(entity)

    # Assert
    assert res == license["name"]


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_entity__id_name(license):
    # Arrange
    entity = ContextEntity(None, license["name"])

    # Act
    res = get_license(entity)

    # Assert
    assert res == license["name"]


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_entity__id_url(license):
    # Arrange
    entity = ContextEntity(None, license["seeAlso"][0])

    # Act
    res = get_license(entity)

    # Assert
    assert res == license["seeAlso"][0]


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_entity__id_local(license):
    # Arrange
    entity = ContextEntity(None, "#local_id", properties={"name": license["name"]})

    # Act
    res = get_license(entity)

    # Assert
    assert res == license["name"]


@pytest.mark.parametrize(
    "license",
    LICENSES_TO_TEST,
)
def test_get_license_from_entity__id_local_no_name(license):
    # Arrange
    entity = ContextEntity(None, "#local_id")

    # Act
    res = get_license(entity)

    # Assert
    assert res == "local_id"
