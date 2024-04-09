from rocrate.rocrate import ROCrate
from zenodo_client import Creator, Metadata, Zenodo, ensure_zenodo

# load a crate
crate_path = "test/test-data/crate1"
crate = ROCrate(crate_path)

# convert it to zip
zip_path = f"{crate_path}.zip"
zipped = crate.write_zip(zip_path)
print(zipped)

# retrieve author(s)
author = crate.root_dataset.get("author")
if isinstance(author, list):
    creators = [Creator(name=a["name"]) for a in author]
else:
    creators = [Creator(name=author["name"])]

# retrieve title
title = crate.root_dataset.get("name")
description = crate.root_dataset.get("description")

# Define the metadata that will be used on initial upload
data = Metadata(
    title=title,
    upload_type="dataset",
    description=description,
    creators=creators,
)

res = ensure_zenodo(
    key="ro-crate-uploader",  # this is a unique key you pick that will be used to store
    # the numeric deposition ID on your local system's cache
    data=data,
    paths=[
        zip_path,
    ],
    sandbox=True,  # remove this when you're ready to upload to real Zenodo
)

print(res.json())
