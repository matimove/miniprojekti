from repositories import misc_repository
from validators import (
    validate_required_field,
    validate_year,
    validate_author,
    validate_title,
    validate_month,
    validate_howpublished,
    validate_common_pattern
)

class UserInputError(Exception):
    """Custom exception for user input validation errors."""
    pass

def validate_misc(author, title, year, month=None, howpublished=None, note=None):


    """
        Parameters:
        author (str): Author's name.
        title (str): Title of the article.
        year (str): Year of publication.
        month (str, optional): Month of publication.
        howpublished (str, optional): How published.
        note (str, optional): Note.
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

        validate_required_field(year, "Year")
        validate_year(year)

        # Validate optional fields
        if howpublished:
            validate_howpublished(howpublished) 
        if note: 
            validate_common_pattern(note, "Note")
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

        # Delegate to repository for database operations
        return misc_repository.create_misc(
            author = author,
            title = title,
            year = year,
            month = month,
            note = note,
            howpublished = howpublished
        )


    except ValueError as e: 
        raise UserInputError(str(e))

