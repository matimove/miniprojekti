import urllib.request
from urllib.error import HTTPError, URLError
import bibtexparser
from validators import validate_doi
from services.citation_service import UserInputError
from flask import flash


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
        if not bib_database.entries:
            flash("No entries found in BibTeX response.", "error")
        entry = bib_database.entries[0]
        return entry
    except HTTPError as e:
        if e.code == 404:
            flash(str(e), "error")
        else:
            raise ConnectionError(
                flash("HTTP error occurred: {e.code}. Please try again later.", "error")
            ) from e
    except URLError as e:
        flash(
            f"Network error occurred: {e.reason}. Please check your connection.",
            "error",
        )
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", "error")
