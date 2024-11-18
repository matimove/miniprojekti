import pytest
from validators import (
    validate_author,
    validate_title,
    validate_journal,
    validate_year,
    validate_doi
)

def test_validate_author_valid():
    assert validate_author("Anne-Marie") is None  # Should pass without error

def test_validate_author_invalid():
    with pytest.raises(ValueError, match="Author name can only contain letters, spaces, and dashes."):
        validate_author("123InvalidName")

def test_validate_title_valid():
    assert validate_title("The Impact of AI on Society") is None

def test_validate_title_invalid():
    with pytest.raises(ValueError, match="Title contains invalid characters."):
        validate_title("Bad <script>Title</script>")

def test_validate_journal_valid():
    assert validate_journal("Nature") is None

def test_validate_journal_invalid():
    with pytest.raises(ValueError, match="Journal name contains invalid characters."):
        validate_journal("Journal|With|Pipes")

def test_validate_year_valid():
    assert validate_year("2023") is None

def test_validate_year_invalid():
    with pytest.raises(ValueError, match="Year must be a valid number between 1500 and 2100."):
        validate_year("abcd")

def test_validate_doi_valid():
    assert validate_doi("10.1234/example-doi") is None

def test_validate_doi_invalid():
    with pytest.raises(ValueError, match="DOI must follow the format '10.xxxx/xxxxx'."):
        validate_doi("invalid-doi")
