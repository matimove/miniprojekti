from repositories import article_repository

class UserInputError(Exception):
    pass

def validate(author, title, journal, year, volume, number, pages, month, doi):
    if not (author and title and journal and year):
        raise UserInputError("Author, title, journal, and year are required fields")

    if not year.isdigit():
        raise UserInputError("Year value can only contain numbers")

    return article_repository.create_article(author, title, journal, year, volume, number, pages, month, doi)
