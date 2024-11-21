from repositories import article_repository
from validators import (
    validate_required_field,
    validate_numeric,
    validate_year,
    validate_author,
    validate_title,
    validate_journal,
    validate_doi,
    validate_pages,
    validate_month
)

class UserInputError(Exception):
    """Custom exception for user input validation errors."""
    pass

def validate_article(author, title, journal, year, volume=None, number=None, pages=None, month=None, doi=None):
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
        if doi:
            validate_doi(doi)
        
        # Delegate to repository for database operations
        return article_repository.create_article(
            author=author,
            title=title,
            journal=journal,
            year=year,
            volume=volume,
            number=number,
            pages=pages,
            month=month,
            doi=doi
        )
    
    except ValueError as e:
        raise UserInputError(str(e))
