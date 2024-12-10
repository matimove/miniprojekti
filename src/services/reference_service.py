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

    def sort_by_primary_and_secondary_key(
        self, primary="title", secondary="author", reverse=False
    ):
        self.references.sort(
            key=lambda ref: (
                (
                    getattr(ref, primary).lower()
                    if isinstance(getattr(ref, primary), str)
                    else getattr(ref, primary)
                ),
                (
                    getattr(ref, secondary).lower()
                    if isinstance(getattr(ref, secondary), str)
                    else getattr(ref, secondary)
                ),
            ),
            reverse=reverse,
        )

        return self.references

    def get_reverse(self, order):
        return True if order == "desc" else False

    def search_with_keyword(self, search):
        search = search.lower().strip()
        result = filter(
            lambda ref: search in ref.title.lower()
            or search == str(ref.year)
            or search in ref.author.lower(),
            self.references,
        )
        return list(result)
