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


def get_abort_response(reason):
    return Response(f"REJECTED; {reason}", status=400)


# TODO: Fix this so that we pass in the origin of choice from ENVs (and document in README)
@app.after_request
def add_cors_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/events/<event_type>", methods=["GET"])
@app.route("/events/<event_type>/since/<seq>", methods=["GET"])
def list_events(event_type, seq=None):
    """
    List events of the given type.

    Optionally a subset of events can be requested, by use of the
    `since/<seq>` syntax.

    See README.md for details of the syntax options and the response
    payload components.
    """
    logger.info(f'list_events called with event_type "{event_type}, seq {seq}"')
    try:
        since_seq = int(seq or 0)
    except ValueError:
        return get_abort_response('"since_seq" must be an integer')
    if since_seq:
        results = query_db(
            "SELECT seq, data FROM events WHERE type = ? AND seq > ? ORDER BY seq",
            (event_type, since_seq),
        )
    else:
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
    """
    Append an event of the given type.

    See README.md for an example of the call payload.
    """
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
        return get_abort_response(sql_err)

    return Response(status=201)


@app.route("/events/<event_type>", methods=["DELETE"])
def delete_events(event_type):
    """
    Delete all events of given type.

    This method is to facilitate user-led administration of demonstration
    environments.

    Returns 204 regardless of number of records deleted.
    """
    data = request.data
    logger.info(f'append_event called with event_type "{event_type}" and data {data}')
    try:
        query_db(
            "DELETE FROM events WHERE type = ?",
            (event_type,),
        )
    except sqlite3.OperationalError as sql_err:
        return get_abort_response(sql_err)

    return Response(status=204)
