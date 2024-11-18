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
            validate_month(month)
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
