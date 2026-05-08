---
title: Update Network
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created PUT /v2/networks reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Network

Updates the profile information for an existing ECGrid network.

## Endpoint

```http
PUT /v2/networks
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `networkId` | integer | Yes | — | ID of the network to update |
| `companyName` | string | No | — | Legal company name for the network |
| `address1` | string | No | — | Street address line 1 |
| `address2` | string | No | — | Street address line 2 (suite, floor, etc.) |
| `city` | string | No | — | City |
| `state` | string | No | 2-char code | State or province abbreviation |
| `zip` | string | No | — | Postal / ZIP code |
| `phone` | string | No | — | Primary contact phone number |
| `website` | string | No | Valid URL | Public website URL |

```json
{
  "networkId": 1001,
  "companyName": "Acme Corporation",
  "address1": "123 Commerce Way",
  "address2": "Suite 400",
  "city": "Chicago",
  "state": "IL",
  "zip": "60601",
  "phone": "312-555-0100",
  "website": "https://www.acme.example.com"
}
```

## Response

Returns the updated `NetworkIDInfo` object reflecting the saved values.

```json
{
  "success": true,
  "data": {
    "networkId": 1001,
    "uniqueId": "MYNETWORK",
    "companyName": "Acme Corporation",
    "status": "Active",
    "created": "2020-03-15T08:00:00Z",
    "modified": "2026-05-07T10:45:00Z"
  },
  "errorCode": null,
  "message": null
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X PUT "https://rest.ecgrid.io/v2/networks" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "networkId": 1001, "companyName": "Acme Corporation", "address1": "123 Commerce Way", "address2": "Suite 400", "city": "Chicago", "state": "IL", "zip": "60601", "phone": "312-555-0100", "website": "https://www.acme.example.com" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — update network company name and address
var payload = new
{
    networkId = 1001,
    companyName = "Acme Corporation",
    address1 = "123 Commerce Way",
    address2 = "Suite 400",
    city = "Chicago",
    state = "IL",
    zip = "60601",
    phone = "312-555-0100",
    website = "https://www.acme.example.com"
};

var request = new HttpRequestMessage(HttpMethod.Put, "https://rest.ecgrid.io/v2/networks")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<NetworkIdInfo>>();
Console.WriteLine($"Updated: {result?.Data?.CompanyName} at {result?.Data?.Modified}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"networkId\": 1001, \"companyName\": \"Acme Corporation\", \"address1\": \"123 Commerce Way\", \"address2\": \"Suite 400\", \"city\": \"Chicago\", \"state\": \"IL\", \"zip\": \"60601\", \"phone\": \"312-555-0100\", \"website\": \"https://www.acme.example.com\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/networks"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .PUT(HttpRequest.BodyPublishers.ofString(body))
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
const url = 'https://rest.ecgrid.io/v2/networks';

const response = await fetch(url, {
  method: 'PUT',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "networkId": 1001, "companyName": "Acme Corporation", "address1": "123 Commerce Way", "address2": "Suite 400", "city": "Chicago", "state": "IL", "zip": "60601", "phone": "312-555-0100", "website": "https://www.acme.example.com" }),
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
url = "https://rest.ecgrid.io/v2/networks"

response = requests.put(
    url,
    json={ "networkId": 1001, "companyName": "Acme Corporation", "address1": "123 Commerce Way", "address2": "Suite 400", "city": "Chicago", "state": "IL", "zip": "60601", "phone": "312-555-0100", "website": "https://www.acme.example.com" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Network](./get-network)
- [List Networks](./list-networks)
- [Update Network Config](./update-config)
