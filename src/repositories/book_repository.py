from sqlalchemy import text
from config import db


def create_book(author, title, year, publisher, edition, pages, doi, key):
    sql = """
        INSERT INTO books
            (author, title, year, publisher, edition, pages, doi, key)
        VALUES
            (:author, :title, :year, :publisher, :edition, :pages, :doi, :key)
        RETURNING id
    """
    params = {
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher,
        "edition": edition,
        "pages": pages,
        "doi": doi,
        "key": key,
    }

    book_id = db.session.execute(text(sql), params).fetchone()[0]
    db.session.commit()

    return book_id


def get_books():
    sql = "SELECT id, category, author, title, year, publisher, edition, pages, doi, key FROM books"
    result = db.session.execute(text(sql))
    articles = result.fetchall()
    return articles


def delete_book(book_id):
    sql = text("DELETE FROM books WHERE id = :id")
    db.session.execute(sql, {"id": book_id})
    db.session.commit()


def get_book_by_id(book_id):
    sql = text("SELECT * FROM books WHERE id = :id")
    result = db.session.execute(sql, {"id": book_id})
    return result.fetchone()


def is_key_unique(key):
    sql = "SELECT COUNT(*) FROM books WHERE key = :key"
    result = db.session.execute(text(sql), {"key": key}).fetchone()[0]
    return result == 0
