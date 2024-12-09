import pytest
from unittest.mock import patch

from services.citation_service import (
    validate_article,
    validate_inproceedings,
    validate_book,
    validate_misc,
    UserInputError,
    generate_citation_key,
    normalize_month_input,
)


@pytest.fixture
def mock_repositories():
    # Mock repository methods that are used in citation_service
    with patch(
        "services.citation_service.article_repository"
    ) as mock_article_repo, patch(
        "services.citation_service.inproceedings_repository"
    ) as mock_inproceedings_repo, patch(
        "services.citation_service.book_repository"
    ) as mock_book_repo, patch(
        "services.citation_service.misc_repository"
    ) as mock_misc_repo:

        # By default, make is_key_unique return True (no duplicates)
        mock_article_repo.is_key_unique.return_value = True
        mock_inproceedings_repo.is_key_unique.return_value = True
        mock_book_repo.is_key_unique.return_value = True
        mock_misc_repo.is_key_unique.return_value = True

        # Make create methods return a dummy ID
        mock_article_repo.create_article.return_value = 1
        mock_inproceedings_repo.create_inproceedings.return_value = 2
        mock_book_repo.create_book.return_value = 3
        mock_misc_repo.create_misc.return_value = 4

        yield {
            "article": mock_article_repo,
            "inproceedings": mock_inproceedings_repo,
            "book": mock_book_repo,
            "misc": mock_misc_repo,
        }


def test_generate_citation_key_normal_case(mock_repositories):
    # Simple test for key generation with a two-part name
    key = generate_citation_key("John Doe", "2024")
    assert key == "JDoe2024"


def test_generate_citation_key_single_name(mock_repositories):
    # Test key generation with a single-part name
    key = generate_citation_key("Joulupukki", "2024")
    assert key == "Joulupukki2024"


def test_generate_citation_key_duplicates(mock_repositories):
    # Test what happens if the key initially isn’t unique
    # First call: is_key_unique -> False, forcing to add suffixes
    mock_repositories["article"].is_key_unique.side_effect = [False, True]

    key = generate_citation_key("John Doe", "2024")
    # First attempt would be "JDoe2024" (not unique), next "JDoe2024a"
    assert key == "JDoe2024a"


def test_normalize_month_input_numeric():
    assert normalize_month_input("1") == "January"
    assert normalize_month_input("12") == "December"


def test_normalize_month_input_abbreviation():
    assert normalize_month_input("Jan") == "January"
    assert normalize_month_input("Dec") == "December"


def test_normalize_month_input_full_name():
    assert normalize_month_input("January") == "January"
    assert normalize_month_input("january") == "January"


def test_normalize_month_input_invalid():
    with pytest.raises(ValueError):
        normalize_month_input("NotAMonth")

    with pytest.raises(ValueError):
        normalize_month_input("13")  # Invalid numeric month


def test_validate_article_success(mock_repositories):
    # All required fields and valid values
    article_id = validate_article(
        author="John Doe",
        title="A Great Discovery",
        journal="Famous Journal",
        year="2024",
        volume="10",
        number="2",
        pages="100-110",
        month="Mar",
        doi="10.1234/56789",
    )
    assert article_id == 1
    # Check that create_article was called with the normalized month and generated key
    args, kwargs = mock_repositories["article"].create_article.call_args
    assert kwargs["month"] == "March"
    assert kwargs["author"] == "John Doe"
    assert "key" in kwargs


def test_validate_article_missing_required_field(mock_repositories):
    # Missing author should raise an error
    with pytest.raises(UserInputError, match="Author is required"):
        validate_article(
            author="", title="A Great Discovery", journal="Famous Journal", year="2024"
        )


def test_validate_article_invalid_year(mock_repositories):
    # Invalid year should raise an error
    with pytest.raises(UserInputError):
        validate_article(
            author="John Doe",
            title="A Great Discovery",
            journal="Famous Journal",
            year="abcd",
        )


def test_validate_inproceedings_success(mock_repositories):
    inproc_id = validate_inproceedings(
        author="Jane Smith",
        title="A Conference Paper",
        booktitle="Proceedings of Something",
        year="2024",
        editor="Editor Name",
        volume="1",
        number="1",
        series="Lecture Notes",
        pages="50-60",
        address="Helsinki",
        month="Feb",
        organization="ACM",
        publisher="Springer",
    )
    assert inproc_id == 2
    args, kwargs = mock_repositories["inproceedings"].create_inproceedings.call_args
    assert kwargs["month"] == "February"
    assert kwargs["author"] == "Jane Smith"


def test_validate_book_success(mock_repositories):
    book_id = validate_book(
        author="John Doe",
        title="A Great Book",
        year="2024",
        publisher="Best Publisher",
        edition="2",
        pages="200",
    )
    assert book_id == 3
    args, kwargs = mock_repositories["book"].create_book.call_args
    assert kwargs["publisher"] == "Best Publisher"
    assert kwargs["edition"] == "2"


def test_validate_misc_success(mock_repositories):
    misc_id = validate_misc(
        author="John Doe",
        title="Some Title",
        year="2024",
        month="Jan",
        howpublished="Online",
        note="Some note",
    )
    assert misc_id == 4
    args, kwargs = mock_repositories["misc"].create_misc.call_args
    assert kwargs["month"] == "January"
    assert kwargs["howpublished"] == "Online"
    assert kwargs["note"] == "Some note"


def test_validate_misc_missing_required(mock_repositories):
    # Missing title
    with pytest.raises(UserInputError):
        validate_misc(author="John Doe", title="", year="2024")

    # Missing author
    with pytest.raises(UserInputError):
        validate_misc(author="", title="Some Title", year="2024")

    # Missing year
    with pytest.raises(UserInputError):
        validate_misc(author="John Doe", title="Some Title", year="")
