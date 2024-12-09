from sqlalchemy import text
from config import db


def create_misc(author, title, year, month, note, howpublished, key):
    sql = """
        INSERT INTO misc
            (author, title, year, month, howpublished, note, key)
        VALUES
            (:author, :title, :year, :month, :howpublished, :note, :key)
        RETURNING id
        """
    params = {
        "author": author,
        "title": title,
        "year": year,
        "month": month,
        "howpublished": howpublished,
        "note": note,
        "key": key,
    }

    misc_id = db.session.execute(text(sql), params).fetchone()[0]
    db.session.commit()

    return misc_id


def get_misc():
    sql = "SELECT id, category, author, title, year, month, howpublished, note, key FROM misc"
    result = db.session.execute(text(sql))
    articles = result.fetchall()
    return articles


def delete_misc(misc_id):
    sql = text("DELETE FROM misc WHERE id = :id")
    db.session.execute(sql, {"id": misc_id})
    db.session.commit()


def get_misc_by_id(misc_id):
    sql = text("SELECT * FROM misc WHERE id = :id")
    result = db.session.execute(sql, {"id": misc_id})
    return result.fetchone()


def is_key_unique(key):
    sql = "SELECT COUNT(*) FROM misc WHERE key = :key"
    result = db.session.execute(text(sql), {"key": key}).fetchone()[0]
    return result == 0
