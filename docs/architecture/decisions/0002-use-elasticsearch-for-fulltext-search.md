# 2. Use Elasticsearch for fulltext search

Date: 2017-11-11

## Status

Accepted

## Context

We need a database with fulltext search capable of searching in various  
languages especially in Czech.

## Decision

We will use Elasticsearch. It's well known database with great fulltext search  
capabilities based on Apache Lucene. It has also aggregations, highlighting of  
results, and many other useful features.

We will use it as database for all data so we have just one database in the  
system.

## Consequences

* Great fulltext in any language.
* Some extra work on application level with management of database relations,  
  because Elasticsearch is not relational database.
