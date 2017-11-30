# Open Lobby Server

Open Lobby is register of lobby meetings. It's being developed for and tested
on [Czech Pirate Party](https://www.pirati.cz) but later it may be used by
any party, organization, agency, ...

_Open Lobby is in early beta version now. Not for production use._

This is core of the register - server with [GraphQL API](http://graphql.org).
Over API are connected application interfaces. Default web application is
available at
[openlobby/openlobby-app](https://github.com/openlobby/openlobby-app).

Register is built on top of
[Elasticsearch](https://www.elastic.co/products/elasticsearch). For now it's
intended for search in Czech language with custom Czech text analyzer. There is
prepared Elasticsearch Docker container with Czech support at
[openlobby/openlobby-es-czech](https://github.com/openlobby/openlobby-es-czech).

## Configuration

Configuration is done by environment variables:
 - `SECRET_KEY` - long random secret string (required)
 - `ELASTICSEARCH_DSN` - DSN of Elasticsearch cluster (default: `http://localhost:9200`)
 - `SITE_NAME` - site name for OpenID authentication (default: `Open Lobby`)
 - `ES_INDEX` - Elasticsearch index (default: `openlobby`)

## Docker

Docker image is at Docker Hub
[openlobby/openlobby-server](https://hub.docker.com/r/openlobby/openlobby-server/).
It exposes server on port 8010. You should provide it environment variables for
configuration (at least `SECRET_KEY`).

## Demo

Demo of Open Lobby with instructions is in repository
[openlobby/demo](https://github.com/openlobby/demo).

## Local run and development

You need to have Python 3 installed. Clone this repository and run:

1. `make init-env` - prepares Python virtualenv in dir `.env`
2. `source .env/bin/activate` - activates virtualenv
3. `make install` - installs requirements and server in development mode
4. `make run` - runs development server on port `8010`

Now you can use GraphQL API endpoint and GraphiQL web interface at
`http://localhost:8010/graphql`

Next time you can just do steps 2 and 4.

Development server assumes that you have
[openlobby/openlobby-es-czech](https://github.com/openlobby/openlobby-es-czech).
running on `http://localhost:9200`. You can override this address in environment
variable `ELASTICSEARCH_DSN`. E.g.
`ELASTICSEARCH_DSN=http://my-server:9200 make run`

### Testing

Run: `pytest`

Expects Elasticsearch for tests running on `localhost:9200` (can be override by
environment variable `ELASTICSEARCH_DSN`). Tests creates random indices with
prefix `test_` and deletes all indices matching `test_*` on teardown.
