---
title: SOAP HttpClient Sample
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP HttpClient sample documentation page - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs to SOAP HttpClient sample key patterns - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# SOAP HttpClient Sample

The `ECGrid-SOAP-dotnet10-Console-HttpClient` project demonstrates calling the ECGridOS SOAP API without a generated proxy. Instead, SOAP envelopes are constructed manually using `XDocument` and sent with `HttpClient`. This approach gives maximum control and has minimal dependencies.

:::caution Established API
The ECGridOS SOAP API is in maintenance mode. For new integrations, use the [REST API](../rest-api/overview.md) instead. This sample is provided for teams maintaining or migrating existing SOAP-based integrations.
:::

## Project Location

```
samples/soap/ECGrid-SOAP-dotnet10-Console-HttpClient/
```

## What It Demonstrates

- Constructing SOAP 1.1 envelopes with `XDocument`
- Sending SOAP requests with `HttpClient` and the correct `SOAPAction` header
- Parsing SOAP response XML with LINQ to XML
- Full session lifecycle: Login → operations → Logout
- Operations covered: `Login`, `ParcelInBox`, `ParcelDownload`, `ParcelDownloadConfirm`, `Logout`

## SOAP Endpoint Details

| Property | Value |
|---|---|
| Endpoint | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx` |
| XML Namespace | `http://www.ecgridos.net/` |
| SOAP Version | SOAP 1.1 |
| Content-Type | `text/xml; charset=utf-8` |

## Key Files

| File | Purpose |
|---|---|
| `Program.cs` | Entry point — full session workflow |
| `SoapClient.cs` | Reusable helper for sending SOAP envelopes |
| `appsettings.json` | Login credentials and endpoint URL |

## Key Patterns

