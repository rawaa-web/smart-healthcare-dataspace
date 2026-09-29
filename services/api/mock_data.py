"""S4: canned JSON returned by the API while MOCK_MODE=true.

Replace with real EDC connector responses when S3 delivers them.
"""

MOCK_CONNECTORS = [
    {
        "connector": "edc-a",
        "hospital": "a",
        "status": "up",
        "management_url": "http://edc-a:19193/management",
    },
    {
        "connector": "edc-b",
        "hospital": "b",
        "status": "up",
        "management_url": "http://edc-b:19193/management",
    },
    {
        "connector": "edc-c",
        "hospital": "c",
        "status": "up",
        "management_url": "http://edc-c:19193/management",
    },
]

MOCK_CONTRACTS = [
    {"contract_id": "contract-a", "hospital": "a", "status": "active"},
    {"contract_id": "contract-b", "hospital": "b", "status": "active"},
    {"contract_id": "contract-c", "hospital": "c", "status": "active"},
]

MOCK_LOGS = [
    {
        "time": "2026-01-01T10:00:00Z",
        "connector": "edc-a",
        "action": "publish",
        "asset": "hospital-a-data",
    },
    {
        "time": "2026-01-01T10:05:00Z",
        "connector": "edc-b",
        "action": "negotiate",
        "asset": "hospital-b-data",
    },
    {
        "time": "2026-01-01T10:07:00Z",
        "connector": "edc-c",
        "action": "negotiate",
        "asset": "hospital-c-data",
    },
]

MOCK_TRAINING_APPROVED = {
    "approved": True,
    "contracts": ["contract-a", "contract-b", "contract-c"],
}
