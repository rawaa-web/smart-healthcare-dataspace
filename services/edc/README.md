# services/edc — Eclipse Dataspace Connectors (owner S3)

One connector per hospital (`edc-a`, `edc-b`, `edc-c`). The connectors are
**Java** services: there is deliberately **no Dockerfile and no code** for
them in this repository yet, and they are excluded from `docker-compose.yml`
and `k8s/kustomization.yaml` until S3 delivers them.

## What belongs here

- `config/` — one properties file per connector (`a.properties`, `b.properties`,
  `c.properties`) with the participant id, ports and API keys (never real keys).
- A `README.md` section with the curl cheat sheet for the connector
  management APIs once the connector version is pinned.

## Planned integration points (docs/interfaces.md)

- Management API of each connector: `http://edc-a|b|c:19193/management`
- The gateway (S4) calls the connectors through `services/api/edc_client.py`
  (publish / catalog / negotiate / logs — currently stubs).
- Prerequisite to build/run them locally: **JDK 17**.

## TODO S3

1. Pin the EDC connector version and document how to build its image.
2. Add `config/a.properties`, `config/b.properties`, `config/c.properties`.
3. Add the connector services to `docker-compose.yml` and `k8s/edc.yaml`,
   then remove the exclusions mentioned above.
