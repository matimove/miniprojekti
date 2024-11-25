import pytest
from services.book_service import validate_book, UserInputError
from unittest.mock import patch

def test_validate_book_valid():
    """Test that a valid book passes validation and is created."""
    with patch("services.book_service.book_repository.create_book") as mock_create:
        mock_create.return_value = 1

        result = validate_book(
            title="An Analysis of Example",
            author="John Smith and Jane Doe",
            year="2022",
            publisher="ACM Press",
            pages="123-130",
            doi="10.1111/11111"
        )

        assert result == 1
        mock_create.assert_called_once()

def test_validate_book_missing_optional_fields():
    """Test that an book can be created without optional fields."""
    with patch("services.book_service.book_repository.create_book") as mock_create:
        mock_create.return_value = 1

        result = validate_book(
            title="An Analysis of Example",
            author="John Smith and Jane Doe",
            year="2022",
        )

        assert result == 1
        mock_create.assert_called_once()

def test_validate_book_invalid_author():
    """Test that an invalid book title raises UserInputError."""
    with pytest.raises(UserInputError, match="Title must be between 5 and 255 characters."):
        validate_book(author="Joulupukki", title="t", year="2023")
