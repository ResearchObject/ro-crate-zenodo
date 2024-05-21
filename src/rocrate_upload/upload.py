from __future__ import annotations
from typing import Any

import json
import requests

from pydantic_core import ValidationError
from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity
from zenodo_client import Metadata, create_zenodo
import logging

from rocrate_upload.authors import build_zenodo_creator_list

logging.basicConfig(format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def build_zenodo_metadata_from_crate(crate: ROCrate) -> Metadata:
    """Given an RO-Crate, collect the metadata to use in Zenodo upload"""
    # retrieve author(s)
    authors = crate.root_dataset.get("author")
    creators = build_zenodo_creator_list(authors)

    # retrieve title
    title = crate.root_dataset.get("name")
    description = crate.root_dataset.get("description")

    license = get_license(crate.root_dataset.get("license", ""))

    # Define the metadata that will be used on initial upload
    # Metadata is a Pydantic model that provides some type validation
    try:
        data = Metadata(
            title=title,
            upload_type="dataset",
            description=description,
            creators=creators,
            license=license,
        )
    except ValidationError as exception:
        errors = json.loads(exception.json())
        msg = (
            "The RO-Crate metadata could not be converted to Zenodo metadata. "
            "Encountered the following errors:\n"
        )
        for e in errors:
            # TODO: replace Metadata field with corresponding RO-Crate field
            field = ", ".join(e["loc"])
            msg += f"Field {field}: {e['msg']}\n"
        raise RuntimeError(msg)

    return data


def get_license(license: str | ContextEntity) -> str | None:
    """Search the Zenodo license list and return the ID of the best match"""
    if not license:
        return None

    # the id in the RO-Crate should be sufficient
    # whether this is a URI, a name, or an identifier
    if type(license) == ContextEntity:
        id = license["@id"]
    else:
        id = license

    # search Zenodo database for a matching license
    # this is quite a forgiving search so imperfect matches are possible
    # assume the first result is the best
    r = requests.get(f"https://zenodo.org/api/licenses?q={id}&size=1&sort=bestmatch")
    r.raise_for_status()
    matched_license = r.json()["hits"]["hits"][0]

    logger.debug(f"Found matching license: {matched_license['title']['en']}")
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
