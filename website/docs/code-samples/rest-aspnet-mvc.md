---
title: REST ASP.NET Core MVC Sample
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created REST ASP.NET Core MVC sample documentation page - Greg Kolinski */}

# REST ASP.NET Core MVC Sample

The `ECGrid-REST-dotnet10-AspNetCore-MVC` project shows how to integrate ECGrid REST into a full ASP.NET Core MVC web application. ECGrid operations are encapsulated in a typed service class that is injected into MVC controllers.

## Project Location

```
samples/rest/ECGrid-REST-dotnet10-AspNetCore-MVC/
```

## What It Demonstrates

- Registering a named `HttpClient` in `Program.cs` using `IHttpClientFactory`
- A typed `EcGridService` class that wraps all ECGrid REST calls
- An `EcGridController` MVC controller with actions for inbox, download, and upload
- API key loaded from `appsettings.json` or user-secrets — never hardcoded
- Strongly typed response models using `System.Text.Json`

## Key Files

| File | Purpose |
|---|---|
| `Program.cs` | Service registration, HttpClient configuration |
| `Services/EcGridService.cs` | Typed service wrapping ECGrid REST endpoints |
| `Controllers/EcGridController.cs` | MVC controller exposing ECGrid actions to views |
| `Models/` | Response model classes |
| `Views/EcGrid/` | Razor views for inbox, parcel detail, upload form |
| `appsettings.json` | Base configuration |

## Key Patterns

### Service Registration (`Program.cs`)

```csharp
// Program.cs — register the typed ECGrid service backed by a named HttpClient
builder.Services.AddHttpClient("ecgrid", (sp, client) =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    client.BaseAddress = new Uri(config["ECGrid:BaseUrl"]!);
    // API key injected from configuration — never stored in source code
    client.DefaultRequestHeaders.Add("X-API-Key", config["ECGrid:ApiKey"]!);
});

// Register the service so controllers can receive it via DI
builder.Services.AddScoped<EcGridService>();
```

### Typed Service (`EcGridService.cs`)

```csharp
/// <summary>
/// Wraps ECGrid REST API calls for use in ASP.NET Core controllers and services.
/// </summary>
public class EcGridService
{
    private readonly HttpClient _http;

    // IHttpClientFactory keeps connection pooling healthy — avoids socket exhaustion
    public EcGridService(IHttpClientFactory factory)
    {
        _http = factory.CreateClient("ecgrid");
    }

    /// <summary>Returns parcels waiting in the mailbox inbox.</summary>
    public async Task<List<ParcelSummary>> GetInboxAsync(int mailboxId)
    {
        var result = await _http.GetFromJsonAsync<ApiResponse<List<ParcelSummary>>>(
            $"/v2/parcels/inbox?mailboxId={mailboxId}");
        return result?.Data ?? [];
    }

    /// <summary>Downloads a parcel's EDI content as a byte array.</summary>
    public async Task<byte[]> DownloadParcelAsync(long parcelId)
    {
        var response = await _http.GetAsync($"/v2/parcels/{parcelId}/download");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadAsByteArrayAsync();
    }

    /// <summary>Confirms delivery of a downloaded parcel.</summary>
    public async Task ConfirmDownloadAsync(long parcelId)
    {
        await _http.PostAsync($"/v2/parcels/{parcelId}/confirm", null);
    }

    /// <summary>Uploads an outbound EDI file.</summary>
    public async Task<long> UploadParcelAsync(byte[] fileContent, string fileName)
    {
        using var content = new ByteArrayContent(fileContent);
        content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
        content.Headers.ContentDisposition =
            new ContentDispositionHeaderValue("attachment") { FileName = fileName };

        var response = await _http.PostAsync("/v2/parcels/upload", content);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<ApiResponse<ParcelUploadResult>>();
        return result?.Data?.ParcelId ?? 0;
    }
}
```

### MVC Controller (`EcGridController.cs`)

```csharp
/// <summary>Exposes ECGrid inbox and parcel operations as MVC actions.</summary>
public class EcGridController : Controller
{
    private readonly EcGridService _ecGrid;
    private readonly IConfiguration _config;

    public EcGridController(EcGridService ecGrid, IConfiguration config)
    {
        _ecGrid = ecGrid;
        _config = config;
    }

    /// <summary>Lists parcels in the configured mailbox inbox.</summary>
    public async Task<IActionResult> InboxList()
    {
        var mailboxId = _config.GetValue<int>("ECGrid:MailboxId");
        var parcels = await _ecGrid.GetInboxAsync(mailboxId);
        return View(parcels);
    }

    /// <summary>Downloads a parcel and returns it as a file response.</summary>
    public async Task<IActionResult> DownloadParcel(long parcelId)
    {
        var data = await _ecGrid.DownloadParcelAsync(parcelId);
        await _ecGrid.ConfirmDownloadAsync(parcelId);
        return File(data, "application/octet-stream", $"parcel-{parcelId}.edi");
    }

    [HttpPost]
    /// <summary>Accepts an EDI file upload from a form and sends it via ECGrid.</summary>
    public async Task<IActionResult> UploadParcel(IFormFile file)
    {
        using var ms = new MemoryStream();
        await file.CopyToAsync(ms);
        var parcelId = await _ecGrid.UploadParcelAsync(ms.ToArray(), file.FileName);
        return RedirectToAction(nameof(InboxList));
    }
}
```

## Configuration

```json
{
  "ECGrid": {
    "BaseUrl": "https://rest.ecgrid.io",
    "ApiKey": "",
    "MailboxId": 0
  }
}
```

Set the API key locally with user-secrets:

```bash
cd samples/rest/ECGrid-REST-dotnet10-AspNetCore-MVC
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
```

## How to Run

```bash
cd samples/rest/ECGrid-REST-dotnet10-AspNetCore-MVC
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
dotnet run
```

Then navigate to `https://localhost:5001` in your browser.

## See Also

- [REST API Overview](../rest-api/overview.md)
- [Poll Inbound Files](../common-operations/poll-inbound-files.md)
- [Download a File](../common-operations/download-a-file.md)
- [Upload a File](../common-operations/upload-a-file.md)
