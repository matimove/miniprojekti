from repositories import (
    article_repository,
    inproceedings_repository,
    book_repository,
    misc_repository,
)
from validators import (
    validate_required_field,
    validate_numeric,
    validate_year,
    validate_author,
    validate_title,
    validate_journal,
    validate_doi,
    validate_pages,
    validate_month,
    validate_publisher,
    validate_booktitle,
    validate_editor,
    validate_series,
    validate_address,
    validate_organization,
    validate_howpublished,
    validate_common_pattern,
)


class UserInputError(Exception):
    """Custom exception for user input validation errors."""

    pass


class KeyGenerationError(Exception):
    """Custom exception for key generation errors."""

    pass


def normalize_month_input(month):
    month_mapping = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December",
    }

    if month.isdigit():
        # If month input is numeric, convert into corresponding month
        month_num = int(month)
        if 1 <= month_num <= 12:
            month = month_mapping[month_num]
        else:
            raise ValueError("Numeric month input must be between 1 and 12.")
    elif month in month_mapping:
        # If month input is abbreviated, convert into corresponding month
        month = month_mapping[month]
    elif month.capitalize() in month_mapping.values():
        # If month input is full month name, normalize capitalization
        month = month.capitalize()
    else:
        raise ValueError("Month must be a valid name or abbreviation.")

    return month


def is_key_unique(key):
    """
    Checks if a given citation key is unique across all citation types.

    Parameters:
        key (str): The citation key to check.

    Returns:
        bool: True if the key is unique, False otherwise.
    """
    # Check in articles
    if article_repository.is_key_unique(key) is False:
        return False

    # Check in inproceedings
    if inproceedings_repository.is_key_unique(key) is False:
        return False

    # Check in books
    if book_repository.is_key_unique(key) is False:
        return False

    # Check in misc
    if misc_repository.is_key_unique(key) is False:
        return False

    return True


def generate_citation_key(author, year):
    """
    Generates a citation key based on the first author's initials and the year.

    Parameters:
        author (str): The author string (e.g., "John Doe and Jane Smith" or "John Doe, Jane Smith").
        year (str): The year of publication.

    Returns:
        str: A generated citation key (e.g., "JDoe2023" or "Joulupukki2023").
    """
    if not author or not year:
        raise UserInputError("Author and year are required to generate a citation key.")

    # Split authors using both "and" and "," as separators
    first_author = author.split(" and ")[0].split(",")[0].strip()
    names = first_author.split()

    if len(names) == 1:
        # Handle single-word names like "Joulupukki"
        base_key = f"{names[0].capitalize()}{year}"
    elif len(names) > 1:
        # Handle standard first and last name cases
        first_initial = names[0][0].upper()
        last_name = names[-1].capitalize()
        base_key = f"{first_initial}{last_name}{year}"

    # Ensure the key is unique by querying all repositories
    unique_key = base_key
    suffix = 1
    while not is_key_unique(unique_key):
        if suffix <= 26:
            unique_key = f"{base_key}{chr(96 + suffix)}"  # Append 'a', 'b', 'c', ...
        else:
            unique_key = f"{base_key}_{suffix}"  # Append numeric suffix
        suffix += 1

    return unique_key


def validate_article(
    author,
    title,
    journal,
    year,
    volume=None,
    number=None,
    pages=None,
    month=None,
    doi=None,
    key=None,
):
    """
    Validates an article's input fields and delegates creation to the repository.

    Parameters:
        author (str): Author's name.
        title (str): Title of the article.
        journal (str): Journal name.
        year (str): Year of publication.
        volume (str, optional): Volume number.
        number (str, optional): Issue number.
        pages (str, optional): Page range.
        month (str, optional): Month of publication.
        doi (str, optional): Digital Object Identifier.
        key (str, optional): User-provided citation key.

    Raises:
        UserInputError: If any field fails validation.

    Returns:
        int: The ID of the created article.
    """
    try:
        # Validate required fields
        validate_required_field(author, "Author")
        validate_author(author)

        validate_required_field(title, "Title")
        validate_title(title)

        validate_required_field(journal, "Journal")
        validate_journal(journal)

        validate_required_field(year, "Year")
        validate_year(year)

        # Validate optional fields
        if volume:
            validate_numeric(volume, "Volume")
        if number:
            validate_numeric(number, "Issue")
        if pages:
            validate_pages(pages)
        if month:
            month = normalize_month_input(month)
            validate_month(month)
        if doi:
            validate_doi(doi)

        if not key or not is_key_unique(key):
            key = generate_citation_key(author, year)

        return article_repository.create_article(
            author=author,
            title=title,
            journal=journal,
            year=year,
            volume=volume,
            number=number,
            pages=pages,
            month=month,
            doi=doi,
            key=key,
        )

    except ValueError as e:
        raise UserInputError(str(e)) from e


