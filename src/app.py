from flask import flash, jsonify, redirect, render_template, request, url_for

from config import app, test_env
from db_helper import reset_db
from forms import (
    AddArticleForm,
    AddBookForm,
    AddInproceedingsForm,
    AddMiscForm,
    SearchForm,
)
from repositories import (
    article_repository,
    book_repository,
    inproceedings_repository,
    misc_repository,
)
from services.citation_service import (
    UserInputError,
    validate_article,
    validate_book,
    validate_inproceedings,
    validate_misc,
)
from services.reference_service import ReferenceService
from services.bibtex_service import BibtexService

class DeletionError(Exception):
    """Custom exception for citation deletion operations."""

    pass


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    # Possibly could be called at start once to avoid unnecessary database calls
    reference_service = ReferenceService()
    reference_service.add_references()

    if not reference_service.references:
        message_references = "You have no references saved"
    else:
        message_references = None

    sort_by = request.args.get("sort_by", "title")

    if sort_by == "title":
        reference_service.sort_references_by_title()
    elif sort_by == "author":
        reference_service.sort_references_by_author()
    elif sort_by == "year":
        reference_service.sort_references_by_year()

    if form.validate_on_submit():
        search = form.search.data
        return redirect(url_for("search_citations", search=search))

    return render_template(
        "index.html",
        references=reference_service.references,
        message_references=message_references,
        selected_value=sort_by,
        form=form,
    )


@app.route("/search/<search>", methods=["GET", "POST"])
def search_citations(search=None):
    form = SearchForm()

    if form.validate_on_submit():
        search = form.search.data
        return redirect(
            url_for(
                "search_citations",
                search=search,
                sort_by=request.args.get("sort_by", "title"),
            )
        )

    search = search or request.args.get("search", "")
    form.search.data = search
    sort_by = request.args.get("sort_by", "title")

    reference_service = ReferenceService()
    reference_service.add_references()

    if not reference_service.references:
        message_references = "You have no references saved"
    else:
        message_references = None

    if sort_by == "title":
        reference_service.sort_references_by_title()
    elif sort_by == "author":
        reference_service.sort_references_by_author()
    elif sort_by == "year":
        reference_service.sort_references_by_year()

    result = reference_service.search_with_keyword(search)
    message_search = f"({len(result)}) results found for {search}"

    return render_template(
        "index.html",
        references=result,
        message_references=message_references,
        message_search=message_search,
        selected_value=sort_by,
        form=form,
    )


@app.route("/add-article", methods=["POST", "GET"])
def add_article():
    form = AddArticleForm()

    if form.validate_on_submit():
        # Extract form data
        author = form.author.data
        title = form.title.data
        journal = form.journal.data
        year = form.year.data

        # Non-required fields are replaced with None if empty
        volume = form.volume.data if form.volume.data else None
        number = form.number.data if form.number.data else None
        pages = form.pages.data if form.pages.data else None
        month = form.month.data if form.month.data else None
        doi = form.doi.data if form.doi.data else None

        try:
            # Validate and create the article
            validate_article(
                author, title, journal, year, volume, number, pages, month, doi
            )
            flash("Article added successfully!", "success")  # Success message

            # Clear form fields after data extraction
            form.author.data = ""
            form.title.data = ""
            form.journal.data = ""
            form.year.data = ""
            form.volume.data = ""
            form.number.data = ""
            form.pages.data = ""
            form.month.data = ""
            form.doi.data = ""

            return redirect(url_for("index"))

        except UserInputError as e:
            # Pass the error message to the template
            flash(str(e), "error")  # Error message

    # Render the form again (with error messages if any)
    return render_template("article.html", form=form)


@app.route("/add-inproceedings", methods=["POST", "GET"])
def add_inproceedings():
    form = AddInproceedingsForm()

    if form.validate_on_submit():
        # Extract form data
        author = form.author.data
        title = form.title.data
        booktitle = form.booktitle.data
        year = form.year.data

        # Non-required fields are replaced with None if empty
        editor = form.editor.data if form.editor.data else None
        volume = form.volume.data if form.volume.data else None
        number = form.number.data if form.number.data else None
        series = form.series.data if form.series.data else None
        pages = form.pages.data if form.pages.data else None
        address = form.address.data if form.address.data else None
        month = form.month.data if form.month.data else None
        organization = form.organization.data if form.organization.data else None
        publisher = form.publisher.data if form.publisher.data else None

        try:
            # Validate and create the article
            validate_inproceedings(
                author,
                title,
                booktitle,
                year,
                editor,
                volume,
                number,
                series,
                pages,
                address,
                month,
                organization,
                publisher,
            )
            flash("Inproceedings added successfully!", "success")  # Success message

            # Clear form fields after data extraction
            form.author.data = ""
            form.title.data = ""
            form.booktitle.data = ""
            form.year.data = ""
            form.editor.data = ""
            form.volume.data = ""
            form.number.data = ""
            form.series.data = ""
            form.pages.data = ""
            form.address.data = ""
            form.month.data = ""
            form.organization.data = ""
            form.publisher.data = ""

            return redirect(url_for("index"))

        except UserInputError as e:
            # Pass the error message to the template
            flash(str(e), "error")  # Error message

    # Render the form again (with error messages if any)
    return render_template("inproceedings.html", form=form)


