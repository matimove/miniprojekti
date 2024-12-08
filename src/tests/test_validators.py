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
    validate_field,
    validate_name,
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

    with pytest.raises(ValueError, match="Title must be between 5 and 255 characters."):
        validate_title("B" * 256)  # Too long


def test_validate_journal_valid():
    """Test a valid journal."""
    assert validate_journal("Joulutiede Journal") is None  # Should pass without error


def test_validate_journal_invalid():
    """Test an invalid journal."""
    with pytest.raises(ValueError, match="Journal contains invalid characters."):
        validate_journal("Journal|Name")  # Contains invalid character '|'

    with pytest.raises(
        ValueError, match="Journal must be between 2 and 255 characters."
    ):
        validate_journal("J")  # Too short

    with pytest.raises(
        ValueError, match="Journal must be between 2 and 255 characters."
    ):
        validate_journal("A" * 256)  # Too long


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


def test_validate_field_valid_inputs():
    """Test valid inputs for validate_field."""
    # Valid general inputs
    assert validate_field("Hello World!", "Test Field") is None
    assert validate_field("Ääkköset Överissä Ålandissa", "Test Field") is None
    assert validate_field("12345 äöåÄÖÅ?!,.-@", "Test Field") is None
    assert (
        validate_field("Simple title", "Test Field", min_length=5, max_length=20)
        is None
    )
    assert (
        validate_field("1", "Test Field", min_length=1, max_length=255) is None
    )  # Minimum valid length


def test_validate_field_invalid_inputs():
    """Test invalid inputs for validate_field."""
    # Test empty input when not allowed
    with pytest.raises(
        ValueError,
        match=re.escape("Test Field must be between 1 and 255 characters."),
    ):
        validate_field("", "Test Field")  # Empty input is not valid by default

    # Test too short
    with pytest.raises(
        ValueError,
        match=re.escape("Test Field must be between 5 and 10 characters."),
    ):
        validate_field("Hi", "Test Field", min_length=5, max_length=10)

    # Test too long
    with pytest.raises(
        ValueError,
        match=re.escape("Test Field must be between 5 and 10 characters."),
    ):
        validate_field(
            "This is way too long", "Test Field", min_length=5, max_length=10
        )

    # Test invalid characters
    with pytest.raises(
        ValueError,
        match=re.escape("Test Field contains invalid characters."),
    ):
        validate_field("Invalid 🚀 input", "Test Field")  # Emoji is not allowed

    with pytest.raises(
        ValueError,
        match=re.escape("Test Field contains invalid characters."),
    ):
        validate_field("Invalid<>[]{}", "Test Field")  # Disallowed symbols


def test_validate_field_edge_cases():
    """Test edge cases for validate_field."""
    # Test exact boundary conditions
    assert (
        validate_field("Valid", "Test Field", min_length=5, max_length=5) is None
    )  # Exact length match

    # Input with only whitespace
    with pytest.raises(
        ValueError,
        match=re.escape("Test Field must be between 1 and 255 characters."),
    ):
        validate_field("    ", "Test Field")  # Whitespace-only is invalid

    # Large input at upper boundary
    large_input = "a" * 255
    assert (
        validate_field(large_input, "Test Field", min_length=1, max_length=255) is None
    )  # Valid upper boundary
    with pytest.raises(
        ValueError,
        match=re.escape("Test Field must be between 1 and 255 characters."),
    ):
        validate_field(
            large_input + "a", "Test Field", min_length=1, max_length=255
        )  # Exceeds upper boundary


def test_validate_name_valid_inputs():
    """Test valid name inputs."""
    # Simple names
    assert validate_name("John", "Name") is None
    assert validate_name("Matti Meikäläinen", "Name") is None  # Finnish characters
    assert validate_name("Åke Öberg", "Name") is None  # Finnish characters with spaces
    assert validate_name("Anne-Marie", "Name") is None  # Name with dash
    assert (
        validate_name("Dr. John Smith", "Name") is None
    )  # Name with periods and spaces
    assert validate_name("Smith, John", "Name") is None  # Name with commas

    # Boundary cases
    assert (
        validate_name("AB", "Name", min_length=2, max_length=100) is None
    )  # Minimum valid length
    assert (
        validate_name("A" * 100, "Name", min_length=2, max_length=100) is None
    )  # Maximum valid length


def test_validate_name_invalid_inputs():
    """Test invalid name inputs."""
    # Too short, default values
    with pytest.raises(
        ValueError,
        match=re.escape("Name must be between 2 and 100 characters."),
    ):
        validate_name("t", "Name")

    # Too short
    with pytest.raises(
        ValueError,
        match=re.escape("Name must be between 5 and 20 characters."),
    ):
        validate_name("Ann", "Name", min_length=5, max_length=20)

    # Too long
    with pytest.raises(
        ValueError,
        match=re.escape("Name must be between 5 and 20 characters."),
    ):
        validate_name("A" * 21, "Name", min_length=5, max_length=20)

    # Invalid characters
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Name can only contain letters, spaces, dashes, commas, periods, and Finnish characters."
        ),
    ):
        validate_name("Invalid123", "Name")  # Numbers not allowed

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Name can only contain letters, spaces, dashes, commas, periods, and Finnish characters."
        ),
    ):
        validate_name("Invalid@Name", "Name")  # Disallowed symbol

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Name can only contain letters, spaces, dashes, commas, periods, and Finnish characters."
        ),
    ):
        validate_name("🚀", "Name")  # Emoji not allowed


def test_validate_name_edge_cases():
    """Test edge cases for validate_name."""
    # Names with leading/trailing spaces
    assert (
        validate_name("  John Smith  ", "Name") is None
    )  # Leading/trailing spaces should be stripped

    # Name with special characters in Finnish
    assert (
        validate_name("Ääliö Östman Åström", "Name") is None
    )  # Fully valid Finnish characters

    # Exact boundary lengths
    assert (
        validate_name("A" * 2, "Name", min_length=2, max_length=2) is None
    )  # Minimum length exact
    assert (
        validate_name("A" * 100, "Name", min_length=2, max_length=100) is None
    )  # Maximum length exact
