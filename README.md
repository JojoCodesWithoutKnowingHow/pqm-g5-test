# pqm-g5-test

A throwaway companion program for **Prompt Queue Manager** (PQM), session G.5:
the smallest thing that looks like a real extension's remote half to PQM's pod
agent. PQM fetches it onto a rented pod at a pinned commit, runs its install
step, starts its service, and checks each one before the pod counts as booted.

- `install.py <part>` — an install step. Hashes this checkout and writes
  `installed-<part>.json` into the extension's folder on the pod. `fail` exits 3
  on purpose.
- `serve.py <port>` — a service on `127.0.0.1:<port>` with `GET /health`.

Standard library only. Nothing here is useful outside PQM's tests.
