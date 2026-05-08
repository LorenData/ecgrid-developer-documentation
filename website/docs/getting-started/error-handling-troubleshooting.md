---
title: Error Handling & Troubleshooting
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created error handling and troubleshooting guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs to error handling and retry examples - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Error Handling & Troubleshooting

This guide covers error formats, HTTP status codes, retry strategies, and common troubleshooting scenarios for both the REST and SOAP APIs.

## REST Error Format

All REST API errors return a consistent JSON structure regardless of the HTTP status code:

```json
{
  "success": false,
  "errorCode": "InvalidSession",
  "message": "The session token is invalid or has expired.",
  "data": null
}
```

| Field | Type | Description |
|---|---|---|
| `success` | boolean | Always `false` for error responses |
| `errorCode` | string | Machine-readable error identifier |
| `message` | string | Human-readable description |
| `data` | object/null | Always `null` for error responses |

### HTTP Status Codes

| Status | Meaning | Common Cause |
|---|---|---|
| `200 OK` | Success | Request processed normally |
| `400 Bad Request` | Invalid input | Missing required field, malformed JSON, constraint violation |
| `401 Unauthorized` | Authentication failed | Missing, expired, or invalid API key / token |
| `403 Forbidden` | Insufficient permissions | User `AuthLevel` does not allow this operation |
| `404 Not Found` | Resource not found | Incorrect ID, resource deleted, or wrong endpoint path |
| `429 Too Many Requests` | Rate limit exceeded | Too many calls in a short window — back off and retry |
| `500 Internal Server Error` | Server-side fault | Unexpected error — retry with backoff; contact support if persistent |

### Common REST Error Codes

| Error Code | HTTP Status | Description |
|---|---|---|
| `InvalidSession` | 401 | Session token is missing, malformed, or expired |
| `InvalidAPIKey` | 401 | The `X-API-Key` value is not recognized |
| `InvalidParameter` | 400 | A required parameter is missing or its value fails validation |
| `AccessDenied` | 403 | The authenticated user lacks the required `AuthLevel` |
| `ObjectNotFound` | 404 | The requested resource does not exist |
| `DuplicateObject` | 400 | An object with the same key already exists |
| `RateLimitExceeded` | 429 | Too many requests — see retry guidance below |
| `InternalError` | 500 | Unexpected server-side error |

See [Error Codes](../appendix/error-codes.md) for the complete list.

### REST C# Exception Handling

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Check HTTP status and parse error JSON
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  https://rest.ecgrid.io/v2/mailboxes/99999)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -1)

if [ "$HTTP_CODE" -ge 400 ]; then
  ERROR_CODE=$(echo "$BODY" | jq -r '.errorCode')
  MESSAGE=$(echo "$BODY" | jq -r '.message')
  echo "Error [$HTTP_CODE] [$ERROR_CODE]: $MESSAGE" >&2
fi
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — structured error handling for REST API calls
using System.Net.Http.Json;

record ApiError(bool Success, string? ErrorCode, string? Message);

/// <summary>Executes a REST call and surfaces API errors as exceptions.</summary>
static async Task<T> ExecuteAsync<T>(HttpResponseMessage response)
{
    // Deserialize whether success or failure
    if (response.IsSuccessStatusCode)
    {
        var result = await response.Content.ReadFromJsonAsync<ApiResponse<T>>();
        return result!.Data!;
    }

    // Try to parse the structured error body
    ApiError? error = null;
    try
    {
        error = await response.Content.ReadFromJsonAsync<ApiError>();
    }
    catch { /* fall through to generic message */ }

    var code    = error?.ErrorCode ?? "Unknown";
    var message = error?.Message   ?? response.ReasonPhrase ?? "Unknown error";

    throw response.StatusCode switch
    {
        System.Net.HttpStatusCode.Unauthorized  => new UnauthorizedAccessException($"[{code}] {message}"),
        System.Net.HttpStatusCode.Forbidden     => new UnauthorizedAccessException($"[{code}] {message}"),
        System.Net.HttpStatusCode.NotFound      => new KeyNotFoundException($"[{code}] {message}"),
        System.Net.HttpStatusCode.TooManyRequests => new HttpRequestException($"Rate limit exceeded: {message}"),
        _ => new HttpRequestException($"[{(int)response.StatusCode}] [{code}] {message}")
    };
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — structured error handling for REST API calls
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/99999"))
    .header("X-API-Key", apiKey)
    .GET()
    .build();

var response = http.send(request, BodyHandlers.ofString());
int status = response.statusCode();

if (status >= 400) {
    // Parse error JSON — use a JSON library (e.g. Jackson) in production
    String body = response.body();
    // Extract errorCode and message from body
    System.err.println("Error [" + status + "] from API: " + body);
    // Throw appropriate exception based on status
    if (status == 401) throw new SecurityException("Unauthorized: check API key");
    if (status == 404) throw new java.util.NoSuchElementException("Resource not found");
    throw new RuntimeException("API error " + status + ": " + body);
}
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — structured error handling for REST API calls
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/mailboxes/99999', {
  headers: { 'X-API-Key': apiKey }
});