@app.route("/add-book", methods=["POST", "GET"])
def add_book():
    form = AddBookForm()

    if form.validate_on_submit():
        # Extract form data
        author = form.author.data
        title = form.title.data
        year = form.year.data

        # Non-required fields are replaced with None if empty
        publisher = form.publisher.data if form.publisher.data else None
        edition = form.edition.data if form.edition.data else None
        pages = form.pages.data if form.pages.data else None
        doi = form.doi.data if form.doi.data else None

        try:
            # Validate and create the article
            validate_book(author, title, year, publisher, edition, pages, doi)
            flash("Book added successfully!", "success")  # Success message

            # Clear form fields after data extraction
            form.author.data = ""
            form.title.data = ""
            form.year.data = ""
            form.publisher.data = ""
            form.edition.data = ""
            form.pages.data = ""
            form.doi.data = ""

            return redirect(url_for("index"))

        except UserInputError as e:
            # Pass the error message to the template
            flash(str(e), "error")  # Error message

    # Render the form again (with error messages if any)
    return render_template("book.html", form=form)


@app.route("/add-misc", methods=["POST", "GET"])
def add_misc():
    form = AddMiscForm()

    if form.validate_on_submit():
        # Extract form data
        author = form.author.data
        title = form.title.data
        year = form.year.data

        month = form.month.data if form.month.data else None
        howpublished = form.howpublished.data if form.howpublished.data else None
        note = form.note.data if form.note.data else None

        try:
            # Validate and create the article
            validate_misc(author, title, year, month, howpublished, note)
            flash("Misc added successfully!", "success")  # Success message

            # Clear form fields after data extraction
            form.author.data = ""
            form.title.data = ""
            form.year.data = ""
            form.month.data = ""
            form.howpublished.data = ""
            form.note.data = ""

            return redirect(url_for("index"))

        except UserInputError as e:
            # Pass the error message to the template
            flash(str(e), "error")  # Error message

    return render_template("misc.html", form=form)


@app.route("/delete/<citation_type>/<int:citation_id>", methods=["POST"])
def delete_citation(citation_type, citation_id):
    try:
        if citation_type == "article":
            article_repository.delete_article(citation_id)
        elif citation_type == "book":
            book_repository.delete_book(citation_id)
        elif citation_type == "inproceedings":
            inproceedings_repository.delete_inproceeding(citation_id)
        elif citation_type == "misc":
            misc_repository.delete_misc(citation_id)
        else:
            flash("Invalid citation type", "error")
            return redirect(url_for("index"))

        flash("Reference deleted successfully!", "success")
    except DeletionError as e:
        flash(f"Error deleting reference: {str(e)}", "error")

    return redirect(url_for("index"))


@app.route("/edit/<citation_type>/<int:citation_id>", methods=["GET", "POST"])
def edit_citation(citation_type, citation_id):
    form = None
    citation = None

    if citation_type == "article":
        citation = article_repository.get_article_by_id(citation_id)
        form = AddArticleForm(obj=citation)
    elif citation_type == "book":
        citation = book_repository.get_book_by_id(citation_id)
        form = AddBookForm(obj=citation)
    elif citation_type == "inproceedings":
        citation = inproceedings_repository.get_inproceeding_by_id(citation_id)
        form = AddInproceedingsForm(obj=citation)
    elif citation_type == "misc":
        citation = misc_repository.get_misc_by_id(citation_id)
        form = AddMiscForm(obj=citation)
    else:
        flash("Invalid reference type", "error")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        try:
            # Update based on type
            if citation_type == "article":
                validate_article(
                    form.author.data,
                    form.title.data,
                    form.journal.data,
                    form.year.data,
                    form.volume.data if form.volume.data else None,
                    form.number.data if form.number.data else None,
                    form.pages.data if form.pages.data else None,
                    form.month.data if form.month.data else None,
                    form.doi.data if form.doi.data else None,
                )

            elif citation_type == "book":
                validate_book(
                    form.author.data,
                    form.title.data,
                    form.year.data,
                    form.publisher.data if form.publisher.data else None,
                    form.edition.data if form.edition.data else None,
                    form.pages.data if form.pages.data else None,
                    form.doi.data if form.doi.data else None,
                )

            elif citation_type == "inproceedings":
                validate_inproceedings(
                    form.author.data,
                    form.title.data,
                    form.booktitle.data,
                    form.year.data,
                    form.editor.data if form.editor.data else None,
                    form.volume.data if form.volume.data else None,
                    form.number.data if form.number.data else None,
                    form.series.data if form.series.data else None,
                    form.pages.data if form.pages.data else None,
                    form.address.data if form.address.data else None,
                    form.month.data if form.month.data else None,
                    form.organization.data if form.organization.data else None,
                    form.publisher.data if form.publisher.data else None,
                )

            elif citation_type == "misc":
                validate_misc(
                    form.author.data,
                    form.title.data,
                    form.year.data,
                    form.month.data if form.month.data else None,
                    form.howpublished.data if form.howpublished.data else None,
                    form.note.data if form.note.data else None,
                )

            delete_citation(citation_type, citation_id)

            flash("Reference updated successfully!", "success")
            return redirect(url_for("index"))
        except UserInputError as e:
            flash(str(e), "error")

    return render_template(f"{citation_type}.html", form=form, editing=True)


@app.route("/bibtex", methods=["GET"])
def generate_bibtex_all():
    reference_service = ReferenceService()
    reference_service.add_references()
    bibtex_service = BibtexService(reference_service.references)
    bibtex_service.generate_bibtex_all()
    return render_template("bibtex.html", bibtex_string=bibtex_service.bibtex_string)



# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
