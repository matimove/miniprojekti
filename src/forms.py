from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email


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