if (!response.ok) {
  let errorCode = 'Unknown', message = response.statusText;
  try {
    const err = await response.json();
    errorCode = err.errorCode ?? errorCode;
    message   = err.message   ?? message;
  } catch { /* non-JSON error body */ }

  const err = new Error(`[${response.status}] [${errorCode}] ${message}`);
  err.status = response.status;
  throw err;
}

const data = await response.json();
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

resp = session.get("https://rest.ecgrid.io/v2/mailboxes/99999")

if not resp.ok:
    try:
        err = resp.json()
        error_code = err.get("errorCode", "Unknown")
        message    = err.get("message", resp.reason)
    except Exception:
        error_code, message = "Unknown", resp.text

    raise Exception(f"[{resp.status_code}] [{error_code}] {message}")

data = resp.json()
```

</TabItem>
</Tabs>

---

## SOAP Error Format

SOAP errors are returned as standard SOAP Faults. ECGridOS extends the fault with a numeric error code.

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <soap:Fault>
      <faultcode>soap:Client</faultcode>
      <faultstring>Invalid SessionID</faultstring>
      <detail>
        <ECGridOSSOAPErrorCode>5</ECGridOSSOAPErrorCode>
      </detail>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>
```

### SOAP C# Exception Handling

When using `dotnet-svcutil`, SOAP faults surface as `FaultException`:

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — SOAP fault handling with dotnet-svcutil proxy
using System.ServiceModel;

var sessionID = string.Empty;
try
{
    sessionID = await client.LoginAsync(email, password);
    var parcelList = await client.ParcelInBoxAsync(sessionID, mailboxID, begin, end);
}
catch (FaultException fault)
{
    // fault.Message contains the SOAP faultstring
    // fault.Code.Name is "Client" or "Server"
    Console.Error.WriteLine($"SOAP Fault [{fault.Code.Name}]: {fault.Message}");

    // Check ECGridOSSOAPErrorCode in fault.Detail if needed
}
catch (CommunicationException ex)
{
    // Network-level error (timeout, connection refused, etc.)
    Console.Error.WriteLine($"Communication error: {ex.Message}");
}
finally
{
    if (!string.IsNullOrEmpty(sessionID))
        await client.LogoutAsync(sessionID);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — detect SOAP faults in the raw XML response
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Build and send a SOAP request
String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><!-- operation here --></soap:Body></soap:Envelope>";

var response = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "OperationName\"")
    .POST(BodyPublishers.ofString(envelope)).build(), BodyHandlers.ofString());

String responseXml = response.body();

