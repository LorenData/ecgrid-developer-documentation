---
title: Java
sidebar_position: 5
---

{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-06-17: Code examples section - Christian Nichols */}

# Java Examples

These examples use the Java 11+ `HttpClient` from the standard library. No third-party dependencies required.

**Base URL:** `https://rest.ecgrid.io`

---

## Setup

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class ECGridClient {

    private static final String BASE_URL = "https://rest.ecgrid.io";

    private final HttpClient http;
    private final String apiKey;
    private String sessionKey;

    public ECGridClient(String apiKey) {
        this.apiKey = apiKey;
        this.http = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .build();
    }

    private HttpRequest.Builder requestBuilder(String path) {
        var builder = HttpRequest.newBuilder()
            .uri(URI.create(BASE_URL + path))
            .header("Content-Type", "application/json");

        if (sessionKey != null) {
            builder.header("Authorization", "Bearer " + sessionKey);
        }

        return builder;
    }

    private HttpResponse<String> send(HttpRequest request) throws Exception {
        var response = http.send(request, HttpResponse.BodyHandlers.ofString());

        // Re-authenticate on 401 and retry once
        if (response.statusCode() == 401) {
            login();
            // Rebuild request with updated session key
            var retried = HttpRequest.newBuilder(request, (n, v) -> true)
                .header("Authorization", "Bearer " + sessionKey)
                .build();
            response = http.send(retried, HttpResponse.BodyHandlers.ofString());
        }

        return response;
    }

    public HttpResponse<String> post(String path, String json) throws Exception {
        var request = requestBuilder(path)
            .POST(HttpRequest.BodyPublishers.ofString(json))
            .build();
        return send(request);
    }

    public HttpResponse<String> get(String path) throws Exception {
        var request = requestBuilder(path).GET().build();
        return send(request);
    }
}
```

---

## Authentication

```java
import org.json.JSONObject; // or use Jackson / Gson for JSON parsing

public String login() throws Exception {
    String body = """
        { "apiKey": "YOUR_API_KEY" }
        """;

    var request = HttpRequest.newBuilder()
        .uri(URI.create(BASE_URL + "/v2/auth/login"))
        .header("Content-Type", "application/json")
        .POST(HttpRequest.BodyPublishers.ofString(body))
        .build();

    var response = http.send(request, HttpResponse.BodyHandlers.ofString());

    if (response.statusCode() != 200) {
        throw new RuntimeException("Login failed: " + response.statusCode());
    }

    var result = new JSONObject(response.body());
    sessionKey = result.getJSONObject("data").getString("sessionKey");
    System.out.println("Session key: " + sessionKey);
    return sessionKey;
}
```

> **Note:** These examples use `org.json` for JSON parsing. You can substitute Jackson (`ObjectMapper`) or Gson — the HTTP layer stays the same.

---

## Mailboxes

### Get a mailbox by ID

```java
// GET /v2/mailboxes/{id}
var response = client.get("/v2/mailboxes/1234");

if (response.statusCode() == 200) {
    var result = new JSONObject(response.body());
    var mailbox = result.getJSONObject("data");

    System.out.println("Mailbox: " + mailbox.getString("mailboxName"));
    System.out.println("Network: " + mailbox.getString("networkName"));
}
```

### List mailboxes on a network

```java
// POST /v2/mailboxes/list
String body = """
    {
        "networkId":    5050,
        "mailboxId":    0,
        "showInactive": false
    }
    """;

var response = client.post("/v2/mailboxes/list", body);

if (response.statusCode() == 200) {
    var result = new JSONObject(response.body());
    var mailboxes = result.getJSONArray("data");

    for (int i = 0; i < mailboxes.length(); i++) {
        var mb = mailboxes.getJSONObject(i);
        System.out.println(mb.getInt("mailboxId") + ": " + mb.getString("mailboxName"));
    }
}
```

---

## Interchanges

### List inbound interchanges

```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

