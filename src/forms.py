from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    journal = StringField("Journal", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])
    volume = StringField("Volume")
    number = StringField("Number")
    pages = StringField("Pages")
    month = StringField("Month")
    doi = StringField("doi")
    key = StringField("key")
    submit = SubmitField("Submit")


class AddBookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])
    publisher = StringField("Publisher")
    edition = StringField("edition")
    pages = StringField("Pages")
    doi = StringField("doi")
    submit = SubmitField("Submit")


class AddInproceedingsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    booktitle = StringField("Booktitle", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])
    editor = StringField("Editor")
    volume = StringField("Volume")
    number = StringField("Number")
    series = StringField("Series")
    pages = StringField("Pages")
    address = StringField("Address")
    month = StringField("Month")
    organization = StringField("Organization")
    publisher = StringField("Publisher")
    submit = SubmitField("Submit")


class AddMiscForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])
    month = StringField("Month")
    howpublished = StringField("How Published")
    note = StringField("Note")
    submit = SubmitField("Submit")


class AddDoiForm(FlaskForm):
    doi = StringField("DOI", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField("", validators=[DataRequired()])
    submit = SubmitField("Search")
