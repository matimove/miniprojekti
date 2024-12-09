import pytest
from services.citation_service import validate_article, UserInputError
from unittest.mock import patch


def test_validate_article_valid():
    """Test that a valid article passes validation and is created."""
    with patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
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


def test_validate_article_missing_optional_fields():
    """Test that an article can be created without optional fields."""
    with patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
        mock_create.return_value = 1

        result = validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )

        assert result == 1
        mock_create.assert_called_once()


def test_validate_article_invalid_author():
    """Test that an invalid author raises UserInputError."""
    with pytest.raises(
        UserInputError, match="Author name must be between 2 and 500 characters."
    ):
        validate_article(
            author="j",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )


def test_validate_article_invalid_volume():
    """Test that an invalid volume raises UserInputError."""
    with pytest.raises(UserInputError, match="Volume must be a valid number."):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            volume="invalid",
        )


def test_validate_article_repository_failure():
    """Test that repository failure raises an exception."""
    with patch(
        "services.citation_service.article_repository.create_article",
        side_effect=Exception("DB Error"),
    ):
        with pytest.raises(Exception, match="DB Error"):
            validate_article(
                author="Joulupukki",
                title="Toimitusketjujen optimointi",
                journal="Joulutiede Journal",
                year="2023",
            )


def test_validate_article_missing_author():
    """Test that an missing author input raises UserInputError."""
    with pytest.raises(UserInputError, match="Author is required"):
        validate_article(
            author="",  # Missing author
            title="The Future of AI",
            journal="AI Journal",
            year="2023",
        )


def test_validate_article_invalid_year():
    """Test that an invalid year raises UserInputError."""
    with pytest.raises(
        UserInputError, match="Year must be a valid number between 0 and 2100."
    ):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="20twenty",  # Invalid year
        )


def test_validate_article_invalid_title():
    """Test that an invalid title raises UserInputError."""
    with pytest.raises(UserInputError, match="Title contains invalid characters."):
        validate_article(
            author="Joulupukki",
            title="Toimitus<script>alert('bad')</script>",  # Invalid title
            journal="Joulutiede Journal",
            year="2023",
        )


def test_validate_article_missing_optional_fields():
    """Test that an article can be created without optional fields."""
    with patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
        mock_create.return_value = 1

        # Call validate_article with only required fields
        result = validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )

        assert result == 1  # Should return the article ID
        mock_create.assert_called_once()  # Ensure repository method was called


def test_validate_article_invalid_volume():
    """Test that an invalid volume raises UserInputError."""
    with pytest.raises(UserInputError, match="Volume must be a valid number."):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            volume="invalid",  # Invalid volume
        )


def test_validate_article_invalid_pages():
    """Test that invalid pages raise UserInputError."""
    with pytest.raises(UserInputError, match="Pages must be a number or range."):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            pages="not-a-range",  # Invalid pages
        )


def test_validate_article_invalid_month():
    """Test that an invalid month raises UserInputError."""
    with pytest.raises(
        UserInputError, match="Month must be a valid name or abbreviation."
    ):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            month="FakeMonth",  # Invalid month
        )


def test_validate_valid_numeric_month():
    """Test that a valid article passes validation and is created."""
    with patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
        mock_create.return_value = 1

        result = validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            volume="10",
            number="2",
            pages="1-10",
            month="12",
            doi="10.1234/example-doi",
        )

        assert result == 1
        mock_create.assert_called_once()


def test_validate_article_invalid_numeric_month():
    """Test that an invalid month raises UserInputError."""
    with pytest.raises(
        UserInputError, match="Numeric month input must be between 1 and 12."
    ):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            month="13",  # Invalid month
        )


def test_validate_valid_abbreviated_month():
    """Test that a valid article passes validation and is created."""
    with patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
        mock_create.return_value = 1

        result = validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            volume="10",
            number="2",
            pages="1-10",
            month="Dec",
            doi="10.1234/example-doi",
        )

        assert result == 1
        mock_create.assert_called_once()


def test_validate_article_invalid_abbreviated_month():
    """Test that an invalid month raises UserInputError."""
    with pytest.raises(
        UserInputError, match="Month must be a valid name or abbreviation."
    ):
        validate_article(
            author="Joulupukki",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
            month="Doc",  # Invalid month
        )


def test_validate_article_repository_failure():
    """Test that repository failure raises an exception."""
    with patch(
        "services.citation_service.article_repository.create_article",
        side_effect=Exception("DB Error"),
    ):
        with pytest.raises(Exception, match="DB Error"):
            validate_article(
                author="Joulupukki",
                title="Toimitusketjujen optimointi",
                journal="Joulutiede Journal",
                year="2023",
            )


def test_validate_article_author_boundary():
    """Test author field boundary values."""
    with patch(
        "services.citation_service.article_repository.create_article"
    ) as mock_create:
        mock_create.return_value = 1

        # Minimum valid length
        result = validate_article(
            author="Jo",
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )
        assert result == 1

        # Maximum valid length
        long_author = "J" * 100
        result = validate_article(
            author=long_author,
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )
        assert result == 1

    # Invalid lengths
    with pytest.raises(
        UserInputError, match="Author name must be between 2 and 500 characters."
    ):
        validate_article(
            author="J",  # Too short
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )

    with pytest.raises(
        UserInputError, match="Author name must be between 2 and 500 characters."
    ):
        validate_article(
            author="J" * 501,  # Too long
            title="Toimitusketjujen optimointi",
            journal="Joulutiede Journal",
            year="2023",
        )
