from flask import redirect, render_template, request, jsonify, flash, url_for
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo
from forms import AddArticleForm

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

    return render_template("article.html", form=form) 

@app.route("/new_todo")
def new():
    return render_template("new_todo.html")

@app.route("/create_todo", methods=["POST"])
def todo_creation():
    content = request.form.get("content")

    try:
        validate_todo(content)
        create_todo(content)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_todo")

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
