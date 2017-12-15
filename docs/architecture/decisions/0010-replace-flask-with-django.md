# 10. Replace Flask with Django

Date: 2017-12-15

## Status

Accepted

Supercedes [6. Use Flask](0006-use-flask.md)

## Context

Flask turned out to be poorly designed piece of software which relays on too  
much magic like manipulations of global objects like `g`.

Seems like we will also decide to use relational database.

## Decision

We will switch to Django. It's not only well written server but it has also  
"batteries included" like a good ORM layer. And some other features like  
middlewares will simplify things.

## Consequences

* Extra work with rewriting functioning code.
* Better development practices and testing.
