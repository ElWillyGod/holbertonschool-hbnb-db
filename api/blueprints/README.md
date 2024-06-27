# Blueprints
---

## What
  Blueprints are essentially a pre-app object. We use them to attach endpoints
and some configurations without the need to passing the app instance around
like we did before.

## Why
  We've decieded to use them as they offer a way to compartmentalize all the
endpoints and use them in a factory pattern.

## How
  In each file we have a blueprint instance called bp where we attach each
endpoint. We also configure it to manage a URL prefix to make it more clean,
excpet on reviews as it uses multiple URLs that a prefix is not viable. On the
init we import those blueprints and attach them to an app instance.
