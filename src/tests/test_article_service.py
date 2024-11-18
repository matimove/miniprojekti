import pytest
from services.article_service import validate_article, UserInputError
from unittest.mock import patch

def test_validate_article_valid():
    """Test that a valid article passes validation and is created."""
    with patch("services.article_service.article_repository.create_article") as mock_create:
        mock_create.return_value = 1  # Simulate a valid article ID being returned

        # Call validate_article with valid inputs
        result = validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            volume="10",
            number="2",
            pages="1-10",
            month="December",
            doi="10.1234/example-doi"
        )

        assert result == 1  # Should return the article ID
        mock_create.assert_called_once()  # Ensure repository method was called


def test_validate_article_invalid_author():
    """Test that an invalid author raises UserInputError."""
    with pytest.raises(UserInputError, match="Author name must be between 2 and 100 characters."):
        validate_article(
            author="j",  # Invalid author
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023"
        )

def test_validate_article_missing_author():
    """Test that an missing author input raises UserInputError."""
    with pytest.raises(UserInputError, match="Author is required"):
        validate_article(
            author="",  # Missing author
            title="The Future of AI",
            journal="AI Journal",
            year="2023"
        )

def test_validate_article_invalid_year():
    """Test that an invalid year raises UserInputError."""
    with pytest.raises(UserInputError, match="Year must be a valid number between 1500 and 2100."):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="20twenty" # Invalid year
        )


def test_validate_article_invalid_title():
    """Test that an invalid title raises UserInputError."""
    with pytest.raises(UserInputError, match="Title contains invalid characters."):
        validate_article(
            author="Joulupukki",
            title="Toimitus<script>alert('bad')</script>", # Invalid title
            journal="Joulutiede Journal",
            year="2023"
        )
