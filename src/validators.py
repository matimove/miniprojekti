import re


def validate_required_field(value, field_name):
    """Ensures that a required field is not empty or just whitespace."""
    if not value or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"{field_name} is required.")


def validate_length(value, field_name, min_length, max_length):
    """Validates the length of a string."""
    if len(value.strip()) < min_length or len(value.strip()) > max_length:
        raise ValueError(
            f"{field_name} must be between {min_length} and {max_length} characters."
        )


def validate_numeric(value, field_name):
    """Validates that a value is numeric."""
    if not str(value).isdigit():
        raise ValueError(f"{field_name} must be a valid number.")


def validate_common_pattern(string, name):
    """Validates that a given string only contains Finnish letters, numbers, spaces, and punctuation."""
    pattern = r"^[a-zA-Z0-9 äöåÄÖÅ.,\-?!:;'()\"@]+$"
    if not re.match(pattern, string):
        raise ValueError(f"{name} contains invalid characters.")


def validate_field(value, field_name, min_length=1, max_length=255):
    """
    General-purpose validator for fields with Finnish letters, numbers, spaces, and punctuation.
    Handles both length and character checks. Default min length is 1, default max length is 255.
    """
    validate_length(value, field_name, min_length, max_length)
    validate_common_pattern(value, field_name)


def validate_name(name, field_name, min_length=2, max_length=100):
    """
    Validates name(s) (Finnish letters, spaces, dashes, commas, and periods).
    Default min length is 2, default max length is 100.
    """
    pattern = r"^[a-zA-Z äöåÄÖÅ.,\- ]+$"
    if not re.match(pattern, name):
        raise ValueError(
            f"{field_name} can only contain letters, spaces, dashes, commas, periods, and Finnish characters."
        )
    validate_length(name, field_name, min_length, max_length)


def validate_year(year):
    """Validates that the year is numeric and within a realistic range (0-2100)."""
    try:
        year = int(year)
        if not 0 <= year <= 2100:
            raise ValueError
    except (ValueError, TypeError) as e:
        raise ValueError("Year must be a valid number between 0 and 2100.") from e


def validate_author(author):
    """Validates author name(s)."""
    validate_name(author, "Author name")


def validate_editor(editor):
    """Validates editor name(s)."""
    validate_name(editor, "Editor name")


def validate_title(title):
    """Validates a title (Finnish letters, numbers, spaces, and punctuation)."""
    validate_field(title, "Title", min_length=5)


def validate_journal(journal):
    """Validates a journal name (Finnish letters, numbers, spaces, and punctuation)."""
    validate_field(journal, "Journal", min_length=2)


def validate_doi(doi):
    """Validates a DOI (Digital Object Identifier)."""
    pattern = r"^10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$"
    if not re.match(pattern, doi):
        raise ValueError("DOI must follow the format '10.xxxx/xxxxx'.")


def validate_pages(pages):
    """Validates page ranges (e.g., '1-10', '5', or '1-5, 10-15')
    with support for both short ('-') and long ('–') dashes."""
    pattern = r"^(\d+([-\u2013]\d+)?)(,\s*\d+([-\u2013]\d+)?)*$"
    if not re.match(pattern, pages):
        raise ValueError("Pages must be a number or range (e.g., '1-10' or '1–10').")


def validate_month(month):
    """Validates a month (numeric 1-12 or a full/abbreviated name)."""
    valid_months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    if month.capitalize() not in valid_months:
        raise ValueError("Month must be a valid name or abbreviation.")


def validate_booktitle(booktitle):
    """Validates a booktitle (Finnish letters, numbers, spaces, and punctuation)."""
    validate_field(booktitle, "Booktitle")


def validate_series(series):
    """Validates a series name (Finnish letters, numbers, spaces, and punctuation)."""
    validate_field(series, "Series")


def validate_address(address):
    """Validates an address (Finnish letters, numbers, spaces, and punctuation)."""
    validate_field(address, "Address")


def validate_organization(organization):
    """Validates an organization name (Finnish letters, numbers, spaces, and punctuation)."""
    validate_field(organization, "Organization")


def validate_publisher(publisher):
    """Validates a publisher name (Finnish letters, numbers, spaces, and punctuation)."""
    validate_field(publisher, "Publisher")


def validate_howpublished(howpublished):
    validate_field(howpublished, "How Published")


def validate_note(note):
    validate_field(note, "Note")
