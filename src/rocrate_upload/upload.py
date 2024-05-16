from __future__ import annotations

import json

from pydantic_core import ValidationError
from rocrate.rocrate import ROCrate
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

    # Define the metadata that will be used on initial upload
    # Metadata is a Pydantic model that provides some type validation
    try:
        data = Metadata(
            title=title,
            upload_type="dataset",
            description=description,
            creators=creators,
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


def ensure_crate_zipped(crate: ROCrate) -> str:
    """Returns a path to the zipped crate."""
    # TODO - use original crate path if it was a zip
    # TODO - save zipped crate to crate parent directory
    zip_path = "/tmp/crate.zip"
    zipped = crate.write_zip(zip_path)
    return zipped


def upload_crate_to_zenodo(crate_zip_path: str, metadata: Metadata):
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


# included for convenience, remove or update this as code expands
if __name__ == "__main__":
    crate_path = "../demo/demo_crate"
    crate = ROCrate(crate_path)

    metadata = build_zenodo_metadata_from_crate(crate)
    crate_zip_path = ensure_crate_zipped(crate)
    record = upload_crate_to_zenodo(crate_zip_path, metadata)
    logger.debug("Created record:")
    logger.debug(record)
