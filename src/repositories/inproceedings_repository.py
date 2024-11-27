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
):
    sql = """
        INSERT INTO inproceedings
            (author, title, booktitle, year, editor, volume, number, series, pages, address, month, organization, publisher)
        VALUES
            (:author, :title, :booktitle, :year, :editor, :volume, :number, :series, :pages, :address, :month, :organization, :publisher)
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
    }

    inproceedings_id = db.session.execute(text(sql), params).fetchone()[0]
    db.session.commit()

    return inproceedings_id


def get_inproceedings():
    sql = "SELECT id, title, author, booktitle, year, editor, volume, number, series, pages, address, month, organization, publisher FROM inproceedings"
    result = db.session.execute(text(sql))
    inproceedings = result.fetchall()
    return inproceedings


def delete_inproceeding(id):
    sql = text("DELETE FROM inproceedings WHERE id = :id")
    db.session.execute(sql, {"id": id})
    db.session.commit()


def get_inproceeding_by_id(id):
    sql = text("SELECT * FROM inproceedings WHERE id = :id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()
