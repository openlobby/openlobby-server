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
 - `DEBUG` - Set to any value to turn on debug mode. Don't use in production!
 - `SECRET_KEY` - long random secret string (required if not in debug mode)
 - `DATABASE_DSN` - DSN of PostgreSQL database (default: `postgresql://db:db@localhost:5432/openlobby`)
 - `ELASTICSEARCH_DSN` - DSN of Elasticsearch cluster (default: `http://localhost:9200`)
 - `SITE_NAME` - site name for OpenID authentication (default: `Open Lobby`)
 - `ES_INDEX` - Elasticsearch indices prefix (default: `openlobby`)
 - `REDIRECT_URI` - redirect URI used in OpenID Connect authentication (default: `http://localhost:8010/login-redirect`)
     - put there address where you run server, but keep there `/login-redirect`
     - this is the Redirect URI for static client registration at OpenID Provider

### Login shortcuts aka preregistered OpenID Clients

Some OpenID Providers does not allow dynamic client registration. You can still
use them. Register client with `REDIRECT_URI` and save client's credentials into
database. You can do it in admin interface running at `/admin`. It's standard
Django admin (create superuser for yourself like `./manage.py createsuperuser`).

## Docker

Docker image is at Docker Hub
[openlobby/openlobby-server](https://hub.docker.com/r/openlobby/openlobby-server/).
It exposes server on port 8010. You should provide it environment variables for
configuration (at least `SECRET_KEY`).

## Demo

Demo of Open Lobby with instructions is in repository
[openlobby/demo](https://github.com/openlobby/demo).

## Local run and development

### Prerequisites

You need to have Python 3 installed.

Run PostgreSQL database on `localhost:5432` with user `db`, password `db` and
database `openlobby`. You can provide different address in environment variable
`DATABASE_DSN`.

Run Elasticsearch server
[openlobby/openlobby-es-czech](https://github.com/openlobby/openlobby-es-czech) 
on `http://localhost:9200`. You can provide different address in environment
variable `ELASTICSEARCH_DSN`.

### Local run

Clone this repository and run:

1. `make init-env` - prepares Python virtualenv in dir `.env`
2. `source .env/bin/activate` - activates virtualenv
3. `make install` - installs requirements and server in development mode
4. `make migrate` - runs database migrations and rebuilds Elasticsearch index
5. `make run` - runs development server on port `8010`

Now you can use GraphQL API endpoint and GraphiQL web interface at
`http://localhost:8010/graphql`

Next time you can just do steps 2 and 5.

### Testing

Run: `pytest`

For full test suite run you have to provide OpenID Provider issuer URL which
allows client registration. For example you can run Keycloak sever locally:
`docker run -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=pass -p 8080:8080 --rm jboss/keycloak`

Login into Keycloak admin console `http://localhost:8080/auth/admin/`
(as admin/pass) and go to Realm Settings -> Client Registration -> Client 
Registration Policies -> Trusted Hosts. There add `localhost` to "Trusted 
Hosts", turn off "Host Sending Client Registration Request Must Match" and save
it.

Now run: `pytest --issuer=http://localhost:8080/auth/realms/master`
