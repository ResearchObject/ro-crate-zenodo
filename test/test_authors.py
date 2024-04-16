from unittest import TestCase

from rocrate.model.person import Person

from ro_crate_uploader.upload import (
    build_zenodo_creator_list,
)

person_with_id_orcid = {
    "@id": "https://orcid.org/0000-0000-0000-0000",
    "@type": Person,
    "affiliation": "Test University",
    "name": "ORCID Person",
}

person_with_id_uri = {
    "@id": "https://example.org",
    "@type": Person,
    "affiliation": "Test University",
    "name": "URI Person",
}

person_with_id_local = {
    "@id": "#local_person",
    "@type": Person,
    "affiliation": "Test University",
    "name": "Local Person",
}

person_with_id_name = {"@id": "Named Person"}

person_with_id_blank = {
    "@id": "_:blank_person",
    "@type": Person,
}

person_with_intl_chars = {
    "@id": "https://orcid.org/0000-0000-0000-0001",
    "@type": Person,
    "affiliation": "Test University",
    "name": "Ãệïøù Person",
}


class TestAuthorConversion(TestCase):
    def test_orcid_person(self):
        # Arrange
        person = person_with_id_orcid
        expected = {
            "name": person["name"],
            "affiliation": person["affiliation"],
            "orcid": person["@id"],
            "gnd": None,
        }

        # Act
        result = build_zenodo_creator_list(person)

        # Assert
        self.assertDictEqual(expected, result[0].model_dump())

    def test_uri_person(self):
        # Arrange
        person = person_with_id_uri
        expected = {
            "name": person["name"],
            "affiliation": person["affiliation"],
            "orcid": None,
            "gnd": None,
        }

        # Act
        result = build_zenodo_creator_list(person)

        # Assert
        self.assertDictEqual(expected, result[0].model_dump())

    def test_local_person(self):
        # Arrange
        expected = {
            "name": "Local Person",
            "affiliation": "Test University",
            "orcid": None,
            "gnd": None,
        }

        # Act
        result = build_zenodo_creator_list(person_with_id_local)

        # Assert
        self.assertDictEqual(expected, result[0].model_dump())

    def test_named_person(self):
        # Arrange
        person = person_with_id_local
        expected = {
            "name": person["name"],
            "affiliation": None,
            "orcid": None,
            "gnd": None,
        }

        # Act
        result = build_zenodo_creator_list(person)

        # Assert
        self.assertDictEqual(expected, result[0].model_dump())

    def test_blank_person(self):
        # Arrange
        person = person_with_id_blank
        expected = {
            "name": None,
            "affiliation": None,
            "orcid": None,
            "gnd": None,
        }

        # Act
        result = build_zenodo_creator_list(person)

        # Assert
        self.assertDictEqual(expected, result[0].model_dump())

    def test_person_with_intl_chars(self):
        # Arrange
        person = person_with_intl_chars
        expected = {
            "name": person["name"],
            "affiliation": person["affiliation"],
            "orcid": person["@id"],
            "gnd": None,
        }

        # Act
        result = build_zenodo_creator_list(person)

        # Assert
        self.assertDictEqual(expected, result[0].model_dump())
