import pytest
from services.citation_service import (
    validate_article,
    UserInputError,
    generate_citation_key,
)
from unittest.mock import patch


def test_validate_article_valid():
    """Test that a valid article passes validation and is created."""
    with patch("services.citation_service.get_existing_keys") as mock_get_keys, patch(
        "services.citation_service.generate_citation_key"
    ) as mock_generate_key, patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
        mock_get_keys.return_value = {"GSmiths2023", "GSmiths2023a"}
        mock_generate_key.side_effect = (
            lambda author, year, existing_keys: f"{author[:2].upper()}{year}"
        )
        mock_create.return_value = 1

        result = validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            volume="10",
            number="2",
            pages="1-10",
            month="December",
            doi="10.1234/example-doi",
        )

        assert result == 1
        mock_create.assert_called_once()
        mock_generate_key.assert_called_once_with(
            "Joulupukki", "2023", {"GSmiths2023", "GSmiths2023a"}
        )


def test_validate_article_with_conflicting_key():
    """Test that a conflicting citation key triggers unique generation."""
    with patch("services.citation_service.get_existing_keys") as mock_get_keys, patch(
        "services.citation_service.generate_citation_key"
    ) as mock_generate_key, patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
        mock_get_keys.return_value = {"GSmiths2023", "GSmiths2023a"}
        mock_generate_key.side_effect = (
            lambda author, year, existing_keys: "Joulupukki2023b"
        )  # Simulate unique key generation
        mock_create.return_value = 1

        result = validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )

        assert result == 1
        mock_create.assert_called_once()
        mock_generate_key.assert_called_once_with(
            "Joulupukki", "2023", {"GSmiths2023", "GSmiths2023a"}
        )


def test_validate_article_invalid_author():
    """Test that an invalid author raises UserInputError."""
    with patch("services.citation_service.get_existing_keys"):
        with pytest.raises(
            UserInputError, match="Author name must be between 2 and 500 characters."
        ):
            validate_article(
                author="j",
                title="Toimitusketjujen optimointi",
                journal="Joulutiede Journal",
                year="2023",
            )


def test_validate_article_invalid_year():
    """Test that an invalid year raises UserInputError."""
    with patch("services.citation_service.get_existing_keys"):
        with pytest.raises(
            UserInputError, match="Year must be a valid number between 0 and 2100."
        ):
            validate_article(
                author="Joulupukki",
                title="Toimitusketjujen optimointi",
                journal="Joulutiede Journal",
                year="20twenty",  # Invalid year
            )


def test_validate_article_missing_author():
    """Test that a missing author raises UserInputError."""
    with patch("services.citation_service.get_existing_keys"):
        with pytest.raises(UserInputError, match="Author is required"):
            validate_article(
                author="",
                title="The Future of AI",
                journal="AI Journal",
                year="2023",
            )


def test_generate_citation_key_unique():
    """Test that generate_citation_key resolves conflicts and creates unique keys."""
    existing_keys = {"JDoe2023", "JDoe2023a", "JDoe2023b"}

    with patch("services.citation_service.generate_citation_key") as mock_key_gen:
        mock_key_gen.side_effect = lambda author, year, keys: (
            "JDoe2023c" if "JDoe2023c" not in keys else "JDoe2023d"
        )

        unique_key = generate_citation_key("John Doe", "2023", existing_keys)
        assert unique_key == "JDoe2023c"

        existing_keys.add(unique_key)

        another_key = generate_citation_key("John Doe", "2023", existing_keys)
        assert another_key == "JDoe2023d"


def test_generate_citation_key_no_conflict():
    """Test that generate_citation_key generates a clean key if no conflict exists."""
    existing_keys = {"GSmiths2023", "GSmiths2023a", "GSmiths2023b"}
    generated_key = generate_citation_key("Jane Smith", "2023", existing_keys)
    assert generated_key == "JSmith2023"
