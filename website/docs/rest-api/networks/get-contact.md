---
title: Get Network Contact
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created POST /v2/networks/get-contact reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Network Contact

Retrieves the contact information associated with a specific contact role for a given network.

## Endpoint

```http
POST /v2/networks/get-contact
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `networkId` | integer | Yes | — | ID of the network to query |
| `contactType` | string | Yes | See [`NetworkContactType`](#networkcontacttype) | The role category of the contact to retrieve |

```json
{
  "networkId": 1001,
  "contactType": "CustomerService"
}
```

## Response

Returns the contact details for the requested contact role on the network.

```json
{
  "success": true,
  "data": {
    "networkId": 1001,
    "contactType": "CustomerService",
    "name": "Jane Smith",
    "email": "support@acme.example.com",
    "phone": "312-555-0199"
  },
  "errorCode": null,
  "message": null
}
```

## ENUMs

### NetworkContactType

The `contactType` field uses the `NetworkContactType` enum. See the full value table in [Appendix: ENUMs](../../appendix/enums#networkcontacttype).

| Value | Description |
|---|---|
| `Owner` | Primary account owner |
| `Errors` | Recipient for error notifications |
| `Interconnects` | Contact for partner interconnect requests |
| `Notices` | General system notices |
| `Reports` | Recipient for scheduled reports |
| `Accounting` | Billing and invoicing contact |
| `CustomerService` | Customer-facing support contact |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/networks/get-contact" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "networkId": 1001, "contactType": "CustomerService" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve the accounting contact for a network
var payload = new
{
    networkId = 1001,
    contactType = "Accounting"
};

var request = new HttpRequestMessage(HttpMethod.Post, "https://rest.ecgrid.io/v2/networks/get-contact")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<NetworkContactInfo>>();
Console.WriteLine($"Accounting contact: {result?.Data?.Name} — {result?.Data?.Email}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"networkId\": 1001, \"contactType\": \"CustomerService\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/networks/get-contact"))
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
const url = 'https://rest.ecgrid.io/v2/networks/get-contact';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "networkId": 1001, "contactType": "CustomerService" }),
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
url = "https://rest.ecgrid.io/v2/networks/get-contact"

response = requests.post(
    url,
    json={ "networkId": 1001, "contactType": "CustomerService" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Network](./get-network)
- [Update Network](./update-network)
- [Appendix: ENUMs](../../appendix/enums)