### SOAP Envelope Construction

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
/// <summary>
/// Builds a SOAP 1.1 envelope wrapping a single operation element.
/// </summary>
private static XDocument BuildEnvelope(string methodName, string ns, params (string Name, string Value)[] parameters)
{
    var soapNs = XNamespace.Get("http://schemas.xmlsoap.org/soap/envelope/");
    var apiNs  = XNamespace.Get(ns);

    // SOAP body element containing the operation and its parameters
    var bodyContent = new XElement(apiNs + methodName,
        parameters.Select(p => new XElement(apiNs + p.Name, p.Value)));

    return new XDocument(
        new XElement(soapNs + "Envelope",
            new XAttribute(XNamespace.Xmlns + "soap", soapNs),
            new XAttribute(XNamespace.Xmlns + "ecg",  apiNs),
            new XElement(soapNs + "Body", bodyContent)));
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — build a SOAP 1.1 envelope for any ECGridOS method
String buildEnvelope(String methodName, String ns, java.util.Map<String, String> params) {
    var sb = new StringBuilder();
    sb.append("<?xml version=\"1.0\" encoding=\"utf-8\"?>");
    sb.append("<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" ");
    sb.append("xmlns:ecg=\"").append(ns).append("\">");
    sb.append("<soap:Body><ecg:").append(methodName).append(">");
    for (var entry : params.entrySet()) {
        sb.append("<ecg:").append(entry.getKey()).append(">");
        sb.append(entry.getValue());
        sb.append("</ecg:").append(entry.getKey()).append(">");
    }
    sb.append("</ecg:").append(methodName).append(">");
    sb.append("</soap:Body></soap:Envelope>");
    return sb.toString();
}

// Example: build a Login envelope
var loginEnv = buildEnvelope("Login", "http://www.ecgridos.net/",
    java.util.Map.of("Email", "user@example.com", "Password", "YourPassword1!"));
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — build a SOAP 1.1 envelope for any ECGridOS method
function buildEnvelope(methodName, ns, params) {
  const paramXml = Object.entries(params)
    .map(([k, v]) => `<ecg:${k}>${v}</ecg:${k}>`)
    .join('');

  return `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>
    <ecg:${methodName}>
      ${paramXml}
    </ecg:${methodName}>
  </soap:Body>
</soap:Envelope>`;
}

// Example: build a Login envelope
const loginEnv = buildEnvelope('Login', 'http://www.ecgridos.net/', {
  Email: 'user@example.com',
  Password: 'YourPassword1!'
});
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — build a SOAP 1.1 envelope for any ECGridOS method
def build_envelope(method_name, ns, **params):
    param_xml = "".join(
        f"<ecg:{k}>{v}</ecg:{k}>" for k, v in params.items()
    )
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        f'xmlns:ecg="{ns}">'
        f'<soap:Body><ecg:{method_name}>{param_xml}</ecg:{method_name}></soap:Body>'
        '</soap:Envelope>'
    )

# Example: build a Login envelope
ns = "http://www.ecgridos.net/"
login_env = build_envelope("Login", ns,
    Email="user@example.com",
    Password="YourPassword1!")
```

</TabItem>
</Tabs>

### Sending a SOAP Request

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
private const string EcgNs       = "http://www.ecgridos.net/";
private const string EndpointUrl = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";

/// <summary>
/// Posts a SOAP envelope and returns the parsed response document.
/// </summary>
private static async Task<XDocument> PostSoapAsync(
    HttpClient http, string methodName, XDocument envelope)
{
    var body = new StringContent(
        envelope.ToString(),
        System.Text.Encoding.UTF8,
        "text/xml");

    // SOAPAction header is required by SOAP 1.1; value identifies the operation
    body.Headers.Add("SOAPAction", $"\"{EcgNs}{methodName}\"");

    var response = await http.PostAsync(EndpointUrl, body);
    response.EnsureSuccessStatusCode();

    var xml = await response.Content.ReadAsStringAsync();
    return XDocument.Parse(xml);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — send a SOAP request and return the response body
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

static final String ECG_NS       = "http://www.ecgridos.net/";
static final String ENDPOINT_URL = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";

String postSoap(HttpClient http, String methodName, String envelope) throws Exception {
    var request = HttpRequest.newBuilder()
        .uri(URI.create(ENDPOINT_URL))
        .header("Content-Type", "text/xml; charset=utf-8")
        .header("SOAPAction", "\"" + ECG_NS + methodName + "\"")
        .POST(BodyPublishers.ofString(envelope))
        .build();

    var response = http.send(request, BodyHandlers.ofString());
    if (response.statusCode() >= 400)
        throw new RuntimeException("SOAP HTTP error: " + response.statusCode());

    return response.body(); // parse XML for the result element
}
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — send a SOAP request and return the response XML
const ECG_NS       = 'http://www.ecgridos.net/';
const ENDPOINT_URL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';

async function postSoap(methodName, envelope) {
  const response = await fetch(ENDPOINT_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/xml; charset=utf-8',
      SOAPAction: `"${ECG_NS}${methodName}"`
    },
    body: envelope
  });

  if (!response.ok)
    throw new Error(`SOAP HTTP error: ${response.status}`);

  return response.text(); // parse XML for the result element
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — send a SOAP request and return the response XML
import requests

ECG_NS       = "http://www.ecgridos.net/"
ENDPOINT_URL = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"

def post_soap(method_name, envelope):
    resp = requests.post(ENDPOINT_URL,
        data=envelope.encode("utf-8"),
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f'"{ECG_NS}{method_name}"'
        })
    resp.raise_for_status()
    return resp.text  # parse XML for the result element
```

</TabItem>
</Tabs>

### Session Lifecycle

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// Program.cs — .NET 10 top-level statements

// Load credentials from IConfiguration — never hardcoded
var config = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddUserSecrets<Program>()
    .Build();

using var http = new HttpClient();   // Console sample — single instance is acceptable here

// --- Login ---
var loginEnvelope = BuildEnvelope("Login", EcgNs,
    ("Login",    config["ECGridOS:Login"]!),
    ("Password", config["ECGridOS:Password"]!));

var loginResponse = await PostSoapAsync(http, "Login", loginEnvelope);

XNamespace ns = EcgNs;
// Extract the session ID from the Login response
var sessionId = loginResponse
    .Descendants(ns + "LoginResult")
    .First().Value;

// --- Check inbox ---
var inboxEnvelope = BuildEnvelope("ParcelInBox", EcgNs,
    ("SessionID", sessionId),
    ("MailboxID", config["ECGridOS:MailboxId"]!));

var inboxResponse = await PostSoapAsync(http, "ParcelInBox", inboxEnvelope);

foreach (var parcel in inboxResponse.Descendants(ns + "ParcelIDInfo"))
{
    var parcelId = parcel.Element(ns + "ParcelID")!.Value;

    // --- Download parcel ---
    var downloadEnvelope = BuildEnvelope("ParcelDownload", EcgNs,
        ("SessionID", sessionId),
        ("ParcelID",  parcelId));

    var downloadResponse = await PostSoapAsync(http, "ParcelDownload", downloadEnvelope);
    var base64Content = downloadResponse
        .Descendants(ns + "ParcelDownloadResult")
        .First().Value;

    var ediBytes = Convert.FromBase64String(base64Content);
    await File.WriteAllBytesAsync($"parcel-{parcelId}.edi", ediBytes);

    // --- Confirm download ---
    var confirmEnvelope = BuildEnvelope("ParcelDownloadConfirm", EcgNs,
        ("SessionID", sessionId),
        ("ParcelID",  parcelId));

    await PostSoapAsync(http, "ParcelDownloadConfirm", confirmEnvelope);
}

// --- Logout ---
var logoutEnvelope = BuildEnvelope("Logout", EcgNs, ("SessionID", sessionId));
await PostSoapAsync(http, "Logout", logoutEnvelope);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — full SOAP session lifecycle: Login → ParcelInBox → Download → Confirm → Logout
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login
String loginEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email><ecg:Password>pass</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";
var loginResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "Login\"")
    .POST(BodyPublishers.ofString(loginEnv)).build(), BodyHandlers.ofString());
