<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: SOAP HttpClient sample README - Greg Kolinski -->

# ECGrid SOAP — .NET 10 Console (Manual HttpClient)

This project demonstrates how to call the ECGridOS SOAP API (v4.1) from a .NET 10
console application using raw `HttpClient` and `XDocument` — **no generated proxy,
no WCF configuration files**. It is the lightest-weight SOAP integration approach
and is ideal when you want minimal dependencies.

---

## What It Demonstrates

- Building SOAP 1.1 envelopes by hand with correct namespace declarations
- Setting the `SOAPAction` HTTP header required by ECGridOS
- Parsing SOAP XML responses with `XDocument` and LINQ to XML
- Using `IHttpClientFactory` for proper connection pool management
- Login → inbox poll → download → confirm → logout workflow
- Saving downloaded parcels to disk only before confirming (safe sequencing)
- Logging out in a `finally` block to prevent orphaned server sessions

---

## SOAP Envelope Pattern

Every ECGridOS call follows this structure. The namespace `http://www.ecgridos.net/`
must appear on the operation element:

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <Login xmlns="http://www.ecgridos.net/">
      <UserName>user@example.com</UserName>
      <Password>P@ssw0rd!</Password>
    </Login>
  </soap:Body>
</soap:Envelope>
```

The HTTP request must include the `SOAPAction` header:

```
SOAPAction: "http://www.ecgridos.net/Login"
Content-Type: text/xml; charset=utf-8
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| .NET SDK | 10.0 or later |
| ECGrid account | Valid username and password |

---

## Configuration

Open `appsettings.json`:

```json
{
  "ECGrid": {
    "UserName": "YOUR_USERNAME",
    "Password": "YOUR_PASSWORD",
    "BaseUrl": "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
  }
}
```

Or use environment variables:

```bash
export ECGrid__UserName="your-username"
export ECGrid__Password="your-password"
```

> Never commit real credentials to source control.

---

## How to Run

```bash
cd samples/soap/ECGrid-SOAP-dotnet10-Console-HttpClient
dotnet run
```

Downloaded parcels are written to a `downloads/` subdirectory next to the executable.

---

## Project Structure

```
ECGrid-SOAP-dotnet10-Console-HttpClient/
├── ECGrid-SOAP-dotnet10-Console-HttpClient.csproj
├── appsettings.json
├── SoapClient.cs       ← EcGridSoapClient with typed async methods
├── Program.cs          ← Top-level entry point; polling workflow
└── README.md
```

---

## Key Files

### `SoapClient.cs`

`EcGridSoapClient` exposes typed async methods:

| Method | Description |
|---|---|
| `LoginAsync(userName, password)` | Authenticates; returns session ID |
| `ParcelInBoxAsync(sessionId, networkId, mailboxId)` | Lists inbound parcels |
| `ParcelDownloadAsync(sessionId, parcelId)` | Downloads raw EDI bytes |
| `ParcelDownloadConfirmAsync(sessionId, parcelId)` | Confirms receipt |
| `LogoutAsync(sessionId)` | Terminates the session |

The private `PostSoapAsync(action, bodyXml)` helper handles envelope construction,
the `SOAPAction` header, and XML parsing.

---

## Related Documentation

- [ECGrid SOAP API Overview](../../../website/docs/soap-api/overview.md)
- [Connecting via SOAP](../../../website/docs/guides/connecting-via-soap.md)
- [Parcels — ParcelInBox](../../../website/docs/soap-api/parcels/parcel-inbox.md)
- [Parcels — ParcelDownload](../../../website/docs/soap-api/parcels/parcel-download.md)
- [REST equivalent sample](../../../samples/rest/ECGrid-REST-dotnet10-MinimalAPI/)