// Check for SOAP Fault in response
if (responseXml.contains("<soap:Fault>") || responseXml.contains("<faultstring>")) {
    // Parse faultstring and detail/ECGridOSSOAPErrorCode using an XML parser
    System.err.println("SOAP Fault received: " + responseXml);
    throw new RuntimeException("SOAP Fault: check responseXml for details");
}
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — detect SOAP faults in the raw XML response
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body><!-- operation here --></soap:Body>
</soap:Envelope>`;

const response = await fetch(endpoint, {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    SOAPAction: `"${ns}OperationName"`
  },
  body: envelope
});

const xml = await response.text();

// Check for SOAP Fault
if (xml.includes('<soap:Fault>') || xml.includes('<faultstring>')) {
  // Use an XML parser to extract faultstring and ECGridOSSOAPErrorCode
  throw new Error(`SOAP Fault received. Raw XML: ${xml.slice(0, 500)}`);
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — detect SOAP faults in the raw XML response
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:ecg="' + ns + '">'
    '<soap:Body><!-- operation here --></soap:Body></soap:Envelope>'
)

resp = requests.post(endpoint, data=envelope.encode(), headers={
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": f'"{ns}OperationName"'
})
resp.raise_for_status()

# Check for SOAP Fault
if "<soap:Fault>" in resp.text or "<faultstring>" in resp.text:
    # Use xml.etree.ElementTree to parse faultstring and ECGridOSSOAPErrorCode
    raise Exception(f"SOAP Fault received: {resp.text[:500]}")
```

</TabItem>
</Tabs>

---

## Retry Guidance

Not all errors are permanent. Use exponential backoff for transient failures.

### When to Retry

| Condition | Retry? | Strategy |
|---|---|---|
| `429 Too Many Requests` | Yes | Exponential backoff, honour `Retry-After` header if present |
| `500 Internal Server Error` | Yes | Exponential backoff, max 3 attempts |
| `503 Service Unavailable` | Yes | Exponential backoff, max 3 attempts |
| `401 Unauthorized` | No | Fix credentials — retrying will not help |
| `403 Forbidden` | No | Fix permissions — retrying will not help |
| `400 Bad Request` | No | Fix the request payload |
| `404 Not Found` | No | Verify the resource ID |

### C# Retry with Exponential Backoff

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
#!/usr/bin/env bash
# Exponential backoff retry for REST API calls
URL="https://rest.ecgrid.io/v2/parcels/pending-inbox-list"
MAX_ATTEMPTS=3
DELAY=1

for attempt in $(seq 1 $MAX_ATTEMPTS); do
  HTTP_CODE=$(curl -s -o /tmp/ecgrid_resp.json -w "%{http_code}" \
    -X POST "$URL" \
    -H "X-API-Key: $ECGRID_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"mailboxId":0,"pageNo":1,"recordsPerPage":25}')

  if [ "$HTTP_CODE" -eq 200 ]; then
    cat /tmp/ecgrid_resp.json
    exit 0
  fi

  if [ "$HTTP_CODE" -ne 429 ] && [ "$HTTP_CODE" -lt 500 ]; then
    echo "Non-retryable error: $HTTP_CODE" >&2
    cat /tmp/ecgrid_resp.json >&2
    exit 1
  fi

  echo "Attempt $attempt/$MAX_ATTEMPTS failed ($HTTP_CODE). Retrying in ${DELAY}s..." >&2
  sleep $DELAY
  DELAY=$((DELAY * 2))
done

echo "All $MAX_ATTEMPTS attempts failed." >&2
exit 1
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — simple exponential backoff helper
static async Task<HttpResponseMessage> SendWithRetryAsync(
    HttpClient http,
    Func<HttpRequestMessage> buildRequest,
    int maxAttempts = 3,
    CancellationToken ct = default)
{
    var delay = TimeSpan.FromSeconds(1);

    for (var attempt = 1; attempt <= maxAttempts; attempt++)
    {
        // Build a fresh HttpRequestMessage each attempt — messages cannot be reused
        var request  = buildRequest();
        var response = await http.SendAsync(request, ct);

        var isTransient =
            (int)response.StatusCode == 429 ||
            (int)response.StatusCode >= 500;

        if (!isTransient || attempt == maxAttempts)
            return response;

        // Honour Retry-After if the server provides it
        if (response.Headers.RetryAfter?.Delta is { } retryAfter)
            delay = retryAfter;

        await Task.Delay(delay, ct);
        delay *= 2; // double the delay each attempt
    }

    throw new InvalidOperationException("Retry loop exited without returning a response.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — exponential backoff retry
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;

static HttpResponse<String> sendWithRetry(
    HttpClient http, String url, String body, String apiKey,
    int maxAttempts) throws Exception {

    long delayMs = 1000;
    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
        var request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/json")
            .header("X-API-Key", apiKey)
            .POST(BodyPublishers.ofString(body))
            .build();

        var response = http.send(request, BodyHandlers.ofString());
        int status = response.statusCode();
        boolean isTransient = status == 429 || status >= 500;

        if (!isTransient || attempt == maxAttempts) return response;

        Thread.sleep(delayMs);
        delayMs *= 2; // double the delay each attempt
    }
    throw new IllegalStateException("Retry loop exited without returning.");
}
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — exponential backoff retry
async function fetchWithRetry(url, options, maxAttempts = 3) {
  let delay = 1000;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const response = await fetch(url, options);
    const isTransient = response.status === 429 || response.status >= 500;

    if (!isTransient || attempt === maxAttempts) return response;

    // Honour Retry-After header if provided
    const retryAfter = response.headers.get('Retry-After');
    const waitMs = retryAfter ? parseInt(retryAfter, 10) * 1000 : delay;

    await new Promise(resolve => setTimeout(resolve, waitMs));
    delay *= 2;
  }
}

// Usage
const response = await fetchWithRetry(
  'https://rest.ecgrid.io/v2/parcels/pending-inbox-list',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-API-Key': process.env.ECGRID_API_KEY },
    body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
  }
);
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — exponential backoff retry
import time, os, requests

