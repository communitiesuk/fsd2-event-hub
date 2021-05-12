# fsd2-event-hub

A lightweight schema-enforcing event broker based on easily-tamed components requiring
little specialised maintenance / provision knowledge.

Part of the fsd-proto-2 project.

## Getting set up for development

1. Ensure you have the latest version of [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Run `docker-compose build`

## Running the service in development

### Build the container image

This is a one-off step (unless you materially change the project).

```shell script
docker-compose build
```

### Run the service

```shell script
docker-compose up
```

### Access the API

The API is exposed at http://localhost:5000


## Running in production

### ENVIRONMENT variables

If the container is brought up independently of Docker Compose,
the following vars must be made available:

| ENV VAR | Description |
| ------- | ----------- |
| LOGLEVEL | A string representation of one of the [Python logging levels](https://docs.python.org/3/library/logging.html#levels) |
