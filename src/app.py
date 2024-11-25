from flask import redirect, render_template, request, jsonify, flash, url_for
from db_helper import reset_db
from config import app, test_env

from forms import AddArticleForm, AddBookForm, AddInproceedingsForm
from services.article_service import validate_article, UserInputError as ArticleUserInputError
from services.book_service import validate_book, UserInputError
from services.inproceedings_service import validate_inproceedings, UserInputError as InproceedingsUserInputError
from repositories import article_repository, book_repository, inproceedings_repository


#Pieni muutos

@app.route("/")
def index():
    articles_list = article_repository.get_articles()
    if not articles_list:
        message_articles = "You have no articles saved"
    else:
        message_articles = None

    books_list = book_repository.get_books()
    if not books_list:
        message_books = "You have no books saved"
    else:
        message_books = None

    inproceedings_list = inproceedings_repository.get_inproceedings()
    if not inproceedings_list:
        message_inproceedings = "You have no inproceedings saved"
    else:
        message_inproceedings = None

    return render_template("index.html", articles=articles_list, message_articles=message_articles,
                            books_list=books_list, message_books=message_books,
                            inproceedings_list=inproceedings_list, message_inproceedings=message_inproceedings)


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
            validate_article(author, title, journal, year, volume, number, pages, month, doi)
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

        except ArticleUserInputError as e:
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
            validate_inproceedings(author, title, booktitle, year, editor, volume, number, series, pages, address, month, organization, publisher)
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

        except InproceedingsUserInputError as e:
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

@app.route("/add-conference", methods=["POST", "GET"])
def add_conference():
    # toistaiseksi ohjaa vain takaisin etusivulle
    return redirect(url_for("index"))



@app.route("/add-misc", methods=["POST", "GET"])
def add_misc():
    # toistaiseksi ohjaa vain takaisin etusivulle
    return redirect(url_for("index"))


@app.route("/delete/<citation_type>/<int:id>", methods=["POST"])
def delete_citation(citation_type, id):
    try:
        if citation_type == "article":
            article_repository.delete_article(id)
        elif citation_type == "book":
            book_repository.delete_book(id)
        elif citation_type == "inproceedings":
            inproceedings_repository.delete_inproceeding(id)
        else:
            flash("Invalid citation type", "error")
            return redirect(url_for("index"))
        
        flash("Reference deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting reference: {str(e)}", "error")
    
    return redirect(url_for("index"))

@app.route("/edit/<citation_type>/<int:id>", methods=["GET", "POST"])
def edit_citation(citation_type, id):
    form = None
    citation = None

    if citation_type == "article":
        citation = article_repository.get_article_by_id(id)
        form = AddArticleForm(obj=citation)
    elif citation_type == "book":
        citation = book_repository.get_book_by_id(id)
        form = AddBookForm(obj=citation)
    elif citation_type == "inproceedings":
        citation = inproceedings_repository.get_inproceeding_by_id(id)
        form = AddInproceedingsForm(obj=citation)
    else:
        flash("Invalid reference type", "error")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        try:
            # Update based on type
            if citation_type == "article":
                validate_article(
                    form.author.data, form.title.data, form.journal.data,
                    form.year.data, form.volume.data, form.number.data,
                    form.pages.data, form.month.data, form.doi.data
                )
            elif citation_type == "book":
                validate_book(
                    form.author.data, form.title.data, form.year.data,
                    form.publisher.data, form.edition.data, form.pages.data,
                    form.doi.data
                )
            elif citation_type == "inproceedings":
                validate_inproceedings(
                    form.author.data, form.title.data, form.booktitle.data,
                    form.year.data, form.editor.data, form.volume.data,
                    form.number.data, form.series.data, form.pages.data,
                    form.address.data, form.month.data, form.organization.data,
                    form.publisher.data
                )

            if citation_type == "article":
                article_repository.delete_article(id)
            elif citation_type == "book":
                book_repository.delete_book(id)
            elif citation_type == "inproceedings":
                inproceedings_repository.delete_inproceeding(id)
            
            flash("Reference updated successfully!", "success")
            return redirect(url_for("index"))
        except (ArticleUserInputError, UserInputError, InproceedingsUserInputError) as e:
            flash(str(e), "error")
    
    return render_template(f"{citation_type}.html", form=form, editing=True)


# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
    


