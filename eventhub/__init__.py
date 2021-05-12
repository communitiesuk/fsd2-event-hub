import logging
import os
import sqlite3

from flask import Flask, Response, g, request

app = Flask(__name__)
logging.basicConfig(level=os.environ["LOGLEVEL"])
logger = logging.getLogger(__name__)

DB_PATH = "/var/lib/sqlite3/eventhub.sqlite3"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH, isolation_level=None)  # autocommit
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/events/<event_type>", methods=["GET"])
def list_events(event_type):
    logger.info(f'list_events called with event_type "{event_type}"')
    results = query_db(
        "SELECT seq, data FROM events WHERE type = ? ORDER BY seq", (event_type,)
    )
    events = [{"seq": r[0], "data": r[1]} for r in results]
    result = {"events": events}
    if events:
        result["last_seq_no"] = events[-1]["seq"]
    return result


@app.route("/events/<event_type>", methods=["POST"])
def append_event(event_type):
    # We don't bother to validate the data as JSON since if it's badly formed,
    # the db will reject it.
    data = request.data
    logger.info(f'append_event called with event_type "{event_type}" and data {data}')
    try:
        result = query_db(
            "INSERT INTO events (type, data) VALUES (?, json(?))",
            (
                event_type,
                data,
            ),
        )
    except sqlite3.OperationalError as sql_err:
        return Response(f"REJECTED; {sql_err}", status=400)

    return Response(status=201)
