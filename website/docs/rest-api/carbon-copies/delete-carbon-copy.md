---
title: Delete Carbon Copy
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Delete Carbon Copy REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Delete Carbon Copy

Permanently deletes a carbon copy rule, stopping all future traffic duplication for that rule.

## Endpoint

```http
DELETE /v2/carboncopies/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | Unique identifier of the carbon copy rule to delete |

## Response

Returns a success boolean confirming the deletion.

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
curl -X DELETE "https://rest.ecgrid.io/v2/carboncopies/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Delete a carbon copy rule
using var response = await httpClient.DeleteAsync(
    $"https://rest.ecgrid.io/v2/carboncopies/{ccId}");

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();

if (result.Data)
{
    Console.WriteLine($"Carbon copy rule {ccId} successfully deleted.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/carboncopies/%s", id)))
    .header("X-API-Key", apiKey)
    .DELETE()
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
const url = `https://rest.ecgrid.io/v2/carboncopies/${id}`;

const response = await fetch(url, {
  method: 'DELETE',
  headers: { 'X-API-Key': apiKey },
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
id = 0  # replace with actual id
url = f"https://rest.ecgrid.io/v2/carboncopies/{id}"

response = requests.delete(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Carbon Copy](./get-carbon-copy)
- [Create Carbon Copy](./create-carbon-copy)
- [List Carbon Copies](./list-carbon-copies)
- [Update Carbon Copy](./update-carbon-copy)
