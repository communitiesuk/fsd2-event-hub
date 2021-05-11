import sqlite3

from flask import Flask, Response, g

app = Flask(__name__)

DB_PATH = "/usr/src/app/db.sqlite3"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db


@app.route("/")
def hello():
    return Response("Hello")
