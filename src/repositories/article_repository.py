from sqlalchemy import text
from config import db

def get_articles():
    sql = "SELECT id, author, title, journal, year, volume, number, pages, month, doi FROM articles"
    result = db.session.execute(text(sql))
    articles = result.fetchall()
    return articles
