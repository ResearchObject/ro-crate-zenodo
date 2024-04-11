from ro_crate_uploader.upload import (
    build_zenodo_creator_list,
    build_zenodo_metadata_from_crate,
)
from rocrate.model.person import Person
from rocrate.rocrate import ROCrate
from unittest import TestCase
from zenodo_client import Metadata


class TestUpload(TestCase):
    def test_build_zenodo_metadata_from_crate(self):
        # Arrange
        crate_path = "test/test_data/demo_crate"
        crate = ROCrate(crate_path)

        expected = {
            "title": "Demo Crate",
            "upload_type": "dataset",
            "description": "a demo crate for Galaxy training",
            "creators": [
                {
                    "name": "Jane Smith",
                    "affiliation": None,
                    "orcid": None,
                    "gnd": None,
                }
            ],
        }

        # Act
        result = build_zenodo_metadata_from_crate(crate)
        result = result.model_dump()
        result_select = {key: result[key] for key in result if key in expected}

        # Assert
        self.assertDictEqual(expected, result_select)

    def test_build_zenodo_creator_list__single_author(self):
        authors = Person(
            crate=None,
            identifier="https://orcid.org/0000-0000-0000-0000",
            properties={"name": "Jane Smith", "affiliation": None},
        )
        expected = [
            {
                "name": "Jane Smith",
                "affiliation": None,
                "orcid": None,
                "gnd": None,
            }
        ]

        # Act
        result = build_zenodo_creator_list(authors)

        # Assert
        self.assertEqual(len(result), len(expected))
        self.assertDictEqual(expected[0], result[0].model_dump())
