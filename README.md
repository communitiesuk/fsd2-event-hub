# fsd2-event-hub

A lightweight schema-enforcing event broker based on easily-tamed components requiring
little specialised maintenance / provision knowledge.

Part of the fsd-proto-2 project.

## Getting set up for development

1. Ensure you have the latest version of [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Run `docker-compose build`

## Running the service

### Build the container image

This is a one-off step (unless you materially change the project).

```shell script
docker build -t fsdeventhub .
```

### Run the service

```shell script
docker run --rm -it -e SERVICE_PORT=8000 fsdeventhub
```