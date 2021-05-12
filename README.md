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

#### Appending events

The API is exposed at http://localhost:5000.

Events are appended by POSTing to `/STREAM_NAME` with a JSON string body, e.g.:

```shell script
curl -H "Content-Type: application/json" -v \
     -d "{\"id\": \"a1231232\", \"name\": \"Horace\"}" \
     http://localhost:5000/events/game-characters
```

Returns a 201 on success; 400 on error.

#### Retrieving all events

Events are retrieved by GETting the same URL:

```shell script
curl http://localhost:5000/events/game-characters
```

Result:
```
{
  "events": [
    {
      "data": "{\"id\":\"bcd52333\",\"name\":\"Puckman\"}",
      "seq": 1
    },
    {
      "data": "{\"id\":\"a1231232\",\"name\":\"Horace\"}",
      "seq": 3
    }

  ],
  "last_seq_no": 3
}
```

NOTES:
1. `seq` is ordinal but not contiguous (i.e it is shared across event types)
2. Results are guaranteed to be in order of insert (with `seq` increasing)
3. `last_seq_no` is only in the payload if there are any events for the named stream

#### Retrieving recent events

Restrict the number of events returned by providing a `since_seq` value which is guaranteed to return only events
with a `seq` number greater than that provided. This may of course yield zero events.

```shell script
curl http://localhost:5000/events/game-characters/since/2
```

Result:
```
{
  "events": [
    {
      "data": "{\"id\":\"a1231232\",\"name\":\"Horace\"}",
      "seq": 3
    }

  ],
  "last_seq_no": 3
}
```

## Running in production

### ENVIRONMENT variables

If the container is brought up independently of Docker Compose,
the following vars must be made available:

| ENV VAR | Description |
| ------- | ----------- |
| LOGLEVEL | A string representation of one of the [Python logging levels](https://docs.python.org/3/library/logging.html#levels) |
