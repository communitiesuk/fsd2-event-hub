#!/bin/sh -e
# TODO: Get access logging on the console / output
gunicorn -b $SERVICE_ADDR:$SERVICE_PORT eventhub:app
