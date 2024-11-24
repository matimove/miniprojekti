from sqlalchemy import text
from config import db

def create_book(author, title, year, publisher, edition, pages, doi):
    sql = """
        INSERT INTO books
            (author, title, year, publisher, edition, pages, doi)
        VALUES
            (:author, :title, :year, :publisher, :edition, :pages, :doi)
        RETURNING id
    """
    params = {
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher,
        "edition": edition,
        "pages": pages,
        "doi": doi
    }

    book_id = db.session.execute(text(sql), params).fetchone()[0]
    db.session.commit()

    return book_id

def get_books():
    sql = "SELECT id, author, title, year, publisher, edition, pages, doi FROM books"
    result = db.session.execute(text(sql))
    articles = result.fetchall()
    return articles

def delete_book(id):
    sql = text("DELETE FROM books WHERE id = :id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

def get_book_by_id(id):
    sql = text("SELECT * FROM books WHERE id = :id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()