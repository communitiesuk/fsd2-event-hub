#!/bin/sh -e
gunicorn -b 0.0.0.0:$SERVICE_PORT eventhub:app
