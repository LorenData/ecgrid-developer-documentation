---
title: Connecting via SOAP
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created connecting via SOAP guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs to SOAP connection options - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Connecting via SOAP

This guide covers the three supported methods for connecting a .NET 10 application to the ECGridOS SOAP API.

## Service Endpoints

| Resource | URL |
|---|---|
| SOAP service | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx` |
| WSDL | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL` |
| Service namespace | `http://www.ecgridos.net/` |

---

## Option 1 — Manual HttpClient

Use a raw `HttpClient` to POST SOAP envelopes when you need minimal dependencies and full control over the wire format. This is the approach used in the `ECGrid-SOAP-dotnet10-Console-HttpClient` sample.

### SOAP envelope structure

Every ECGridOS request uses the same SOAP 1.1 envelope structure:

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body>
    <ecg:MethodName>
      <ecg:SessionID>your-session-id</ecg:SessionID>
      <ecg:Param1>value1</ecg:Param1>
    </ecg:MethodName>
  </soap:Body>
</soap:Envelope>
```

### SOAPAction header

Every request must include a `SOAPAction` header matching the method being called:

```http
SOAPAction: "http://www.ecgridos.net/MethodName"
```

### Complete C# example

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — manual HttpClient SOAP, minimal dependencies
// Uses IHttpClientFactory; never instantiate HttpClient directly in production

using System.Net.Http.Headers;
using System.Text;
using System.Xml.Linq;

/// <summary>Sends a raw SOAP request to the ECGridOS endpoint and returns the response XML.</summary>
static async Task<XDocument> SendSoapAsync(
    IHttpClientFactory httpClientFactory,
    string methodName,
    string soapBody)
{
    const string Endpoint  = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
    const string Namespace = "http://www.ecgridos.net/";

    var envelope = $"""
        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope
            xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:ecg="{Namespace}">
          <soap:Body>
            {soapBody}
          </soap:Body>
        </soap:Envelope>
        """;

    using var content = new StringContent(envelope, Encoding.UTF8, "text/xml");
    content.Headers.Add("SOAPAction", $"\"{Namespace}{methodName}\"");

    var http = httpClientFactory.CreateClient("ECGridSOAP");
    var response = await http.PostAsync(Endpoint, content);
    response.EnsureSuccessStatusCode();

    var xml = await response.Content.ReadAsStringAsync();
    return XDocument.Parse(xml);
}

/// <summary>Logs in and returns a SessionID string.</summary>
static async Task<string> LoginAsync(IHttpClientFactory factory, string email, string password)
{
    var body = $"""
        <ecg:Login>
          <ecg:Email>{email}</ecg:Email>
          <ecg:Password>{password}</ecg:Password>
        </ecg:Login>
        """;

    var doc = await SendSoapAsync(factory, "Login", body);

    XNamespace ns = "http://www.ecgridos.net/";
    var sessionID = doc.Descendants(ns + "LoginResult").FirstOrDefault()?.Value
        ?? throw new InvalidOperationException("Login failed — no SessionID returned.");

    return sessionID;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — manual SOAP envelope construction and dispatch
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Build the SOAP envelope for any method
String methodName = "Login";
String soapBody = "<ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login>";

String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body>" + soapBody + "</soap:Body></soap:Envelope>";

var request = HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + methodName + "\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // parse XML to extract result
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — manual SOAP envelope construction and dispatch
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

async function sendSoap(methodName, soapBody) {
  const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>${soapBody}</soap:Body>
</soap:Envelope>`;

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/xml; charset=utf-8',
      SOAPAction: `"${ns}${methodName}"`
    },
    body: envelope
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.text(); // parse XML to extract result
}

// Example: Login
const xml = await sendSoap('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>YourPassword1!</ecg:Password></ecg:Login>');
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — manual SOAP envelope construction and dispatch
import requests

ENDPOINT = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
NS = "http://www.ecgridos.net/"

def send_soap(method_name, soap_body):
    envelope = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:ecg="' + NS + '">'
        '<soap:Body>' + soap_body + '</soap:Body></soap:Envelope>'
    )
    resp = requests.post(ENDPOINT, data=envelope.encode(), headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f'"{NS}{method_name}"'
    })
    resp.raise_for_status()
    return resp.text  # parse XML to extract result

# Example: Login
xml = send_soap("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>YourPassword1!</ecg:Password></ecg:Login>")
```

</TabItem>
</Tabs>

---

## Option 2 — dotnet-svcutil (Recommended)

`dotnet-svcutil` generates a strongly-typed C# proxy from the WSDL.

### Install the tool

```bash
dotnet tool install --global dotnet-svcutil
```

### Generate the proxy

Run this from your project directory:

```bash
dotnet-svcutil https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL --outputDir ./ServiceReference --namespace ECGrid.Soap.Client
```

This creates:
- `ServiceReference/Reference.cs` — the generated proxy class
- `ServiceReference/dotnet-svcutil.params.json` — the generation parameters (commit this file)

### Add the required NuGet package

```bash
dotnet add package System.ServiceModel.Http
```

### Use the generated proxy

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGrid.Soap.Client;
using Microsoft.Extensions.Configuration;

var config = new ConfigurationBuilder()
    .AddEnvironmentVariables()
    .AddJsonFile("appsettings.json", optional: true)
    .Build();

var email    = config["ECGrid:Email"]    ?? throw new InvalidOperationException("ECGrid:Email is not configured.");
var password = config["ECGrid:Password"] ?? throw new InvalidOperationException("ECGrid:Password is not configured.");

// Create the client — endpoint is defined in the generated binding
using var client = new ECGridOSPortTypeClient(
    ECGridOSPortTypeClient.EndpointConfiguration.ECGridOSPort);

var sessionID = string.Empty;
try
{
    sessionID = await client.LoginAsync(email, password);
    Console.WriteLine($"Logged in. SessionID: {sessionID[..8]}...");

    // All subsequent calls pass sessionID as the first argument
    var mailboxInfo = await client.MailboxInfoAsync(sessionID, mailboxID: 0);
    Console.WriteLine($"Default mailbox: {mailboxInfo.MailboxName}");
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
// Java 11+ — no svcutil equivalent; use raw HTTP SOAP
// For a typed approach in Java, consider JAX-WS with wsimport:
//   wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL
//
// Raw HTTP approach (same as Option 1):
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login envelope
String loginEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";

var loginResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "Login\"")
    .POST(BodyPublishers.ofString(loginEnv)).build(), BodyHandlers.ofString());

// Extract sessionId and use it in subsequent calls
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — no svcutil equivalent; use raw HTTP SOAP
// For a typed approach in Node.js, consider the 'soap' npm package:
//   npm install soap
//
// Raw HTTP approach (same as Option 1):
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

const loginEnv = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>
    <ecg:Login>
      <ecg:Email>user@example.com</ecg:Email>
      <ecg:Password>YourPassword1!</ecg:Password>
    </ecg:Login>
  </soap:Body>
</soap:Envelope>`;

