#!/bin/sh -e
gunicorn -b $SERVICE_ADDR:$SERVICE_PORT eventhub:app
