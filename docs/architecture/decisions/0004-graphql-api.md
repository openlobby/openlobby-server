# 4. GraphQL API

Date: 2017-11-11

## Status

Accepted

## Context

Open Lobby Server will be written in API First design. Frontend applications  
will be based on it's API.

## Decision

We will use GraphQL as API standard. From other options like REST and Graph API  
it's the most client friendly approach. GraphQL query language is easy to use,  
validated and self documenting.

GraphQL allows clients to get everything they need in one request without any  
overhead of not needed data. That is very important for mobile frontends.

GraphiQL tool also provides easy way for developers to inspect and try API. So  
it's easy to adopt by frontend applications developers or other API users.

## Consequences

* Clients can use API effectively.
* GraphiQL tool for free.
* Saves a lot of time of writing API documentation.
