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
        print(misc)

        self.references = self.references + articles + books + inproceedings + misc

    def sort_references_by_title(self):
        # secondary sort by author
        self.references.sort(key=lambda ref: (ref.title.lower(), ref.author.lower()))

        return self.references

    def sort_references_by_author(self):
        # secondary sort by title
        self.references.sort(key=lambda ref: (ref.author.lower(), ref.title.lower()))

        return self.references

    def sort_references_by_year(self):
        # secondary sort by author
        self.references.sort(key=lambda ref: (ref.year, ref.author.lower()))

        return self.references

    def search_with_keyword(self, search):
        search = search.lower()
        result = filter(lambda ref: search in ref.title.lower() or search ==
                            str(ref.year) or search in ref.author.lower(),
                            self.references)
        return list(result)
