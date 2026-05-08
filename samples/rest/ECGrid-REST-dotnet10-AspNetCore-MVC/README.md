<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: ASP.NET Core MVC sample README for ECGrid REST API - Greg Kolinski -->

# ECGrid REST API — .NET 10 ASP.NET Core MVC Sample

This sample demonstrates ECGrid REST API parcel operations inside an ASP.NET Core MVC web application using a service layer and `IHttpClientFactory`.

## What It Demonstrates

| Area | Detail |
|------|--------|
| Service layer | `IEcGridService` / `EcGridService` decouples HTTP calls from controllers |
| `IHttpClientFactory` | Named client `"ecgrid"` configured once in `Program.cs` |
| `System.Text.Json` | Record types with `JsonPropertyName` attributes |
| MVC actions | Inbox list, file download (returns `File` result), file upload via `IFormFile` |
| Error handling | Per-action try/catch returning appropriate HTTP status codes |

### Controller Actions

| Route | Method | Description |
|-------|--------|-------------|
| `GET /ECGrid/Inbox` | `GET` | Lists `InBoxReady` parcels |
| `POST /ECGrid/Download/{parcelId}` | `POST` | Downloads + confirms a parcel, returns file bytes |
| `GET /ECGrid/Upload` | `GET` | Shows upload form |
| `POST /ECGrid/Upload` | `POST` | Accepts `IFormFile`, uploads to ECGrid |

## Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0)
- An active ECGrid API key

## Configuration

### Option A — appsettings.json

```json
{
  "ECGrid": {
    "ApiKey": "YOUR_API_KEY_HERE",
    "BaseUrl": "https://rest.ecgrid.io"
  }
}
```

### Option B — dotnet user-secrets (recommended)

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
cd samples/rest/ECGrid-REST-dotnet10-AspNetCore-MVC
dotnet run
```

Then open `https://localhost:5001/ECGrid/Inbox` in a browser.

## Project Structure

```
ECGrid-REST-dotnet10-AspNetCore-MVC/
├── ECGrid-REST-dotnet10-AspNetCore-MVC.csproj
├── appsettings.json
├── Program.cs
├── Controllers/
│   └── EcGridController.cs   ← Inbox, Download, Upload actions
├── Models/
│   └── EcGridModels.cs       ← Record types for requests and responses
├── Services/
│   ├── IEcGridService.cs     ← Service interface
│   └── EcGridService.cs      ← IHttpClientFactory-based implementation
└── README.md
```

## Adding Razor Views

This project registers the MVC pipeline but ships without Razor `.cshtml` files to keep the sample focused on the API integration layer. To add views:

1. Create `Views/ECGrid/Inbox.cshtml` — iterate `IEnumerable<ParcelSummary>` passed as model
2. Create `Views/ECGrid/Upload.cshtml` — HTML form with `enctype="multipart/form-data"`
3. Create `Views/Shared/_Layout.cshtml` and `Views/Shared/Error.cshtml`

## Related Documentation

- [ECGrid REST API Overview](https://developers.ecgrid.com/docs/rest-api/overview)
- [Parcels — Inbox List](https://developers.ecgrid.com/docs/rest-api/parcels/inbox-list)
- [Parcels — Download](https://developers.ecgrid.com/docs/rest-api/parcels/download-parcel)
- [Parcels — Upload](https://developers.ecgrid.com/docs/rest-api/parcels/upload-parcel)
