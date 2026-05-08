<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Console sample README for ECGrid REST API - Greg Kolinski -->

# ECGrid REST API — .NET 10 Console Sample

This sample demonstrates a complete parcel workflow against the ECGrid REST API using a .NET 10 console application with top-level statements.

## What It Demonstrates

| Step | Action | Endpoint |
|------|--------|----------|
| 1 | Verify API connectivity | `GET /v2/auth/version` |
| 2 | Poll inbox for ready parcels | `POST /v2/parcels/inbox-list` |
| 3 | Download each ready parcel | `POST /v2/parcels/download` |
| 4 | Save parcel content to disk | — |
| 5 | Confirm download | `POST /v2/parcels/confirm` |
| 6 | Upload a file to ECGrid | `POST /v2/parcels/upload` |

Key patterns shown:
- `IHttpClientFactory` via `ServiceCollection` (no `new HttpClient()`)
- `System.Text.Json` with record types
- `IConfiguration` loaded from `appsettings.json` and environment variables
- Per-parcel error handling so one bad file never stops the loop

## Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0)
- An active ECGrid API key ([get one at developers.ecgrid.com](https://developers.ecgrid.com))

## Configuration

### Option A — appsettings.json

Open `appsettings.json` and replace the placeholder:

```json
{
  "ECGrid": {
    "ApiKey": "YOUR_API_KEY_HERE",
    "BaseUrl": "https://rest.ecgrid.io"
  }
}
```

### Option B — dotnet user-secrets (recommended for development)

```bash
dotnet user-secrets init
dotnet user-secrets set "ECGrid:ApiKey" "your-actual-key"
```

### Option C — environment variable

```bash
# Windows
set ECGrid__ApiKey=your-actual-key

# macOS / Linux
export ECGrid__ApiKey=your-actual-key
```

## How to Run

```bash
cd samples/rest/ECGrid-REST-dotnet10-Console
dotnet run
```

Downloaded parcels are saved to `downloads/` next to the binary.
The upload step creates a small dummy EDI file in `uploads/` when no file is present.

## Output Example

```
=== ECGrid REST API — Console Sample ===

Step 1: Checking API version...
  API version: 2.6.0

Step 2: Checking inbox for ready parcels...
  Found 2 parcel(s) ready for download.

  Processing parcel 100001 — invoice.edi...
    Saved to: downloads/invoice.edi (1,234 bytes)
    Confirmed: True
  Processing parcel 100002 — po.edi...
    Saved to: downloads/po.edi (987 bytes)
    Confirmed: True

Step 4: Uploading a test file...
  Upload successful. Parcel ID: 100050

=== Sample complete ===
```

## Project Structure

```
ECGrid-REST-dotnet10-Console/
├── ECGrid-REST-dotnet10-Console.csproj
├── appsettings.json
├── Program.cs          ← all logic, record types at bottom
└── README.md
```

## Related Documentation

- [ECGrid REST API Overview](https://developers.ecgrid.com/docs/rest-api/overview)
- [Authentication](https://developers.ecgrid.com/docs/getting-started/authentication-api-keys)
- [Parcels — Download](https://developers.ecgrid.com/docs/rest-api/parcels/download-parcel)
- [Parcels — Upload](https://developers.ecgrid.com/docs/rest-api/parcels/upload-parcel)
