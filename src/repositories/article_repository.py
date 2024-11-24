from sqlalchemy import text
from config import db

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

def get_articles():
    sql = "SELECT id, author, title, journal, year, volume, number, pages, month, doi FROM articles"
    result = db.session.execute(text(sql))
    articles = result.fetchall()
    return articles

def delete_article(id):
    sql = text("DELETE FROM articles WHERE id = :id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

def get_article_by_id(id):
    sql = text("SELECT * FROM articles WHERE id = :id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()