// POST /v2/interchanges/inbox-list
String today    = LocalDate.now().format(DateTimeFormatter.ISO_DATE);
String weekAgo  = LocalDate.now().minusDays(7).format(DateTimeFormatter.ISO_DATE);

String body = String.format("""
    {
        "networkId": 5050,
        "mailboxId": 0,
        "startDate": "%s",
        "endDate":   "%s",
        "pageSize":  50,
        "pageIndex": 1
    }
    """, weekAgo, today);

var response = client.post("/v2/interchanges/inbox-list", body);

if (response.statusCode() == 200) {
    var result = new JSONObject(response.body());
    var items  = result.getJSONArray("data");

    for (int i = 0; i < items.length(); i++) {
        var ix = items.getJSONObject(i);
        System.out.printf("ID: %d | From: %s | %s%n",
            ix.getLong("interchangeId"),
            ix.getString("senderEDIId"),
            ix.getString("statusDescription"));
    }
}
```

---

## Callbacks

### Create a webhook callback

```java
// POST /v2/callbacks/create
String body = """
    {
        "networkId":          5050,
        "mailboxId":          0,
        "userId":             1001,
        "systemObject":       "Interchange",
        "objectStatus":       5,
        "direction":          "InBox",
        "frequency":          60,
        "maxRetries":         24,
        "url":                "https://your-system.com/webhook/ecgrid",
        "httpAuthentication": null,
        "status":             "Active"
    }
    """;

var response = client.post("/v2/callbacks/create", body);

if (response.statusCode() == 200) {
    var result  = new JSONObject(response.body());
    var eventId = result.getJSONObject("data").getInt("callBackEventId");
    System.out.println("Callback created. Event ID: " + eventId);
}
```

### List callbacks for a mailbox

```java
// POST /v2/callbacks/event-list
String body = """
    {
        "networkId":    5050,
        "mailboxId":    0,
        "showInactive": false
    }
    """;

var response = client.post("/v2/callbacks/event-list", body);

if (response.statusCode() == 200) {
    var result    = new JSONObject(response.body());
    var callbacks = result.getJSONArray("data");

    for (int i = 0; i < callbacks.length(); i++) {
        var cb = callbacks.getJSONObject(i);
        System.out.printf("Event %d: %s [%s]%n",
            cb.getInt("callBackEventId"),
            cb.getString("url"),
            cb.getString("statusDescription"));
    }
}
```

---

## Keys (Metadata)

### Create a metadata key

```java
// POST /v2/keys/create
String body = """
    {
        "key":          "integration.vendorCode",
        "systemObject": "Mailbox",
        "objectId":     1234,
        "visibility":   "Private",
        "value":        "ACME-001",
        "meta":         "Vendor code for ACME Corp integration",
        "daysToLive":   -1
    }
    """;

var response = client.post("/v2/keys/create", body);
System.out.println("Key created. Status: " + response.statusCode());
```

### List all keys on an object

```java
// POST /v2/keys/list
String body = """
    {
        "systemObject": "Mailbox",
        "objectId":     1234
    }
    """;

var response = client.post("/v2/keys/list", body);

if (response.statusCode() == 200) {
    var result = new JSONObject(response.body());
    var keys   = result.getJSONArray("data");

    for (int i = 0; i < keys.length(); i++) {
        var k = keys.getJSONObject(i);
        System.out.println(k.getString("key") + ": " + k.getString("value"));
    }
}
```

---

## Error Handling

Non-2xx responses carry an RFC 7807 problem body:

```java
var response = client.post("/v2/mailboxes/list", body);

if (!isSuccess(response.statusCode())) {
    var error   = new JSONObject(response.body());
    String title   = error.optString("title",   "Unknown error");
    String detail  = error.optString("detail",  "");
    String traceId = error.optString("traceId", "");

    System.err.printf("Error %d: %s%n", response.statusCode(), title);
    System.err.println("Detail:   " + detail);
    System.err.println("Trace ID: " + traceId);
    // Include traceId when contacting ECGrid support
}

private static boolean isSuccess(int statusCode) {
    return statusCode >= 200 && statusCode < 300;
}
```
