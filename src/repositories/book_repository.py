from sqlalchemy import text
from config import db

def create_book(author, title, year, publisher, address, pages, doi):
    sql = """
        INSERT INTO books
            (author, title, year, publisher, address, pages, doi)
        VALUES
            (:author, :title, :year, :publisher, :address, :pages, :doi)
        RETURNING id
    """
    params = {
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher,
        "address": address,
        "pages": pages,
        "doi": doi
    }

    book_id = db.session.execute(text(sql), params).fetchone()[0]
    db.session.commit()

    return book_id

def get_books():
    sql = "SELECT id, author, title, year, publisher, address, pages, doi FROM books"
    result = db.session.execute(text(sql))
    articles = result.fetchall()
    return articles
