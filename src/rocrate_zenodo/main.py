import argparse
from rocrate.rocrate import ROCrate

from rocrate_zenodo.upload import (
    build_zenodo_metadata_from_crate,
    ensure_crate_zipped,
    upload_crate_to_zenodo,
)


def cli_entry():
    parser = argparse.ArgumentParser(
        description="Takes a RO-Crate directory as input and uploads it to Zenodo"
    )

    parser.add_argument(
        "ro_crate_directory",
        help="RO-Crate directory to upload.",
        type=str,
        action="store",
    )
    parser.add_argument(
        "-s",
        "--sandbox",
        help="Upload to Zenodo sandbox rather than Zenodo production",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--publish",
        help="Publish the record after uploading.",
        action="store_true",
    )
    args = parser.parse_args()

    crate = ROCrate(args.ro_crate_directory)

    metadata = build_zenodo_metadata_from_crate(crate)
    crate_zip_path = ensure_crate_zipped(crate)
    record = upload_crate_to_zenodo(
        crate_zip_path, metadata, sandbox=args.sandbox, publish=args.publish
    )
    print(f'Created record {record["id"]} ({record["links"]["html"]})')
