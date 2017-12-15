# 7. Adopt GraphQL Relay specification

Date: 2017-11-11

## Status

Accepted

## Context

We need to make API friendly for clients and design pagination.

## Decision

We will adopt GraphQL Relay specification. It solves pagination so we don't  
have to reinvent a wheel. It has handy Node interface for re-fetching objects.  
It has a way to define inputs in mutations.

Graphene lib has good support for creating API following Relay specifications.

## Consequences

* It will be easy to write SPA in JavaScript because it has Relay client lib.  
* It may require some extra work to fulfill Relay specification.
