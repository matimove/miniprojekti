from repositories import book_repository
from validators import (
    validate_required_field,
    validate_numeric,
    validate_year,
    validate_author,
    validate_title,
    validate_doi,
    validate_pages,
    validate_publisher
)

class UserInputError(Exception):
    """Custom exception for user input validation errors."""
    pass

    """
    Parameters:
        author (str): Author's name.
        title (str): Title of the article.
        year (str): Year of publication.
        publisher (str): Publisher name.
        edition (str, optional): Addredd.
        pages (str, optional): Page range.
        doi (str, optional): Digital Object Identifier.
    """


def validate_book(author, title, year, publisher=None, edition=None, pages=None, doi=None):
    
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

        return book_repository.create_book(
            author=author,
            title=title,
            publisher=publisher,
            year=year,
            edition=edition,
            pages=pages,
            doi=doi
        )

    except ValueError as e:
        raise UserInputError(str(e))
