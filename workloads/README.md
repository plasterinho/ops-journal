# application-facing configs

App-level intent, fast-moving.

Each workload has:

* `base/` → environment-agnostic
* `overlays/` → environment-specific deltas

This is where app teams eventually live.

## Rule

If deleting it only breaks *one app*, it belongs here.
