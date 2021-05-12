import logging
import os
import sqlite3

from flask import Flask, Response, g

app = Flask(__name__)
logging.basicConfig(level=os.environ["LOGLEVEL"])
logger = logging.getLogger(__name__)

DB_PATH = "/var/lib/sqlite3/eventhub.sqlite3"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db


@app.route("/")
def hello():
    logger.info('"Hello" was called')
    return Response("Hello")
