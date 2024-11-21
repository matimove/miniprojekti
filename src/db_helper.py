from config import db, app
from sqlalchemy import text

table_names = ["articles", "inproceedings"]

def table_exists(name):
    sql_table_existence = text(
    "SELECT EXISTS ("
    "  SELECT 1"
    "  FROM information_schema.tables"
    f" WHERE table_name = '{name}'"
    ")"
    )

    print(f"Checking if table {name} exists")
    print(sql_table_existence)

    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]

def reset_db():
    for table_name in table_names:
        print(f"Clearing contents from table {table_name}")
        sql = text(f"DROP TABLE {table_name}")
        db.session.execute(sql)
        db.session.commit()

def setup_db():

    reset_db()

    print(f"Creating table: articles")

    sql = text(
        f"CREATE TABLE articles ("
        "  id SERIAL PRIMARY KEY,"
        "  title TEXT NOT NULL,"
        "  author TEXT NOT NULL,"
        "  journal TEXT NOT NULL,"
        "  year INTEGER NOT NULL,"
        "  volume INTEGER,"
        "  number INTEGER,"
        "  pages TEXT,"
        "  month TEXT,"
        "  doi TEXT"
        ");"

    )

    db.session.execute(sql)
    db.session.commit()

    print(f"Creating table: inproceedings")

    sql = text(
        f"CREATE TABLE inproceedings ("
        "  id SERIAL PRIMARY KEY,"
        "  title TEXT NOT NULL,"
        "  booktitle TEXT NOT NULL,"
        "  author TEXT NOT NULL,"
        "  year INTEGER NOT NULL,"
        "  editor TEXT,"
        "  volume INTEGER,"
        "  number INTEGER,"
        "  series TEXT,"
        "  pages TEXT,"
        "  address TEXT,"
        "  month TEXT,"
        "  organization TEXT,"
        "  publisher TEXT"
        ");"

    )

    db.session.execute(sql)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
