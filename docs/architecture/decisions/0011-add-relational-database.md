# 11. Add relational database

Date: 2017-12-15

## Status

Accepted

## Context

Number of document types which does not use Elasticsearch's fulltext  
capabilities is growing. Recently released Elasticsearch 6 is bringing one type  
per index which means management of many indices.

## Decision

We will add relational database as primary database. Elasticsearch will be used  
for denormalized reports and related data intended for fulltext search.

## Consequences

* Proper relations in data on database level.
* Simplification in data management and schema migrations.
* If ORM is used then GraphQL types may be derived without additional effort  
and translations between document types and GraphQL types.
* Less indices in Elasticsearch.
