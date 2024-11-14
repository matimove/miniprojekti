from flask import redirect, render_template, request, jsonify, flash, url_for
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo
from forms import AddArticleForm

#Pieni muutos

@app.route("/")
def index():
    todos = get_todos()
    unfinished = len([todo for todo in todos if not todo.done])
    return render_template("index.html", todos=todos, unfinished=unfinished) 

@app.route("/add-article", methods=["POST", "GET"])
def add_article():
    form = AddArticleForm()

    if form.validate_on_submit():
        author = form.author.data 
        title = form.title.data
        journal = form.journal.data
        year = form.year.data
        volume = form.volume.data
        number = form.number.data
        pages = form.pages.data
        month = form.month.data
        doi = form.doi.data

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

@app.route("/add_article")
def new():
    return render_template("article.html")

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
