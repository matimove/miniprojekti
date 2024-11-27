import pytest
from services.citation_service import validate_misc, UserInputError
from unittest.mock import patch


def test_validate_misc_valid():
    """Test that a valid misc passes validation and is created."""
    with patch("services.citation_service.misc_repository.create_misc") as mock_create:
        mock_create.return_value = 1

        result = validate_misc(
            title="An Analysis of Example",
            author="John Smith and Jane Doe",
            year="2022",
            month="12",
            howpublished="test",
            note="test note",
        )

        assert result == 1
        mock_create.assert_called_once()


def test_validate_misc_missing_optional_fields():
    """Test that an misc can be created without optional fields."""
    with patch("services.citation_service.misc_repository.create_misc") as mock_create:
        mock_create.return_value = 1

        result = validate_misc(
            title="An Analysis of Example",
            author="John Smith and Jane Doe",
            year="2022",
        )

        assert result == 1
        mock_create.assert_called_once()


def test_validate_misc_invalid_title():
    """Test that an invalid misc title raises UserInputError."""
    with pytest.raises(
        UserInputError, match="Title must be between 5 and 255 characters."
    ):
        validate_misc(author="Kirjailija", title="t", year="2023")


def test_validate_misc_note_forbidden_characters():
    """Test that invalid pages raise UserInputError."""
    with pytest.raises(UserInputError, match="Note contains invalid characters."):
        validate_misc(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            year="2023",
            note="==",
        )


def test_validate_misc_invalid_year():
    """Test that an invalid misc title raises UserInputError."""
    with pytest.raises(
        UserInputError, match="Year must be a valid number between 1500 and 2100."
    ):
        validate_misc(author="Kirjailija", title="Otsikko", year="3000")
