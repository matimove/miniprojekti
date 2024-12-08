import pytest
import re

from validators import (
    validate_author,
    validate_title,
    validate_journal,
    validate_year,
    validate_doi,
    validate_month,
    validate_pages,
    validate_common_pattern,
)


def test_validate_author_valid():
    """Test a valid author."""
    assert validate_author("Joulupukki") is None  # Should pass without error


def test_validate_multiple_authors_valid():
    """Test a valid author input with multiple differing authors containing special characters, separated by commas."""
    assert (
        validate_author(
            "Joulupukki, Joulumuori, Tonttu T. Toljanteri, Petteri Punakuono, Iso-Tonttu, Ääkkösmies Öökkölä"
        )
        is None
    )  # Should pass without error


def test_validate_author_invalid():
    """Test an invalid author."""
    with pytest.raises(
        ValueError, match="Author name must be between 2 and 100 characters."
    ):
        validate_author("j")  # Too short

    with pytest.raises(
        ValueError,
        match="Author name can only contain letters, spaces, dashes, commas, periods, and Finnish characters.",
    ):
        validate_author("Joulupukki123")  # Contains invalid characters


def test_validate_title_valid():
    """Test a valid title."""
    assert (
        validate_title("Toimitusketjujen optimointi") is None
    )  # Should pass without error


def test_validate_title_with_finnish_characters_valid():
    """Test a valid title."""
    assert (
        validate_title("Ääkköstitle: Plussana ruotsalainen Å") is None
    )  # Should pass without error


def test_validate_title_invalid():
    """Test an invalid title."""
    with pytest.raises(ValueError, match="Title contains invalid characters."):
        validate_title("Bad<script>alert('XSS')</script>")

    with pytest.raises(ValueError, match="Title must be between 5 and 255 characters."):
        validate_title("Ab")  # Too short


def test_validate_journal_valid():
    """Test a valid journal."""
    assert validate_journal("Joulutiede Journal") is None  # Should pass without error


def test_validate_journal_invalid():
    """Test an invalid journal."""
    with pytest.raises(ValueError, match="Journal name contains invalid characters."):
        validate_journal("Journal|Name")  # Contains invalid character '|'

    with pytest.raises(
        ValueError, match="Journal must be between 2 and 255 characters."
    ):
        validate_journal("J")  # Too short


def test_validate_year_valid():
    """Test a valid year."""
    assert validate_year("2023") is None  # Should pass without error


def test_validate_year_invalid():
    """Test an invalid year."""
    with pytest.raises(
        ValueError, match="Year must be a valid number between 0 and 2100."
    ):
        validate_year("abcd")  # Non-numeric


def test_validate_doi_valid():
    """Test a valid DOI."""
    assert validate_doi("10.1234/example-doi") is None  # Should pass without error


def test_validate_doi_invalid():
    """Test an invalid DOI."""
    with pytest.raises(ValueError, match="DOI must follow the format '10.xxxx/xxxxx'."):
        validate_doi("invalid-doi")  # Wrong format


def test_validate_month_valid():
    """Test a valid month"""
    assert validate_month("January") is None  # Should pass without error


def test_validate_month_invalid():
    """Test an invalid month."""
    with pytest.raises(ValueError, match="Month must be a valid name or abbreviation."):
        validate_month("Dokember")  # Invalid month input


def test_validate_month_missing():
    """Test an invalid month."""
    with pytest.raises(ValueError, match="Month must be a valid name or abbreviation."):
        validate_month("")  # Missing month input


def test_validate_pages_short_dash_valid():
    """Test a valid pages input with a short dash."""
    assert validate_pages("451-475") is None  # Should pass without error


def test_validate_pages_long_dash_valid():
    """Test a valid pages input with a long dash."""
    assert validate_pages("451–475") is None  # Should pass without error


def test_validate_pages_single_number_valid():
    """Test a valid single number pages input."""
    assert validate_pages("0") is None  # Should pass without error


def test_validate_pages_invalid():
    """Test an invalid pages input."""
    with pytest.raises(
        ValueError,
        match=re.escape("Pages must be a number or range (e.g., '1-10' or '1–10')."),
    ):
        validate_pages("OHO–HUPS")  # Invalid page range input


def test_validate_pages_single_number_invalid():
    """Test an invalid single number pages input."""
    with pytest.raises(
        ValueError,
        match=re.escape("Pages must be a number or range (e.g., '1-10' or '1–10')."),
    ):
        validate_pages("-1")  # Invalid page range input


def test_validate_common_pattern_valid_finnish():
    """Test valid Finnish inputs."""
    assert (
        validate_common_pattern("Tämä on testi!", "Test Input") is None
    )  # Valid with Finnish characters
    assert (
        validate_common_pattern("Ääkköset Överissä Ålandissa", "Test Input") is None
    )  # Valid mixed case
    assert (
        validate_common_pattern("12345 äöåÄÖÅ?!,.-@", "Test Input") is None
    )  # Valid with numbers and symbols
    assert (
        validate_common_pattern("Hello, World!", "Test Input") is None
    )  # Valid simple input
    assert (
        validate_common_pattern("Valid input 123.", "Test Input") is None
    )  # Valid input with numbers


def test_validate_common_pattern_invalid_characters():
    """Test invalid inputs with unsupported characters."""

    with pytest.raises(
        ValueError,
        match=re.escape("Test Input contains invalid characters."),
    ):
        validate_common_pattern(
            "Invalid字符", "Test Input"
        )  # Invalid non-Latin characters

    with pytest.raises(
        ValueError,
        match=re.escape("Test Input contains invalid characters."),
    ):
        validate_common_pattern("Invalid<>[]{}", "Test Input")  # Invalid symbols

    with pytest.raises(
        ValueError,
        match=re.escape("Test Input contains invalid characters."),
    ):
        validate_common_pattern("💡", "Test Input")  # Invalid emoji


def test_validate_common_pattern_edge_cases():
    """Test edge cases for valid and invalid inputs."""
    with pytest.raises(
        ValueError,
        match=re.escape("Test Input contains invalid characters."),
    ):
        validate_common_pattern("", "Test Input")  # Empty string (invalid)
    assert validate_common_pattern(" ", "Test Input") is None  # Space only (valid)

    with pytest.raises(
        ValueError,
        match=re.escape("Test Input contains invalid characters."),
    ):
        validate_common_pattern("\n", "Test Input")  # Invalid newline character
