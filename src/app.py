from flask import redirect, render_template, request, jsonify, flash, url_for
from db_helper import reset_db
from config import app, test_env
from forms import AddArticleForm

from services.article_service import validate_article, UserInputError
from repositories import article_repository

#Pieni muutos

@app.route("/")
def index():
    articles_list = article_repository.get_articles()
    if not articles_list:
        message = "You have no articles saved"
    else:
        message = None
    return render_template("index.html", articles=articles_list, message=message)

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

        try:
            # Validate and create the article
            validate_article(author, title, journal, year, volume, number, pages, month, doi)
            flash("Article added successfully!", "success")  # Success message
            return redirect(url_for("index"))

        except UserInputError as e:
            # Pass the error message to the template
            flash(str(e), "error")  # Error message

    # Render the form again (with error messages if any)
    return render_template("article.html", form=form) 

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
