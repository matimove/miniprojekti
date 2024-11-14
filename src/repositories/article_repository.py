from sqlalchemy import text
from config import db

def get_articles():
    sql = "SELECT id, author, title, journal, year, volume, number, pages, month, doi FROM articles"
    result = db.session.execute(text(sql))
    articles = result.fetchall()
    return articles

def create_article(author, title, journal, year, volume, number, pages, month, doi):
    sql = """
        INSERT INTO articles
            (author, title, journal, year, volume, number, pages, month, doi)
        VALUES
            (:author, :title, :journal, :year, :volume, :number, :pages, :month, :doi)
        RETURNING id
    """
    params = {
        "author": author,
        "title": title,
        "journal": journal,
        "year": year,
        "volume": volume,
        "number": number,
        "pages": pages,
        "month": month,
        "doi": doi
    }

    article_id = db.session.execute(text(sql), params).fetchone()[0]
    db.session.commit()

    return article_id