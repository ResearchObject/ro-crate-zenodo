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
SPDX_ID_PATTERN = r"^(?P<id>[-_.a-zA-Z0-9]+\+?)$"


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
    """Search the Zenodo license list and return the ID of the best match"""
    if not license:
        return None

    # first, look at @id
    if type(license) == ContextEntity:
        id = license["@id"]
        name = license.get("name", None)
    else:
        id = license
        if " " in license:
            name = license

    # if @id matches SPDX ID or URL patterns, extract the SPDX identifier
    # otherwise, try and use a name
    using_spdx = False
    using_name = False
    match = re.match(SPDX_URL_PATTERN, id)
    if not match:
        match = re.match(SPDX_ID_PATTERN, id)
    if match:
        using_spdx = True  # try to match exactly
        id = match.group("id")
        if id.endswith(".html") or id.endswith(".json"):
            id = id[:-5]
    else:
        using_name = True if name else False

    search_term = name if using_name else id
    # search Zenodo database for a matching license
    # this is quite a forgiving search so imperfect matches are possible
    # assume the first result is the best
    logger.debug(
        f'Searching Zenodo license list for "{search_term}". Using SPDX: {using_spdx}. Using name: {using_name}.'
    )
    if using_spdx:
        fields = ["id"]
    elif using_name:
        fields = ["title"]
    else:
        fields = ["id", "title", "props"]
    query = {"query_string": {"query": {search_term}, "fields": fields}}

    try:
        r = requests.get(
            f"https://sandbox.zenodo.org/api/licenses",
            params={"q": search_term, "size": 1, "sort": "bestmatch"},
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise RuntimeError(
                "Made too many requests to Zenodo API. Please wait a while and try again."
            )
        raise ValueError(
            f'Zenodo returned an error when searching for license "{search_term}": {r.json()}'
        )

    try:
        matched_license = r.json()["hits"]["hits"][0]
    except IndexError:
        raise ValueError(f'No matching license found for id "{id}"')

    if using_spdx and matched_license["id"] != id.lower():
        raise ValueError(
            f'Zenodo search returned license {matched_license["id"]}, which does not match SPDX id {id}'
        )
    matched_license_name = matched_license["title"]["en"]
    if using_name and matched_license_name.lower() != name.lower():
        raise ValueError(
            f"Zenodo search returned license {matched_license_name}, which does not match name {name}"
        )

    logger.debug(f"Found matching license: {matched_license_name}")
    return matched_license["id"]


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
