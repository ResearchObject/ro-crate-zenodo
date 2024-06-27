from rocrate.rocrate import ROCrate

from rocrate_zenodo.upload import (
    build_zenodo_metadata_from_crate,
    ensure_crate_zipped,
    upload_crate_to_zenodo,
)

if __name__ == "__main__":
    crate_path = "./demo_crate"
    crate = ROCrate(crate_path)

    metadata = build_zenodo_metadata_from_crate(crate)
    crate_zip_path = ensure_crate_zipped(crate)
    record = upload_crate_to_zenodo(crate_zip_path, metadata)
    print("Created record:")
    print(record)
