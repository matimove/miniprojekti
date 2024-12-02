from pybtex.database import BibliographyData, Entry


class BibtexService:
    def __init__(self):
        pass

    def generate_bibtex_all(self, references):
        entries = {}
        for i, reference in enumerate(references):
            entry_key = str(i)
            if reference.category == "article":
                entry = self.create_entry_article(reference)
            elif reference.category == "book":
                entry = self.create_entry_book(reference) 
            elif reference.category == "inproceedings":
                entry = self.create_entry_inproceedings(reference)
            elif reference.category == "misc":
                entry = self.create_entry_misc(reference)
            else:
                break
            entries[entry_key] = entry
        bib_data = BibliographyData(entries)
        print(bib_data.to_string("bibtex"))

    def _clean_fields(self, fields):
        return {k: v for k, v in fields.items() if v is not None}

    def create_entry_article(self, article):
        fields = {
            "author": article.author,
            "title": article.title,
            "year": str(article.year),
            "journal": article.journal,
            "volume": str(article.volume) if article.volume else None,
            "number": str(article.number) if article.number else None,
            "pages": article.pages,
            "month": article.month,
            "doi": article.doi,
        }
        entry = Entry(article.category, fields=self._clean_fields(fields))
        return entry
    
    def create_entry_book(self, book):
        fields = {
            "author": book.author,
            "title": book.title,
            "year": str(book.year),
            "publisher": book.publisher,
            "edition": str(book.edition) if book.edition else None,
            "pages": book.pages,
            "doi": book.doi,
        }
        entry = Entry(book.category, fields=self._clean_fields(fields))
        return entry
    
    def create_entry_inproceedings(self, inproceedings):
        pass

    def create_entry_misc(self, misc):
        pass
