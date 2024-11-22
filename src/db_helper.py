from config import db, app
from sqlalchemy import text

table_names = ["articles", "books"]

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
        sql = text(f"DELETE FROM {table_name}")
        db.session.execute(sql)
        db.session.commit()

def setup_db():
    for table_name in table_names:
        if table_exists(table_name):
          print(f"Table {table_name} exists, dropping")
          sql = text(f"DROP TABLE {table_name}")
          db.session.execute(sql)
          db.session.commit()

        if table_name == "articles":
            print(f"Creating table {table_name}")
            sql = text(
                f"CREATE TABLE {table_name} ("
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
        elif table_name == "books":
            print(f"Creating table {table_name}")
            sql = text(
                f"CREATE TABLE {table_name} ("
                "  id SERIAL PRIMARY KEY,"
                "  title TEXT NOT NULL,"
                "  author TEXT NOT NULL,"
                "  year INTEGER NOT NULL,"
                "  publisher TEXT ,"
                "  edition TEXT,"
                "  pages TEXT,"
                "  doi TEXT"
                ");"
            )

        db.session.execute(sql)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
