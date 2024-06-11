from __future__ import annotations
from typing import Any

import re
import json
import requests
from urllib.parse import urlencode

from pydantic_core import ValidationError
from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity
from zenodo_client import Metadata, create_zenodo
import logging

from rocrate_upload.authors import build_zenodo_creator_list

logging.basicConfig(format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SPDX_URL_PATTERN = r"^https?:\/\/spdx.org\/licenses\/(?P<id>[-_.a-zA-Z0-9]+\+?)$"
# SPDX_ID_PATTERN = r"^(?P<id>[-_.a-zA-Z0-9]+\+?)$"


def build_zenodo_metadata_from_crate(crate: ROCrate) -> Metadata:
    """Given an RO-Crate, collect the metadata to use in Zenodo upload"""
    # retrieve author(s)
    authors = crate.root_dataset.get("author")
    creators = build_zenodo_creator_list(authors)

    # retrieve title
    title = crate.root_dataset.get("name")
    description = crate.root_dataset.get("description")

    license = crate.root_dataset.get("license", "")
    try:
        license_id = get_license(license)
    except ValueError as e:
        license_input = license["@id"] if type(license) == ContextEntity else license
        logger.debug(str(e))
        logger.warning(
            f"Could not find a matching license for {license_input} on Zenodo. "
            "Please enter the license manually after uploading."
        )
        license_id = None

    # Define the metadata that will be used on initial upload
    # Metadata is a Pydantic model that provides some type validation
    try:
        data = Metadata(
            title=title,
            upload_type="dataset",
            description=description,
            creators=creators,
            license=license_id,
        )
    except ValidationError as exception:
        errors = json.loads(exception.json())
        msg = (
            "The RO-Crate metadata could not be converted to Zenodo metadata. "
            "Encountered the following errors:\n"
        )
        for err in errors:
            # TODO: replace Metadata field with corresponding RO-Crate field
            field = ", ".join(err["loc"])
            msg += f"Field {field}: {err['msg']}\n"
        raise RuntimeError(msg)

    return data


def get_license(license: str | ContextEntity) -> str | None:
    """Extract the license SPDX ID, URI, or name, in order of preference"""
    if not license:
        return None

    # first, look at @id
    if type(license) == ContextEntity:
        id = license["@id"].lstrip("#")
        name = license.get("name", None)
    else:
        id = license
        name = None

    # if @id matches SPDX URI patterns, extract the SPDX identifier and return that
    match = re.match(SPDX_URL_PATTERN, id)
    if match:
        id = match.group("id")
        if id.endswith(".html") or id.endswith(".json"):
            id = id[:-5]
        id = id.lower()
        return id
    elif " " in id or "http" in id:
        # we have a name or a URI, return that
        return id
    else:
        # otherwise, try and use a name, but fall back on id
        return name if name else id


def ensure_crate_zipped(crate: ROCrate) -> str:
    """Returns a path to the zipped crate."""
    # TODO - use original crate path if it was a zip
    # TODO - save zipped crate to crate parent directory
    zip_path = "/tmp/crate.zip"
    zipped = crate.write_zip(zip_path)
    return zipped


def upload_crate_to_zenodo(crate_zip_path: str, metadata: Metadata) -> Any:
    """Upload a zipped crate and its metadata to Zenodo.

    It's recommended to keep sandbox=True until ready for production use."""
    # for now, create only, don't update
    res = create_zenodo(
        # this is a unique key you pick that will be used to store
        # the numeric deposition ID on your local system's cache
        # key="ro-crate-uploader",
        data=metadata,
        paths=[
            crate_zip_path,
        ],
        sandbox=True,  # remove this when you're ready to upload to real Zenodo
        publish=False,
    )

    return res.json()