def validate_inproceedings(
    author,
    title,
    booktitle,
    year,
    editor=None,
    volume=None,
    number=None,
    series=None,
    pages=None,
    address=None,
    month=None,
    organization=None,
    publisher=None,
    key=None,
):
    """
    Validates an inproceedings's input fields and delegates creation to the repository.

    Parameters:
        author (str): Author(s) of the paper.
        title (str): Title of the paper.
        booktitle (str): Title of the conference proceedings.
        year (int): Year of publication.
        editor (str, optional): Name(s) of the editor(s).
        volume (str, optional): Volume number.
        number (str, optional): Issue number.
        series (str, optional): Name of conference proceedings.
        pages (str, optional): Page range.
        address (str, optional): Location of the conference.
        month (str, optional): The month the conference was held.
        organization (str, optional): Sponsor organization of the conference proceedings.
        publisher (str, optional): Publisher of the conference proceedings.
        key (str, optional): User-provided citation key.

    Raises:
        UserInputError: If any field fails validation.

    Returns:
        int: The ID of the created inproceedings.
    """
    try:
        # Validate required fields
        validate_required_field(author, "Author")
        validate_author(author)

        validate_required_field(title, "Title")
        validate_title(title)

        validate_required_field(booktitle, "Booktitle")
        validate_booktitle(booktitle)

        validate_required_field(year, "Year")
        validate_year(year)

        # Validate optional fields
        if editor:
            validate_editor(editor)
        if volume:
            validate_numeric(volume, "Volume")
        if number:
            validate_numeric(number, "Issue")
        if series:
            validate_series(series)
        if pages:
            validate_pages(pages)
        if address:
            validate_address(address)
        if month:
            month = normalize_month_input(month)
            validate_month(month)

        if organization:
            validate_organization(organization)
        if publisher:
            validate_publisher(publisher)

        if not key or not is_key_unique(key):
            key = generate_citation_key(author, year)

        return inproceedings_repository.create_inproceedings(
            author=author,
            title=title,
            booktitle=booktitle,
            year=year,
            editor=editor,
            volume=volume,
            number=number,
            series=series,
            pages=pages,
            address=address,
            month=month,
            organization=organization,
            publisher=publisher,
            key=key,
        )

    except ValueError as e:
        raise UserInputError(str(e)) from e


def validate_book(
    author, title, year, publisher=None, edition=None, pages=None, doi=None, key=None
):
    """
    Parameters:
        author (str): Author's name.
        title (str): Title of the article.
        year (str): Year of publication.
        publisher (str): Publisher name.
        edition (str, optional): Addredd.
        pages (str, optional): Page range.
        doi (str, optional): Digital Object Identifier.
        key (str, optional): User-provided citation key.

    Raises:
        UserInputError: If any field fails validation.

    Returns:
        int: The ID of the created book.
    """
    try:
        validate_required_field(author, "Author")
        validate_author(author)

        validate_required_field(title, "Title")
        validate_title(title)

        validate_required_field(year, "Year")
        validate_year(year)

        if publisher:
            validate_publisher(publisher)
        if edition:
            validate_numeric(edition, "Edition")
        if pages:
            validate_pages(pages)
        if doi:
            validate_doi(doi)

        if not key or not is_key_unique(key):
            key = generate_citation_key(author, year)

        return book_repository.create_book(
            author=author,
            title=title,
            publisher=publisher,
            year=year,
            edition=edition,
            pages=pages,
            doi=doi,
            key=key,
        )

    except ValueError as e:
        raise UserInputError(str(e)) from e


def validate_misc(
    author, title, year, month=None, howpublished=None, note=None, key=None
):
    """
    Parameters:
        author (str): Author's name.
        title (str): Title of the article.
        year (str): Year of publication.
        month (str, optional): Month of publication.
        howpublished (str, optional): How published.
        key (str, optional): User-provided citation key.

    Raises:
        UserInputError: If any field fails validation.

    Returns:
        int: The ID of the created misc.
    """

    try:
        # Validate required fields
        validate_required_field(author, "Author")
        validate_author(author)

        validate_required_field(title, "Title")
        validate_title(title)

        validate_required_field(year, "Year")
        validate_year(year)

        # Validate optional fields
        if howpublished:
            validate_howpublished(howpublished)
        if note:
            validate_common_pattern(note, "Note")
        if month:
            month = normalize_month_input(month)
            validate_month(month)

        if not key or not is_key_unique(key):
            key = generate_citation_key(author, year)

        return misc_repository.create_misc(
            author=author,
            title=title,
            year=year,
            month=month,
            note=note,
            howpublished=howpublished,
            key=key,
        )

    except ValueError as e:
        raise UserInputError(str(e)) from e
