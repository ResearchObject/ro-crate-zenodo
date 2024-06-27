from unittest import TestCase

from rocrate.rocrate import ROCrate

from rocrate_zenodo.upload import (
    build_zenodo_metadata_from_crate,
)


class TestUpload(TestCase):
    def test_build_zenodo_metadata(self):
        # Arrange
        crate_path = "test/test_data/valid_crate"
        crate = ROCrate(crate_path)

        expected = {
            "title": "Demo Crate",
            "upload_type": "dataset",
            "description": "a demo crate for Galaxy training",
            "creators": [
                {
                    "name": "Smith, Jane",
                    "affiliation": "Example University",
                    "orcid": "0000-0000-0000-0000",
                    "gnd": None,
                }
            ],
            "license": "cc-by-nc-sa-4.0",
        }

        # Act
        result = build_zenodo_metadata_from_crate(crate)
        result = result.model_dump()
        result_select = {key: result[key] for key in result if key in expected}

        # Assert
        self.assertDictEqual(expected, result_select)

    def test_build_zenodo_metadata_fails_with_invalid_data(self):
        # Arrange
        crate_path = "test/test_data/invalid_data_crate"
        crate = ROCrate(crate_path)

        # Act
        with self.assertRaises(RuntimeError) as cm:
            build_zenodo_metadata_from_crate(crate)

        # Assert
        message = str(cm.exception)
        self.assertIn(
            "The RO-Crate metadata could not be converted to Zenodo metadata",
            message,
        )
        self.assertIn("title", message)
        self.assertIn("description", message)
