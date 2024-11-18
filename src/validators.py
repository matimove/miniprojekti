import re

def validate_required_field(value, field_name):
    """Ensures that a required field is not empty or just whitespace."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} is required.")

def validate_length(value, field_name, min_length, max_length):
    """Validates the length of a string."""
    if len(value.strip()) < min_length or len(value.strip()) > max_length:
        raise ValueError(f"{field_name} must be between {min_length} and {max_length} characters.")

def validate_numeric(value, field_name):
    """Validates that a value is numeric."""
    if not str(value).isdigit():
        raise ValueError(f"{field_name} must be a valid number.")

def validate_year(year):
    """Validates that the year is numeric and within a realistic range."""
    if not year.isdigit() or not (1500 <= int(year) <= 2100):
        raise ValueError("Year must be a valid number between 1500 and 2100.")

def validate_author(author):
    """Validates an author's name (letters, spaces, and dashes)."""
    pattern = r"^[a-zA-Z\- ]+$"
    if not re.match(pattern, author):
        raise ValueError("Author name can only contain letters, spaces, and dashes.")
    validate_length(author, "Author name", 2, 100)

def validate_title(title):
    """Validates an article title (letters, numbers, spaces, and punctuation)."""
    validate_length(title, "Title", 5, 255)
    pattern = r"^[a-zA-Z0-9 .,\-?!:;'()\"@]+$"
    if not re.match(pattern, title):
        raise ValueError("Title contains invalid characters.")

def validate_journal(journal):
    """Validates a journal name (letters, numbers, spaces, and punctuation)."""
    validate_required_field(journal, "Journal")
    validate_length(journal, "Journal", 2, 255)
    pattern = r"^[a-zA-Z0-9 .,\-:]+$"
    if not re.match(pattern, journal):
        raise ValueError("Journal name contains invalid characters.")

def validate_doi(doi):
    """Validates a DOI (Digital Object Identifier)."""
    pattern = r"^10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$"
    if not re.match(pattern, doi):
        raise ValueError("DOI must follow the format '10.xxxx/xxxxx'.")

def validate_pages(pages):
    """Validates page ranges (e.g., '1-10', '5', or '1-5, 10-15')."""
    pattern = r"^(\d+(-\d+)?)(,\s*\d+(-\d+)?)*$"
    if not re.match(pattern, pages):
        raise ValueError("Pages must be a number or range (e.g., '1-10').")

def validate_month(month):
    """Validates a month (numeric 1-12 or a full/abbreviated name)."""
    valid_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
        "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    if month.isdigit() and not (1 <= int(month) <= 12):
        raise ValueError("Month must be a valid number (1-12).")
    elif month.capitalize() not in valid_months:
        raise ValueError("Month must be a valid name or abbreviation.")
