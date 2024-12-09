from sqlalchemy import text
from config import db


def create_inproceedings(
    title,
    author,
    booktitle,
    year,
    editor,
    volume,
    number,
    series,
    pages,
    address,
    month,
    organization,
    publisher,
    key,
):
    sql = """
        INSERT INTO inproceedings
            (author, title, booktitle, year, editor, volume, number, series, pages, address, month, organization, publisher, key)
        VALUES
            (:author, :title, :booktitle, :year, :editor, :volume, :number, :series, :pages, :address, :month, :organization, :publisher, :key)
        RETURNING id
    """
    params = {
        "author": author,
        "title": title,
        "booktitle": booktitle,
        "year": year,
        "editor": editor,
        "volume": volume,
        "number": number,
        "series": series,
        "pages": pages,
        "address": address,
        "month": month,
        "organization": organization,
        "publisher": publisher,
        "key": key,
    }

    inproceedings_id = db.session.execute(text(sql), params).fetchone()[0]
    db.session.commit()

    return inproceedings_id


def get_inproceedings():
    sql = """
        SELECT
            id, category, title, author, booktitle, year, editor, volume, number, series, pages, address, month, organization, publisher, key
        FROM inproceedings
    """
    result = db.session.execute(text(sql))
    inproceedings = result.fetchall()
    return inproceedings


def delete_inproceeding(inproceeding_id):
    sql = text("DELETE FROM inproceedings WHERE id = :id")
    db.session.execute(sql, {"id": inproceeding_id})
    db.session.commit()


def get_inproceeding_by_id(inproceeding_id):
    sql = text("SELECT * FROM inproceedings WHERE id = :id")
    result = db.session.execute(sql, {"id": inproceeding_id})
    return result.fetchone()


def is_key_unique(key):
    sql = "SELECT COUNT(*) FROM inproceedings WHERE key = :key"
    result = db.session.execute(text(sql), {"key": key}).fetchone()[0]
    return result == 0
