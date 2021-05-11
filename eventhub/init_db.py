from eventhub import app, get_db


def load_schema():
    print("Loading schema")
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == "__main__":
    load_schema()
