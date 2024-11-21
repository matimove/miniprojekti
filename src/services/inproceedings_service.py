from repositories import inproceedings_repository
from validators import (
    validate_required_field,
    validate_numeric,
    validate_author,
    validate_title,
    validate_year,
    validate_pages,
    validate_month,
)

class UserInputError(Exception):
    """Custom exception for user input validation errors."""
    pass

def validate_inproceedings(author, title, booktitle, year, editor=None, volume=None, number=None, series=None, pages=None, address=None, month=None, organization=None, publisher=None):
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

    Raises:
        UserInputError: If any field fails validation.

    Returns:
        int: The ID of the created article.
    """
    try:
        # Month mapping for numeric and abbreviated month inputs
        month_mapping = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December",
            "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
            "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
            "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"
        }

        # Validate required fields
        validate_required_field(author, "Author")
        validate_author(author)
        
        validate_required_field(title, "Title")
        validate_title(title)
        
        validate_required_field(booktitle, "Booktitle")
        validate_title(booktitle)
        
        validate_required_field(year, "Year")
        validate_year(year)
        
        # Validate optional fields
        if editor:
            validate_author(editor)
        if volume:
            validate_numeric(volume, "Volume")
        if number:
            validate_numeric(number, "Issue")
        if series:
            validate_title(series)
        if pages:
            validate_pages(pages)
        if address:
            validate_title(address)
        if month:
            # Normalize month input
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
            
            validate_month(month)  # Validate the normalized month
        
        if organization:
            validate_title(organization)
        if publisher:
            validate_title(publisher)

        # Delegate to repository for database operations
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
            publisher=publisher
        )
    
    except ValueError as e:
        raise UserInputError(str(e))
