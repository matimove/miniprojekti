from repositories import (
    article_repository,
    book_repository,
    inproceedings_repository,
    misc_repository,
)


class ReferenceService:
    def __init__(self):
        self.references = []

    def add_references(self):
        articles = article_repository.get_articles()
        books = book_repository.get_books()
        inproceedings = inproceedings_repository.get_inproceedings()
        misc = misc_repository.get_misc()

        self.references = self.references + articles + books + inproceedings + misc

    def sort_references_by_title(self):
        self.references.sort(key=lambda ref: (ref.title, ref.author))

        return self.references
