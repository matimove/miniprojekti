import urllib.request
from urllib.error import HTTPError
import bibtexparser
from validators import validate_doi
from services.citation_service import UserInputError


def get_bibtex_with_doi(doi):
    BASE_URL = "http://dx.doi.org/"

    try:
        validate_doi(doi)
        print(doi)
    except ValueError as e:
        raise UserInputError(str(e)) from e

    url = BASE_URL + doi
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/x-bibtex")

    try:
        with urllib.request.urlopen(req, timeout=10) as f:
            bibtex = f.read().decode()

        bib_database = bibtexparser.loads(bibtex)
        # Extract the entry
        entry = bib_database.entries[0]
        print(entry)
        return entry

    except HTTPError as e:
        if e.code == 404:
            raise "DOI not found."
        else:
            raise "Service unavailable. Try again"
