# 9. OpenID

Date: 2017-11-11

## Status

Accepted

## Context

We need an authentication mechanism for users. It must be secure and  
frontend application independent.

## Decision

We will use OpenID Connect. Open Lobby Server will provide all the hard stuff  
for a frontend applications. Ideally over the GraphQL API.

## Consequences

* We can create a user account simply on the first successful login.
* We don't have to verify user's email and to deal with situations like a lost  
password.
