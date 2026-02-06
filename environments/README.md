# cluster intent by environment

## Key idea

Environments don’t *define* workloads — they *select* them.

`environments/prod/` answers:

* which platform pieces exist here?
* which workloads are allowed to run here?

Not:

* "copy all YAMLs again but with *prod* values"

An environment:

* **does not** redefine apps
* **does not** duplicate configs
* **does not** contain raw Deployments

Instead, it says:

> "In *this* environment, reconcile *these* things."
