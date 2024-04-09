from rocrate.rocrate import ROCrate
from rocrate.model.person import Person
from zenodo_client import Creator, Metadata, ensure_zenodo


def build_zenodo_creator_list(authors: list[Person] | Person) -> list[Creator]:
    if isinstance(authors, list):
        return [Creator(name=a["name"]) for a in authors]
    else:
        # single author
        return [Creator(name=authors["name"])]


# load a crate
crate_path = "test/test-data/crate1"
crate = ROCrate(crate_path)

# retrieve author(s)
authors = crate.root_dataset.get("author")
creators = build_zenodo_creator_list(authors)

# retrieve title
title = crate.root_dataset.get("name")
description = crate.root_dataset.get("description")

# generate zip file
zip_path = f"{crate_path}.zip"
zipped = crate.write_zip(zip_path)
print(zipped)

# Define the metadata that will be used on initial upload
data = Metadata(
    title=title,
    upload_type="dataset",
    description=description,
    creators=creators,
)

# res = ensure_zenodo(
#     key="ro-crate-uploader",  # this is a unique key you pick that will be used to store
#     # the numeric deposition ID on your local system's cache
#     data=data,
#     paths=[
#         zip_path,
#     ],
#     sandbox=True,  # remove this when you're ready to upload to real Zenodo
# )

# print(res.json())
