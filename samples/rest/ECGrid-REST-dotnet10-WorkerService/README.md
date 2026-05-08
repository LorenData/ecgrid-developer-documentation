<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Worker Service sample README for ECGrid REST API polling - Greg Kolinski -->

# ECGrid REST API — .NET 10 Worker Service Sample

This sample demonstrates a production-style background service that polls the ECGrid inbox on a configurable interval, downloads ready parcels to disk, and confirms each download.

## What It Demonstrates

| Area | Detail |
|------|--------|
| `BackgroundService` | Long-running process via `IHostedService` |
| `PeriodicTimer` | Idiomatic .NET 6+ timer — no `Thread.Sleep` or `Task.Delay` loops |
| `IHttpClientFactory` | Named `"ecgrid"` client; never `new HttpClient()` |
| `System.Text.Json` | Record types with `JsonPropertyName` attributes |
| `IConfiguration` | `PollIntervalSeconds` read from `appsettings.json` |
| Per-parcel error isolation | One bad parcel does not stop the polling loop |

### Poll Cycle

```
Every PollIntervalSeconds seconds:
  POST /v2/parcels/inbox-list  → get InBoxReady parcels
  For each parcel:
    POST /v2/parcels/download  → decode base-64 content, write to output/
    POST /v2/parcels/confirm   → mark parcel as InBoxTransferred
```

## Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0)
- An active ECGrid API key

## Configuration

### appsettings.json

```json
{
  "ECGrid": {
    "ApiKey": "YOUR_API_KEY_HERE",
    "BaseUrl": "https://rest.ecgrid.io",
    "PollIntervalSeconds": 30
  }
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `ApiKey` | _(required)_ | ECGrid API key for `X-API-Key` header |
| `BaseUrl` | `https://rest.ecgrid.io` | ECGrid REST API base URL |
| `PollIntervalSeconds` | `30` | How often to check the inbox (seconds) |

### dotnet user-secrets (recommended for development)

```bash
dotnet user-secrets init
dotnet user-secrets set "ECGrid:ApiKey" "your-actual-key"
```

### Environment variables

```bash
# Windows
set ECGrid__ApiKey=your-actual-key
set ECGrid__PollIntervalSeconds=60

# macOS / Linux
export ECGrid__ApiKey=your-actual-key
export ECGrid__PollIntervalSeconds=60
```

## How to Run

```bash
cd samples/rest/ECGrid-REST-dotnet10-WorkerService
dotnet run
```

Downloaded parcels are saved to `output/` next to the binary. The service runs until stopped with `Ctrl+C`.

## Sample Log Output

```
info: ECGrid_REST_dotnet10_WorkerService.EcGridPollingWorker[0]
      ECGrid Polling Worker started. Poll interval: 30s.
info: ECGrid_REST_dotnet10_WorkerService.EcGridPollingWorker[0]
      Polling ECGrid inbox at 2026-05-07T14:00:00.000Z.
info: ECGrid_REST_dotnet10_WorkerService.EcGridPollingWorker[0]
      Found 2 parcel(s) ready for download.
info: ECGrid_REST_dotnet10_WorkerService.EcGridPollingWorker[0]
      Saved parcel 100001 → output/invoice.edi (1,234 bytes).
info: ECGrid_REST_dotnet10_WorkerService.EcGridPollingWorker[0]
      Confirmed parcel 100001.
info: ECGrid_REST_dotnet10_WorkerService.EcGridPollingWorker[0]
      Saved parcel 100002 → output/po.edi (987 bytes).
info: ECGrid_REST_dotnet10_WorkerService.EcGridPollingWorker[0]
      Confirmed parcel 100002.
```

## Deploying as a Windows Service or systemd Unit

### Windows Service

```bash
dotnet publish -c Release -o ./publish
sc create ECGridPoller binPath="C:\path\to\publish\ECGrid-REST-dotnet10-WorkerService.exe"
sc start ECGridPoller
```

### systemd (Linux)

Create `/etc/systemd/system/ecgrid-poller.service`:

```ini
[Unit]
Description=ECGrid Parcel Polling Worker

[Service]
WorkingDirectory=/opt/ecgrid-poller
ExecStart=/opt/ecgrid-poller/ECGrid-REST-dotnet10-WorkerService
Restart=always
RestartSec=10
Environment=ECGrid__ApiKey=your-actual-key

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable ecgrid-poller
systemctl start ecgrid-poller
```

## Project Structure

```
ECGrid-REST-dotnet10-WorkerService/
├── ECGrid-REST-dotnet10-WorkerService.csproj
├── appsettings.json
├── Program.cs                  ← host setup, IHttpClientFactory registration
├── EcGridPollingWorker.cs      ← BackgroundService with PeriodicTimer
└── README.md
```

## Related Documentation

- [ECGrid REST API Overview](https://developers.ecgrid.com/docs/rest-api/overview)
- [Parcels — Inbox List](https://developers.ecgrid.com/docs/rest-api/parcels/inbox-list)
- [Parcels — Download](https://developers.ecgrid.com/docs/rest-api/parcels/download-parcel)
- [Parcels — Confirm Download](https://developers.ecgrid.com/docs/rest-api/parcels/confirm-download)
- [Common Operations — Poll Inbound Files](https://developers.ecgrid.com/docs/common-operations/poll-inbound-files)
