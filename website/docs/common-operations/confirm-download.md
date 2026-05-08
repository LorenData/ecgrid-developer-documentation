---
title: Confirm a Download
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create confirm-download common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Confirm a Download

Mark a downloaded parcel as delivered so ECGrid removes it from your inbox and stops re-delivering it on subsequent polls.

## Overview

ECGrid uses an explicit confirmation step to provide at-least-once delivery guarantees. When you download a parcel its status changes temporarily, but it is **not removed from the inbox** until you confirm the download. If your process crashes before confirming, ECGrid will re-deliver the parcel on the next poll — protecting you from silent data loss.

**The rule is simple:** save the file to durable storage first, then confirm.

Sequence:
1. Download the parcel and write bytes to disk *(see [Download a File](./download-a-file))*.
2. Verify the write succeeded (file exists, correct size, or parsed without error).
3. Call the confirm endpoint with the `parcelId`.
4. ECGrid sets the parcel status to `InBoxTransferred` and will not re-deliver it.

:::danger Do Not Confirm Before Saving
Only confirm after you have durably saved or successfully processed the file. Confirming a parcel you have not yet saved will result in permanent data loss — ECGrid will not re-deliver it.
:::

---

## REST

**Endpoint:** `POST /v2/parcels/confirm`

**Auth:** `X-API-Key: <key>` header

### Step 1 — Send the confirm request

```http
POST https://rest.ecgrid.io/v2/parcels/confirm
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "parcelId": 98765
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `parcelId` | integer (long) | Yes | The ID of the parcel you have already downloaded and saved. |

### Step 2 — Verify the response

```json
{
  "success": true,
  "data": {
    "parcelId": 98765,
    "status": "InBoxTransferred"
  }
}
```

A `success: true` response means ECGrid has recorded the confirmation. The parcel will no longer appear in subsequent `InBoxReady` inbox list responses.

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -s -X POST https://rest.ecgrid.io/v2/parcels/confirm \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"parcelId":98765}' | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — confirm a downloaded parcel using IHttpClientFactory
// "ECGrid" named client is registered with base address and X-API-Key header

using System.Net.Http.Json;

public record ConfirmRequest(long ParcelId);

public record ConfirmData(long ParcelId, string Status);

public record ConfirmResponse(bool Success, ConfirmData Data);

public class ECGridDownloadConfirmer
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridDownloadConfirmer> _logger;

    public ECGridDownloadConfirmer(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridDownloadConfirmer> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Confirms that a parcel has been received. Call this only after the file has been
    /// durably saved. Returns true on success; throws on HTTP or API error.
    /// </summary>
    public async Task<bool> ConfirmAsync(
        long parcelId,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        var response = await http.PostAsJsonAsync(
            "/v2/parcels/confirm",
            new ConfirmRequest(parcelId),
            cancellationToken);

        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ConfirmResponse>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from confirm endpoint.");

        if (!result.Success)
        {
            _logger.LogWarning("Confirm returned success=false for parcelId={ParcelId}", parcelId);
            return false;
        }

        _logger.LogInformation(
            "Confirmed parcelId={ParcelId}, new status={Status}",
            parcelId, result.Data.Status);

        return true;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — confirm a downloaded parcel
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
long parcelId = 98765L;

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/confirm"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"parcelId\":" + parcelId + "}"))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.statusCode()); // 200 = confirmed
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — confirm a downloaded parcel
const apiKey = process.env.ECGRID_API_KEY;
const parcelId = 98765;

const response = await fetch('https://rest.ecgrid.io/v2/parcels/confirm', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ parcelId })
});

const result = await response.json();
console.log(result.data.status); // "InBoxTransferred"
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
parcel_id = 98765

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/confirm",
    headers={"X-API-Key": api_key},
    json={"parcelId": parcel_id}
)
resp.raise_for_status()
print(resp.json()["data"]["status"])  # "InBoxTransferred"
```

</TabItem>
</Tabs>

**Typical usage — save then confirm:**