// Extract sessionId from loginResp.body() using an XML parser (e.g. javax.xml)
String sessionId = "...";

// ParcelInBox — iterate results and download/confirm each
// ... build envelopes for ParcelInBox, ParcelDownload, ParcelDownloadConfirm

// Logout
String logoutEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><ecg:Logout><ecg:SessionID>" + sessionId + "</ecg:SessionID></ecg:Logout>"
    + "</soap:Body></soap:Envelope>";
http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "Logout\"")
    .POST(BodyPublishers.ofString(logoutEnv)).build(), BodyHandlers.discarding());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — full SOAP session lifecycle: Login → ParcelInBox → Download → Confirm → Logout
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

async function soapCall(action, body) {
  const env = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>${body}</soap:Body>
</soap:Envelope>`;
  const r = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}${action}"` },
    body: env
  });
  if (!r.ok) throw new Error(`SOAP HTTP ${r.status}`);
  return r.text();
}

// Login — extract sessionId from XML
const loginXml = await soapCall('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>pass</ecg:Password></ecg:Login>');
const sessionId = '...extracted from loginXml...';

// ParcelInBox → ParcelDownload → ParcelDownloadConfirm for each parcel
// (build body strings and call soapCall for each)

// Logout
await soapCall('Logout',
  `<ecg:Logout><ecg:SessionID>${sessionId}</ecg:SessionID></ecg:Logout>`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — full SOAP session lifecycle: Login → ParcelInBox → Download → Confirm → Logout
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

def soap_call(action, body):
    env = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:ecg="' + ns + '">'
        '<soap:Body>' + body + '</soap:Body></soap:Envelope>'
    )
    resp = requests.post(endpoint, data=env.encode(), headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f'"{ns}{action}"'
    })
    resp.raise_for_status()
    return resp.text

# Login — extract session_id from XML
login_xml = soap_call("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>pass</ecg:Password></ecg:Login>")
session_id = "...extracted from login_xml..."

# ParcelInBox → ParcelDownload → ParcelDownloadConfirm for each parcel
# (build body strings and call soap_call for each)

# Logout
soap_call("Logout",
    f"<ecg:Logout><ecg:SessionID>{session_id}</ecg:SessionID></ecg:Logout>")
```

</TabItem>
</Tabs>

## Configuration

```json
{
  "ECGridOS": {
    "Login": "",
    "Password": "",
    "MailboxId": 0
  }
}
```

Store credentials with user-secrets:

```bash
cd samples/soap/ECGrid-SOAP-dotnet10-Console-HttpClient
dotnet user-secrets set "ECGridOS:Login" "your-login"
dotnet user-secrets set "ECGridOS:Password" "your-password"
```

## How to Run

```bash
cd samples/soap/ECGrid-SOAP-dotnet10-Console-HttpClient
dotnet user-secrets set "ECGridOS:Login" "your-login"
dotnet user-secrets set "ECGridOS:Password" "your-password"
dotnet run
```

## See Also

- [SOAP API Overview](../soap-api/overview.md)
- [SOAP Auth — Login](../soap-api/auth/login.md)
- [SOAP Parcels — ParcelInBox](../soap-api/parcels/parcel-inbox.md)
- [SOAP Parcels — ParcelDownload](../soap-api/parcels/parcel-download.md)
- [Connecting via SOAP](../guides/connecting-via-soap.md)
- [SOAP SvcUtil Sample](./soap-svcutil.md)
