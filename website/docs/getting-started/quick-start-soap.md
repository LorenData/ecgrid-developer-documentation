---
title: Quick Start — SOAP API
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create SOAP API quick start page - Greg Kolinski
    2026-05-07: Rewrote to be language-agnostic with tabbed examples (C#, Java, Node.js, Python) - Greg Kolinski
    2026-05-07: Step 2 corrected to ParcelInBoxEx with actual parameters from live service - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Quick Start — SOAP API

ECGridOS SOAP is standard **SOAP 1.1 over HTTPS**. Under the hood it is a plain HTTP POST with an XML envelope body — any HTTP client in any language can call it.

## Service Endpoint & WSDL

| | URL |
|---|---|
| **Service endpoint** | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx` |
| **WSDL** | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL` |
| **XML namespace** | `https://os.ecgrid.io/` |

## How SOAP Works

Every call is an HTTP POST to the service endpoint with a `SOAPAction` header identifying the method. You can build this with any HTTP library, or use a SOAP library that consumes the WSDL directly.

```http
POST https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx
Content-Type: text/xml; charset=utf-8
SOAPAction: "https://os.ecgrid.io/MethodName"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/>
  <soap:Body>
    <MethodName>
      <SessionID>YOUR_SESSION_ID</SessionID>
      <Param1>value</Param1>
    </MethodName>
  </soap:Body>
</soap:Envelope>
```

Every method except `Login` takes `SessionID` as its first parameter.

---

## Step 1 — Login

Obtain a `SessionID` by calling `Login` or use your User account API Key the two are interchangeable. Pass it as the first parameter to every subsequent call.

`SOAPAction: "https://os.ecgrid.io/Login"`

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
using System.Net.Http;
using System.Text;
using System.Xml.Linq;

var username = Environment.GetEnvironmentVariable("ECGRID_USER")!;
var password = Environment.GetEnvironmentVariable("ECGRID_PASS")!;

using var http = new HttpClient();

var envelope = $"""
    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/>
      <soap:Body>
        <Login>
          <UserID>{username}</UserID>
          <Password>{password}</Password>
        </Login>
      </soap:Body>
    </soap:Envelope>
    """;

using var content = new StringContent(envelope, Encoding.UTF8, "text/xml");
content.Headers.Add("SOAPAction", "\"https://os.ecgrid.io/Login\"");

var response = await http.PostAsync(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx", content);
response.EnsureSuccessStatusCode();

var xml       = XDocument.Parse(await response.Content.ReadAsStringAsync());
XNamespace ns = "https://os.ecgrid.io/";
var sessionId = xml.Descendants(ns + "LoginResult").First().Value;
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;
import javax.xml.parsers.*;
import org.w3c.dom.*;
import java.io.*;

String username = System.getenv("ECGRID_USER");
String password = System.getenv("ECGRID_PASS");

String envelope = """
    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/>
      <soap:Body>
        <Login>
          <UserID>%s</UserID>
          <Password>%s</Password>
        </Login>
      </soap:Body>
    </soap:Envelope>
    """.formatted(username, password);

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"https://os.ecgrid.io/Login\"")
    .POST(HttpRequest.BodyPublishers.ofString(envelope))
    .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setNamespaceAware(true);
Document doc = factory.newDocumentBuilder()
    .parse(new ByteArrayInputStream(response.body().getBytes()));

String sessionId = doc
    .getElementsByTagNameNS("https://os.ecgrid.io/", "LoginResult")
    .item(0).getTextContent();
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — built-in fetch; use xml2js or fast-xml-parser for production XML parsing
const username = process.env.ECGRID_USER;
const password = process.env.ECGRID_PASS;

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/>
  <soap:Body>
    <Login>
      <UserID>${username}</UserID>
      <Password>${password}</Password>
    </Login>
  </soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"https://os.ecgrid.io/Login"'
  },
  body: envelope
});

const xml       = await response.text();
const sessionId = xml.match(/<LoginResult>(.+?)<\/LoginResult>/)?.[1];
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests, xml.etree.ElementTree as ET

username = os.environ['ECGRID_USER']
password = os.environ['ECGRID_PASS']
NS       = 'https://os.ecgrid.io/'

envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/>
  <soap:Body>
    <Login>
      <UserID>{username}</UserID>
      <Password>{password}</Password>
    </Login>
  </soap:Body>
</soap:Envelope>"""

response = requests.post(
    'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx',
    data=envelope.encode('utf-8'),
    headers={
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': f'"{NS}Login"'
    }
)
response.raise_for_status()

root       = ET.fromstring(response.text)
session_id = root.find(f'.//{{{NS}}}LoginResult').text
```

</TabItem>
</Tabs>

The `SessionID` is passed as the first XML element in every subsequent call. Sessions expire after inactivity — always call `Logout` when finished.

---

## Step 2 — Check Your Inbox

`SOAPAction: "https://os.ecgrid.io/ParcelInBox"`

```xml
<ParcelInBoxEx>
  <SessionID>YOUR_SESSION_ID</SessionID>
</ParcelInBoxEx>
```

The response XML contains `ParcelIDInfo` elements with `ParcelID`, `FileName`, `Bytes`, and `ECGridIDFrom`/`ECGridIDTo` — iterate them to build your download list.

The HTTP call pattern (wrap this envelope in a full SOAP `Envelope`/`Body`, POST to the service endpoint with the appropriate `SOAPAction` header) is identical to Login above — just swap the method name and parameters.

---

## Step 3 — Download a Parcel

`SOAPAction: "https://os.ecgrid.io/ParcelDownload"`

```xml
<ParcelDownload>
  <SessionID>YOUR_SESSION_ID</SessionID>
  <ParcelID>123456</ParcelID>
</ParcelDownload>
```

The response contains the EDI file as a base64-encoded string inside `ParcelDownloadResult`. Decode it and write to disk.

---

## Step 4 — Confirm the Download

`SOAPAction: "https://os.ecgrid.io/ParcelDownloadConfirm"`

```xml
<ParcelDownloadConfirm>
  <SessionID>YOUR_SESSION_ID</SessionID>
  <ParcelID>123456</ParcelID>
</ParcelDownloadConfirm>
```

Un-confirmed parcels remain `InBoxReady` and re-appear on the next inbox poll — call this after every successful save.

---

## Step 5 — Logout

`SOAPAction: "https://os.ecgrid.io/Logout"`

```xml
<Logout>
  <SessionID>YOUR_SESSION_ID</SessionID>
</Logout>
```

Always call `Logout`, even on error if you did not use the User API Key to Authenticate. Use a try/finally block to guarantee the session is released.

---

## SOAP Libraries

To avoid constructing XML envelopes by hand, use a SOAP library that consumes the WSDL at `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL`:

| Language | Libraries |
|---|---|
| C# / .NET | `dotnet-svcutil` (typed proxy), `CoreWCF` (WCF migration) |
| Java | JAX-WS (`wsimport`), Apache CXF |
| Node.js | `soap` (npm), `strong-soap` |
| Python | `zeep`, `suds-community` |

---

## Next Steps

- [SOAP API Reference](../soap-api/overview.md) — full method documentation
- [SOAP Connecting Guide](./connecting-via-soap.md) — binding options, error handling, proxy configuration
- [Quick Start — REST API](./quick-start-rest.md) — the modern REST alternative
- [Migrating SOAP to REST](./migrating-soap-to-rest.md) — step-by-step migration guide