```csharp
// Download
string savedPath = await downloader.DownloadToFileAsync(parcel.ParcelId, outputDir, ct);

// Only confirm after the file is durably on disk
bool confirmed = await confirmer.ConfirmAsync(parcel.ParcelId, ct);

if (!confirmed)
    logger.LogError("Failed to confirm parcelId={Id} — will retry on next poll", parcel.ParcelId);
```

:::tip Idempotency
Calling confirm more than once on the same `parcelId` is safe — subsequent calls are no-ops and will still return `success: true`.
:::

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Method:** `ParcelDownloadConfirm(SessionID, ParcelID)` → `bool`

### Step 1 — Call ParcelDownloadConfirm

```csharp
var result = await client.ParcelDownloadConfirmAsync(sessionId, parcelId);
bool confirmed = result.ParcelDownloadConfirmResult;
```

Returns `true` if the confirmation was recorded, `false` if it failed (e.g., parcel not found or already confirmed by another session).

### Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Reference: https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

using ECGridOS;

/// <summary>
/// Downloads a parcel, saves it to disk, and confirms delivery.
/// Confirmation is only sent after the file write succeeds.
/// </summary>
public static async Task DownloadAndConfirmAsync(
    ECGridOSAPIClient client,
    string sessionId,
    int parcelId,
    string outputDirectory)
{
    // Download the file bytes
    var downloadResult = await client.ParcelDownloadAsync(sessionId, parcelId);
    byte[] fileBytes = downloadResult.ParcelDownloadResult;

    // Retrieve filename from parcel info
    var infoResult = await client.ParcelInfoAsync(sessionId, parcelId);
    string safeFileName = Path.GetFileName(infoResult.ParcelInfoResult.FileName);
    string outputPath   = Path.Combine(outputDirectory, safeFileName);

    // Write to disk — confirm only if this succeeds
    await File.WriteAllBytesAsync(outputPath, fileBytes);
    Console.WriteLine($"Saved {outputPath} ({fileBytes.Length} bytes)");

    // Confirm delivery
    var confirmResult = await client.ParcelDownloadConfirmAsync(sessionId, parcelId);
    bool confirmed = confirmResult.ParcelDownloadConfirmResult;

    if (confirmed)
        Console.WriteLine($"Confirmed parcelId={parcelId}");
    else
        Console.Error.WriteLine($"WARNING: confirmation failed for parcelId={parcelId}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP ParcelDownloadConfirm via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
String parcelId  = "98765";

String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:ParcelDownloadConfirm>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:ParcelID>" + parcelId + "</ecg:ParcelID>"
    + "</ecg:ParcelDownloadConfirm></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/ParcelDownloadConfirm\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // true = confirmed
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP ParcelDownloadConfirm via raw HTTP
const sessionId = 'YOUR_SESSION_ID';
const parcelId  = '98765';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelDownloadConfirm>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:ParcelID>${parcelId}</ecg:ParcelID>
  </ecg:ParcelDownloadConfirm></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelDownloadConfirm"'
  },
  body: envelope
});
console.log(await response.text()); // true = confirmed
```

</TabItem>
<TabItem value="python" label="Python">

```python
import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login
parcel_id  = "98765"

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelDownloadConfirm>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:ParcelID>' + parcel_id + '</ecg:ParcelID>'
    '</ecg:ParcelDownloadConfirm></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelDownloadConfirm"'}
)
resp.raise_for_status()
print(resp.text)  # true = confirmed
```

</TabItem>
</Tabs>

---

## Why Confirmation Matters

| Scenario | Without Confirm | With Confirm |
|---|---|---|
| Normal operation | Parcel re-appears on every poll | Parcel removed from inbox after first successful download |
| Process crash after download | File may be lost with no re-delivery | Re-delivered on next poll — no data loss |
| Network error during confirm call | Parcel re-delivered on next poll | Re-delivered — idempotent, safe to process again |
| Double-confirm (retry safe) | N/A | Second confirm is a no-op |

---

## Related

- [Download a File](./download-a-file)
- [Poll for Inbound Files](./poll-inbound-files)
- [REST — Parcels: Confirm Download](../rest-api/parcels/confirm-download)
- [SOAP — ParcelDownloadConfirm](../soap-api/parcels/parcel-download-confirm)
