from unittest import TestCase

import requests
import pytest

from rocrate.model.person import Person
from rocrate.rocrate import ROCrate

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
print(SPDX_LICENSES_IN_ZENODO)


@pytest.mark.parametrize(
    "license",
    SPDX_LICENSES_IN_ZENODO,
)
def test_get_license_from_spdx_reference(license):
    # Arrange
    print(len(SPDX_LICENSES_IN_ZENODO))

    id = license["licenseId"].lower()
    print(id)
    reference = license["reference"]

    # Act & Assert
    res = get_license(reference)
    assert res == id


@pytest.mark.parametrize(
    "license",
    SPDX_LICENSES_IN_ZENODO,
)
def test_get_license_from_spdx_name(license):
    # Arrange
    id = license["licenseId"].lower()
    print(id)
    name = license["name"]

    # Act & Assert
    res = get_license(name)
    assert res == id


# @pytest.mark.parametrize(
#     "license",
#     LICENSES[:5],
# )
# def test_get_license_from_urls(license):
#     # Arrange
#     id = license["licenseId"].lower()
#     print(id)
#     urls = license["seeAlso"]

#     # Act
#     res = [get_license(url) for url in urls]

#     # Assert
#     for r in res:
#         assert r == id