def post_with_retry(url, payload, api_key, max_attempts=3):
    delay = 1.0
    for attempt in range(1, max_attempts + 1):
        resp = requests.post(url,
            json=payload,
            headers={"X-API-Key": api_key, "Content-Type": "application/json"})

        is_transient = resp.status_code == 429 or resp.status_code >= 500
        if not is_transient or attempt == max_attempts:
            return resp

        retry_after = resp.headers.get("Retry-After")
        wait = float(retry_after) if retry_after else delay
        time.sleep(wait)
        delay *= 2
    raise RuntimeError("Retry loop exited without returning.")

# Usage
response = post_with_retry(
    "https://rest.ecgrid.io/v2/parcels/pending-inbox-list",
    {"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25},
    os.environ["ECGRID_API_KEY"]
)
```

</TabItem>
</Tabs>

---

## Common Troubleshooting Scenarios

### 401 Unauthorized on every REST request

**Likely cause:** The API key is not being sent, or the header name is wrong.

**Check:** The header must be spelled exactly `X-API-Key` (case-sensitive on some proxies):

```http
X-API-Key: your-api-key-here
```

Not `x-api-key`, `APIKey`, or `Authorization: ApiKey ...`.

---

### 403 Forbidden when calling a management endpoint

**Likely cause:** The authenticated user's `AuthLevel` is insufficient for the operation.

**Check:** Verify the user's `AuthLevel` using `GET /v2/users/me` (REST) or `WhoAmI()` (SOAP). Operations on network-level resources require at least `NetworkAdmin`.

See [AuthLevel values](../appendix/enums.md#authlevel) in the Enums appendix.

---

### Inbox list returns empty — no parcels

**Check the following in order:**

1. You are querying the correct `mailboxID`. Use `GET /v2/users/me` to confirm the default mailbox ID for your session.
2. Files may already have been downloaded and confirmed. Confirmed parcels no longer appear in the default inbox list.

---

### SOAP session expired mid-process

**Cause:** ECGridOS sessions expire after a period of inactivity. For long-running batch processes, session expiry can occur between calls.

**Fix:** Catch `FaultException` with a session-related fault code and re-authenticate:

```csharp
// Re-login on session expiry — simplified pattern
catch (FaultException fault) when (fault.Message.Contains("SessionID", StringComparison.OrdinalIgnoreCase))
{
    sessionID = await client.LoginAsync(email, password);
    // Retry the failed operation
}
```

For persistent processes, prefer a REST API key which never expires.

---

### dotnet-svcutil proxy throws CommunicationException

**Check:** Ensure `System.ServiceModel.Http` NuGet package is installed and the endpoint URL is correct:

```
https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx
```

Not `http://` — the service requires TLS.

---

## Related

- [Error Codes](../appendix/error-codes.md)
- [Enums — AuthLevel](../appendix/enums.md)
- [Authentication & Session Management](./authentication.md)
- [Connecting via SOAP](./connecting-via-soap.md)
