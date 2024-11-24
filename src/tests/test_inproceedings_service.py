import pytest
from services.inproceedings_service import validate_inproceedings, UserInputError
from unittest.mock import patch

def test_validate_inproceedings_valid():
    """Test that a valid inproceedings passes validation and is created."""
    with patch("services.inproceedings_service.inproceedings_repository.create_inproceedings") as mock_create:
        mock_create.return_value = 1

        result = validate_inproceedings(
            title="An Analysis of Example",
            author="John Smith and Jane Doe",
            year="2022",
            month="June",
            booktitle="Proceedings of the International Conference on Example",
            publisher="ACM Press",
            address="New York, NY",
            series="Example Conference Proceedings",
            volume="1",
            number="2",
            pages="123-130",
            editor="David Brown and Susan Green",
            organization="ACM"
        )

        assert result == 1
        mock_create.assert_called_once()

def test_validate_inproceedings_missing_optional_fields():
    """Test that an inproceedings can be created without optional fields."""
    with patch("services.inproceedings_service.inproceedings_repository.create_inproceedings") as mock_create:
        mock_create.return_value = 1

        result = validate_inproceedings(
            title="An Analysis of Example",
            author="John Smith and Jane Doe",
            year="2022",
            booktitle="Proceedings of the International Conference on Example",
        )

        assert result == 1
        mock_create.assert_called_once()