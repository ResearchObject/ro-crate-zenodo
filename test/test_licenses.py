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


@pytest.mark.parametrize(
    "license",
    SPDX_LICENSES[:10],
)
def test_get_license_from_spdx_reference(license):
    # Arrange
    id = license["licenseId"].lower()
    print(id)
    reference = license["reference"]

    # Act
    res = get_license(reference)

    # Assert
    assert res == id or None


@pytest.mark.parametrize(
    "license",
    SPDX_LICENSES[:10],
)
def test_get_license_from_spdx_name(license):
    # Arrange
    id = license["licenseId"].lower()
    print(id)
    name = license["name"]

    # Act
    res = get_license(name)

    # Assert
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
