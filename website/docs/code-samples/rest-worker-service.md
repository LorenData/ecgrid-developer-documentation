---
title: REST Worker Service Sample
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created REST Worker Service sample documentation page - Greg Kolinski */}

# REST Worker Service Sample

The `ECGrid-REST-dotnet10-WorkerService` project demonstrates running ECGrid inbox polling as a .NET background service. The worker wakes on a configurable interval, checks for new parcels, downloads and processes each one, and confirms receipt before sleeping again.

## Project Location

```
samples/rest/ECGrid-REST-dotnet10-WorkerService/
```

## What It Demonstrates

- Extending `BackgroundService` for a long-running hosted service
- Configurable poll interval via `appsettings.json` (`PollIntervalSeconds`, default 30)
- `IHttpClientFactory` injected into the worker — no direct `HttpClient` instantiation
- Graceful cancellation via `CancellationToken` from the host
- Download-process-confirm loop so parcels are never left in a partially downloaded state

## Key Files

| File | Purpose |
|---|---|
| `Program.cs` | Host configuration, service registration |
| `Worker.cs` | `BackgroundService` subclass with `ExecuteAsync` polling loop |
| `EcGridClient.cs` | Thin wrapper around ECGrid REST endpoints |
| `appsettings.json` | Configuration including `PollIntervalSeconds` |

## Configuration

```json
{
  "ECGrid": {
    "BaseUrl": "https://rest.ecgrid.io",
    "ApiKey": "",
    "MailboxId": 0,
    "PollIntervalSeconds": 30
  }
}
```

Set the API key locally with user-secrets:

```bash
cd samples/rest/ECGrid-REST-dotnet10-WorkerService
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
```

## Key Patterns

### Service Registration (`Program.cs`)

```csharp
// Program.cs — register the background worker and its HttpClient dependency
var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddHttpClient("ecgrid", (sp, client) =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    client.BaseAddress = new Uri(config["ECGrid:BaseUrl"]!);
    // API key from configuration — never hardcoded in source
    client.DefaultRequestHeaders.Add("X-API-Key", config["ECGrid:ApiKey"]!);
});

// Worker runs for the lifetime of the host process
builder.Services.AddHostedService<Worker>();

var host = builder.Build();
await host.RunAsync();
```

### Polling Loop (`Worker.cs`)

```csharp
/// <summary>
/// Background worker that polls the ECGrid inbox on a fixed interval,
/// downloads new parcels, and confirms each download.
/// </summary>
public class Worker : BackgroundService
{
    private readonly IHttpClientFactory _httpFactory;
    private readonly IConfiguration _config;
    private readonly ILogger<Worker> _logger;

    public Worker(IHttpClientFactory httpFactory, IConfiguration config, ILogger<Worker> logger)
    {
        _httpFactory = httpFactory;
        _config = config;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var mailboxId = _config.GetValue<int>("ECGrid:MailboxId");
        // Read poll interval from config; fall back to 30 seconds if not set
        var interval = TimeSpan.FromSeconds(
            _config.GetValue("ECGrid:PollIntervalSeconds", 30));

        _logger.LogInformation("ECGrid worker started. Polling every {Interval}s.", interval.TotalSeconds);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessInboxAsync(mailboxId, stoppingToken);
            }
            catch (Exception ex) when (ex is not OperationCanceledException)
            {
                // Log and continue — a transient error should not stop the worker
                _logger.LogError(ex, "Error processing ECGrid inbox for mailbox {MailboxId}.", mailboxId);
            }

            // Wait for the next poll cycle, respecting cancellation
            await Task.Delay(interval, stoppingToken);
        }

        _logger.LogInformation("ECGrid worker stopping.");
    }

    /// <summary>
    /// Checks the inbox and processes every waiting parcel in the current cycle.
    /// </summary>
    private async Task ProcessInboxAsync(int mailboxId, CancellationToken ct)
    {
        var http = _httpFactory.CreateClient("ecgrid");

        var inboxResponse = await http.PostAsJsonAsync(
            "v2/parcels/pending-inbox-list",
            new { mailboxId, pageNo = 1, recordsPerPage = 25 }, ct);
        var inbox = await inboxResponse.Content
            .ReadFromJsonAsync<ApiResponse<List<ParcelSummary>>>(ct);

        var parcels = inbox?.Data ?? [];
        _logger.LogInformation("{Count} parcel(s) in inbox.", parcels.Count);

        foreach (var parcel in parcels)
        {
            // Download the EDI content
            var download = await http.GetAsync($"/v2/parcels/{parcel.ParcelId}/download", ct);
            download.EnsureSuccessStatusCode();
            var ediBytes = await download.Content.ReadAsByteArrayAsync(ct);

            // Hand off to processing logic — replace with your own pipeline
            await ProcessEdiFileAsync(parcel.ParcelId, ediBytes);

            // Confirm receipt — must be called so ECGrid marks the parcel delivered
            await http.PostAsync($"/v2/parcels/{parcel.ParcelId}/confirm", null, ct);

            _logger.LogInformation("Parcel {ParcelId} downloaded and confirmed.", parcel.ParcelId);
        }
    }

    /// <summary>
    /// Placeholder for application-specific EDI file processing.
    /// Replace with your document routing, transformation, or storage logic.
    /// </summary>
    private static Task ProcessEdiFileAsync(long parcelId, byte[] content)
    {
        // TODO: integrate with your EDI processor
        return Task.CompletedTask;
    }
}
```

## How to Run

```bash
cd samples/rest/ECGrid-REST-dotnet10-WorkerService
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
dotnet run
```

The worker will log each poll cycle to the console. Press `Ctrl+C` to stop gracefully.

## See Also

- [REST API Overview](../rest-api/overview.md)
- [Poll Inbound Files](../common-operations/poll-inbound-files.md)
- [Parcels — Pending Inbox List](../rest-api/parcels/pending-inbox-list.md)
- [Parcels — Confirm Download](../rest-api/parcels/confirm-download.md)
