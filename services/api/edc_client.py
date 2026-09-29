"""S4: thin HTTP client for the Eclipse Dataspace Connectors (S3).

The connectors are Java services owned by S3 and do not exist yet, so these
functions stay stubs. Planned base URLs (docs/interfaces.md):
    http://edc-a:19193/management
    http://edc-b:19193/management
    http://edc-c:19193/management

Owner: S4.
"""


def publish_asset(connector: str, payload: dict) -> dict:
    """Publish a hospital dataset as an EDC asset on `connector`."""
    raise NotImplementedError(f"S4: implement publish_asset({connector!r})")


def request_catalog(connector: str) -> dict:
    """Fetch the public data catalog advertised by `connector`."""
    raise NotImplementedError(f"S4: implement request_catalog({connector!r})")


def negotiate_contract(connector: str, asset_id: str) -> dict:
    """Start and complete a contract negotiation for `asset_id`."""
    raise NotImplementedError(f"S4: implement negotiate_contract({connector!r})")


def fetch_logs(connector: str) -> dict:
    """Fetch the audit trail (agreements / transfers) of `connector`."""
    raise NotImplementedError(f"S4: implement fetch_logs({connector!r})")
