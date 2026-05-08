<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: MinimalAPI sample README - Greg Kolinski -->

# ECGrid REST — .NET 10 Minimal API Sample

This project demonstrates how to integrate with the ECGrid REST API (v2.6) from an
ASP.NET Core Minimal API application running on .NET 10. It acts as a thin proxy layer,
showing the `IHttpClientFactory` pattern, correct header management, and how to forward
multipart file uploads to ECGrid.

---

## What It Demonstrates

- Registering a named `HttpClient` with `IHttpClientFactory` (never `new HttpClient()`)
- Setting `X-API-Key` as a default header on the named client
- Proxying GET and POST requests to the ECGrid REST API
- Forwarding multipart file uploads from a caller to ECGrid
- Returning structured JSON error responses when ECGrid returns a non-2xx status
- Loading the API key from `IConfiguration` / environment variables — never hardcoded

---

## Prerequisites

| Requirement | Version |
|---|---|
| .NET SDK | 10.0 or later |
| ECGrid account | Active API key with at least MailboxUser access |

---

## Configuration

Open `appsettings.json` and fill in your values:

```json
{
  "ECGrid": {
    "ApiKey": "YOUR_API_KEY_HERE",
    "BaseUrl": "https://rest.ecgrid.io"
  }
}
```

Alternatively, set environment variables (useful for CI/CD and containers):

```bash
export ECGrid__ApiKey="your-api-key"
export ECGrid__BaseUrl="https://rest.ecgrid.io"
```

> Never commit real API keys to source control. Add `appsettings.json` overrides to `.gitignore`
> or use a secrets manager such as Azure Key Vault or AWS Secrets Manager in production.

---

## How to Run

```bash
cd samples/rest/ECGrid-REST-dotnet10-MinimalAPI
dotnet run
```

The application starts on `http://localhost:5000` by default.

---

## Endpoint Reference

| Method | Route | Proxied ECGrid Endpoint | Description |
|---|---|---|---|
| `GET` | `/inbox` | `POST /v2/parcels/inbox-list` | List inbound parcels for the authenticated mailbox |
| `GET` | `/parcel/{id}` | `GET /v2/parcels/{id}` | Retrieve metadata for a single parcel |
| `POST` | `/upload` | `POST /v2/parcels/upload` | Upload an EDI file; returns the new parcel ID |
| `POST` | `/confirm/{id}` | `POST /v2/parcels/confirm` | Confirm download of a parcel |

### Example Requests

**List inbox:**
```bash
curl http://localhost:5000/inbox
```

**Get parcel metadata:**
```bash
curl http://localhost:5000/parcel/123456789
```

**Upload a file:**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@./my-edi-file.edi"
```

**Confirm download:**
```bash
curl -X POST http://localhost:5000/confirm/123456789
```

---

## Project Structure

```
ECGrid-REST-dotnet10-MinimalAPI/
├── ECGrid-REST-dotnet10-MinimalAPI.csproj
├── appsettings.json
├── Program.cs          ← All route handlers (top-level statements)
└── README.md
```

---

## Related Documentation

- [ECGrid REST API Overview](../../../website/docs/rest-api/overview.md)
- [Parcels — Upload](../../../website/docs/rest-api/parcels/upload-parcel.md)
- [Parcels — Inbox List](../../../website/docs/rest-api/parcels/inbox-list.md)
- [Parcels — Confirm Download](../../../website/docs/rest-api/parcels/confirm-download.md)
- [Authentication — API Keys](../../../website/docs/getting-started/authentication-api-keys.md)
