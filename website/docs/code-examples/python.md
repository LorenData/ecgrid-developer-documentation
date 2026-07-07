{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-06-17: Code examples section - Christian Nichols */}

---
title: Python
sidebar_position: 3
---

# Python Examples

These examples use the `requests` library. Install it with:

```bash
pip install requests
```

**Base URL:** `https://rest.ecgrid.io`

---

## Setup

```python
import requests

BASE_URL = "https://rest.ecgrid.io"

class ECGridClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._session_key: str | None = None

    def _login(self) -> str:
        response = self.session.post(
            f"{BASE_URL}/v2/auth/login",
            json={"apiKey": self.api_key}
        )
        response.raise_for_status()
        self._session_key = response.json()["data"]["sessionKey"]
        self.session.headers.update({"Authorization": f"Bearer {self._session_key}"})
        return self._session_key

    def _request(self, method: str, path: str, **kwargs):
        """Make an authenticated request, re-authenticating on 401."""
        if not self._session_key:
            self._login()

        response = self.session.request(method, f"{BASE_URL}{path}", **kwargs)

        if response.status_code == 401:
            self._login()
            response = self.session.request(method, f"{BASE_URL}{path}", **kwargs)

        response.raise_for_status()
        return response.json()

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, payload: dict, **kwargs):
        return self._request("POST", path, json=payload, **kwargs)

    def delete(self, path: str, payload: dict, **kwargs):
        return self._request("DELETE", path, json=payload, **kwargs)
```

---

## Authentication

```python
client = ECGridClient(api_key="YOUR_API_KEY")

# Authentication happens automatically on the first request.
# To authenticate explicitly:
session_key = client._login()
print(f"Session key: {session_key}")
```

---

## Mailboxes

### Get a mailbox by ID

```python
# GET /v2/mailboxes/{id}
result = client.get("/v2/mailboxes/1234")
mailbox = result["data"]

print(f"Mailbox: {mailbox['mailboxName']}")
print(f"Network: {mailbox['networkName']}")
```

### List mailboxes on a network

```python
# POST /v2/mailboxes/list
result = client.post("/v2/mailboxes/list", {
    "networkId":    5050,
    "mailboxId":    0,
    "showInactive": False,
})

for mb in result["data"]:
    print(f"{mb['mailboxId']}: {mb['mailboxName']}")
```

---

## Interchanges

### List inbound interchanges

```python
from datetime import datetime, timedelta

# POST /v2/interchanges/inbox-list
today    = datetime.utcnow().strftime("%Y-%m-%d")
week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

result = client.post("/v2/interchanges/inbox-list", {
    "networkId":  5050,
    "mailboxId":  0,
    "startDate":  week_ago,
    "endDate":    today,
    "pageSize":   50,
    "pageIndex":  1,
})

for ix in result["data"]:
    print(f"{ix['interchangeId']} | From: {ix['senderEDIId']} | {ix['statusDescription']}")
```

---

## Callbacks

### Create a webhook callback

```python
# POST /v2/callbacks/create
result = client.post("/v2/callbacks/create", {
    "networkId":          5050,
    "mailboxId":          0,
    "userId":             1001,
    "systemObject":       "Interchange",
    "objectStatus":       5,           # 5 = Ready
    "direction":          "InBox",
    "frequency":          60,
    "maxRetries":         24,
    "url":                "https://your-system.com/webhook/ecgrid",
    "httpAuthentication": None,
    "status":             "Active",
})

print(f"Callback event ID: {result['data']['callBackEventId']}")
```

### List callbacks for a mailbox

```python
# POST /v2/callbacks/event-list
result = client.post("/v2/callbacks/event-list", {
    "networkId":    5050,
    "mailboxId":    0,
    "showInactive": False,
})

for cb in result["data"]:
    print(f"{cb['callBackEventId']}: {cb['url']} [{cb['statusDescription']}]")
```

---

## Keys (Metadata)

### Create a metadata key

```python
# POST /v2/keys/create
client.post("/v2/keys/create", {
    "key":          "integration.vendorCode",
    "systemObject": "Mailbox",
    "objectId":     1234,
    "visibility":   "Private",
    "value":        "ACME-001",
    "meta":         "Vendor code for ACME Corp integration",
    "daysToLive":   -1,    # -1 = no expiry
})

print("Key created.")
```

### List all keys on an object

```python
# POST /v2/keys/list
result = client.post("/v2/keys/list", {
    "systemObject": "Mailbox",
    "objectId":     1234,
})

for k in result["data"]:
    print(f"{k['key']}: {k['value']}")
```

---

## Error Handling

`requests.raise_for_status()` raises `HTTPError` on non-2xx responses. The response body is RFC 7807 problem JSON:

```python
import requests

try:
    result = client.post("/v2/mailboxes/list", {
        "networkId":    5050,
        "mailboxId":    0,
        "showInactive": False,
    })
except requests.HTTPError as e:
    error = e.response.json()
    print(f"Status:   {e.response.status_code}")
    print(f"Title:    {error.get('title')}")
    print(f"Detail:   {error.get('detail')}")
    print(f"Trace ID: {error.get('traceId')}")
    # Include traceId when contacting ECGrid support
```
