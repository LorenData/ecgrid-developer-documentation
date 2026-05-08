---
title: Acknowledgment Note
sidebar_position: 14
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/acknowledgment-note.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Acknowledgment Note

Attach a free-text acknowledgment note to a parcel record for auditing or communication purposes.

## Endpoint

```http
POST /v2/parcels/acknowledgment-note
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `parcelId` | long | Yes | | Unique identifier of the parcel |
| `note` | string | Yes | Non-empty | Acknowledgment text to attach to the parcel |

```json
{
  "parcelId": 987654321,
  "note": "Received and processed by AP system at 2026-05-07T10:15:00Z."
}
```

## Response

Returns a success boolean indicating the note was attached to the parcel record.

```json
{
  "success": true,
  "data": true
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/acknowledgment-note" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "parcelId": 987654321, "note": "Received and processed by AP system at 2026-05-07T10:15:00Z." }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — attach an acknowledgment note to a parcel after business processing
using System.Net.Http.Json;

var noteRequest = new
{
    parcelId = 987654321L,
    note = $"Processed by AP system at {DateTime.UtcNow:O}."
};

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/acknowledgment-note",
    noteRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
if (result!.Data)
{
    Console.WriteLine($"Acknowledgment note attached to parcel {noteRequest.parcelId}.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"parcelId\": 987654321, \"note\": \"Received and processed by AP system at 2026-05-07T10:15:00Z.\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/acknowledgment-note"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(body))
    .build();

HttpClient client = HttpClient.newHttpClient();
HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString());

System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
const apiKey = process.env.ECGRID_API_KEY;
const url = 'https://rest.ecgrid.io/v2/parcels/acknowledgment-note';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "parcelId": 987654321, "note": "Received and processed by AP system at 2026-05-07T10:15:00Z." }),
});

const data = await response.json();
console.log(data);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
headers = {"X-API-Key": api_key}
url = "https://rest.ecgrid.io/v2/parcels/acknowledgment-note"

response = requests.post(
    url,
    json={ "parcelId": 987654321, "note": "Received and processed by AP system at 2026-05-07T10:15:00Z." },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Parcel](./get-parcel) — retrieve the parcel record the note is attached to
- [Confirm Download](./confirm-download) — confirm delivery before attaching a note
