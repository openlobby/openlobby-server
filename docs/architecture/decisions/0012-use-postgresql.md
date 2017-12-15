# 12. Use PostgreSQL

Date: 2017-12-16

## Status

Accepted

## Context

We want to add relational database.

## Decision

We will use PostgreSQL. It's a mature database with handy features like JSON  
and hstore data types. It's fully ACID compliant including schema changes. It  
has very good support in Django's ORM.

Another popular option is MySQL/MariaDB. But because it has a major bug `#28727`  
(10 years since it has been reported and it's still not fixed) breaking ACID in  
schema changes it can't be used for any serious project.

## Consequences

We will have mature relatonal database with handy JSON and hstore data types.