const loginResp = await fetch(endpoint, {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}Login"` },
  body: loginEnv
});
const xml = await loginResp.text();
// Extract sessionId from xml and use in subsequent calls
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — no svcutil equivalent; use raw HTTP SOAP
# For a typed approach in Python, consider the 'zeep' library:
#   pip install zeep
#   from zeep import Client
#   client = Client("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL")
#
# Raw HTTP approach (same as Option 1):
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

login_env = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:ecg="' + ns + '">'
    '<soap:Body><ecg:Login>'
    '<ecg:Email>user@example.com</ecg:Email>'
    '<ecg:Password>YourPassword1!</ecg:Password>'
    '</ecg:Login></soap:Body></soap:Envelope>'
)
login_resp = requests.post(endpoint, data=login_env.encode(), headers={
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": f'"{ns}Login"'
})
# Extract session_id from login_resp.text and use in subsequent calls
```

</TabItem>
</Tabs>

---

## Option 3 — CoreWCF

CoreWCF is the right choice when you are **migrating existing WCF client code** to .NET 10. It provides a familiar `ChannelFactory<T>` programming model.

### Add the NuGet package

```bash
dotnet add package CoreWCF.Http
```

### Configure the channel

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — CoreWCF ChannelFactory, mirrors classic WCF client usage
using CoreWCF;
using CoreWCF.Channels;
using ECGrid.Soap.Contracts; // your manually-defined or generated service contract

var binding  = new BasicHttpsBinding();
var endpoint = new EndpointAddress("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx");

using var factory = new ChannelFactory<IECGridOS>(binding, endpoint);
var channel = factory.CreateChannel();

var sessionID = await channel.LoginAsync(email, password);
try
{
    var parcelList = await channel.ParcelInBoxAsync(sessionID, mailboxID, beginDate, endDate);
}
finally
{
    await channel.LogoutAsync(sessionID);
    factory.Close();
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — no CoreWCF equivalent; use raw HTTP SOAP
// For a typed approach in Java, consider JAX-WS with wsimport:
//   wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL
//
// Raw HTTP approach (same as Option 1):
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login envelope
String loginEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";

var loginResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "Login\"")
    .POST(BodyPublishers.ofString(loginEnv)).build(), BodyHandlers.ofString());

// Extract sessionId and use it in subsequent calls
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — no CoreWCF equivalent; use raw HTTP SOAP
// For a typed approach in Node.js, consider the 'soap' npm package:
//   npm install soap
//
// Raw HTTP approach (same as Option 1):
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

const loginEnv = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>
    <ecg:Login>
      <ecg:Email>user@example.com</ecg:Email>
      <ecg:Password>YourPassword1!</ecg:Password>
    </ecg:Login>
  </soap:Body>
</soap:Envelope>`;

const loginResp = await fetch(endpoint, {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}Login"` },
  body: loginEnv
});
const xml = await loginResp.text();
// Extract sessionId from xml and use in subsequent calls
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — no CoreWCF equivalent; use raw HTTP SOAP
# For a typed approach in Python, consider the 'zeep' library:
#   pip install zeep
#   from zeep import Client
#   client = Client("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL")
#
# Raw HTTP approach (same as Option 1):
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

login_env = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:ecg="' + ns + '">'
    '<soap:Body><ecg:Login>'
    '<ecg:Email>user@example.com</ecg:Email>'
    '<ecg:Password>YourPassword1!</ecg:Password>'
    '</ecg:Login></soap:Body></soap:Envelope>'
)
login_resp = requests.post(endpoint, data=login_env.encode(), headers={
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": f'"{ns}Login"'
})
# Extract session_id from login_resp.text and use in subsequent calls
```

</TabItem>
</Tabs>

:::note
CoreWCF is best suited for migrating existing WCF code. For greenfield projects, use `dotnet-svcutil` (Option 1) or manual `HttpClient` (Option 3).
:::

---

## Choosing Between the Three Options

| Scenario | Recommended option |
|---|---|
| New .NET 10 project, SOAP required | dotnet-svcutil |
| Migrating existing WCF client code | CoreWCF |
| Minimal dependencies, full wire control | Manual HttpClient |

## Related

- [REST vs SOAP — Choosing the Right API](./rest-vs-soap.md)
- [Authentication & Session Management](./authentication.md)
- [SOAP API Overview](../soap-api/overview.md)
- [Code Samples — SOAP HttpClient](../code-samples/soap-httpclient.md)
- [Code Samples — SOAP SvcUtil](../code-samples/soap-svcutil.md)
