# 6. Use Flask

Date: 2017-11-11

## Status

Accepted

## Context

We need to choose webserver.

## Decision

We will use Flask. Server should be simple - pretty much just with a GraphQL  
endpoint and GraphiQL.

## Consequences

Flask has "no batteries included" so we will have to rely on third-party libs  
if we want to extend server later.
