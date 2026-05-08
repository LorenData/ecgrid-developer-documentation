// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: Console sample demonstrating ECGrid REST API parcel workflow - Greg Kolinski
// 2026-05-07: Updated inbox polling to use pending-inbox-list endpoint - Greg Kolinski
// ------------------------------------------------------------

using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;

// ---------------------------------------------------------------------------
// Configuration — loads appsettings.json; override with environment variables
// or dotnet user-secrets in development
// ---------------------------------------------------------------------------
var configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: false)
    .AddEnvironmentVariables()
    .Build();

var apiKey  = configuration["ECGrid:ApiKey"]  ?? throw new InvalidOperationException("ECGrid:ApiKey is not configured.");
var baseUrl = configuration["ECGrid:BaseUrl"] ?? "https://rest.ecgrid.io";

// ---------------------------------------------------------------------------
// DI container — register IHttpClientFactory with a named "ecgrid" client
// The named client centralises base address and default headers so callers
// never construct an HttpClient directly.
// ---------------------------------------------------------------------------
var services = new ServiceCollection();

services.AddHttpClient("ecgrid", client =>
{
    client.BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/");
    // X-API-Key is the authentication header for all ECGrid REST calls
    client.DefaultRequestHeaders.Add("X-API-Key", apiKey);
    client.DefaultRequestHeaders.Add("Accept", "application/json");
});

var provider = services.BuildServiceProvider();
var httpClientFactory = provider.GetRequiredService<IHttpClientFactory>();

// ---------------------------------------------------------------------------
// JSON options — use camelCase to match ECGrid REST response property names
// ---------------------------------------------------------------------------
var jsonOptions = new JsonSerializerOptions
{
    PropertyNamingPolicy        = JsonNamingPolicy.CamelCase,
    DefaultIgnoreCondition      = JsonIgnoreCondition.WhenWritingNull,
    PropertyNameCaseInsensitive = true,
};

Console.WriteLine("=== ECGrid REST API — Console Sample ===");
Console.WriteLine();

try
{
    using var http = httpClientFactory.CreateClient("ecgrid");

    // -----------------------------------------------------------------------
    // Step 1 — Verify connectivity with a version check (no auth required)
    // -----------------------------------------------------------------------
    Console.WriteLine("Step 1: Checking API version...");

    var versionResponse = await http.GetFromJsonAsync<ApiResponse<VersionData>>(
        "v2/auth/version", jsonOptions);

    if (versionResponse?.Success == true)
        Console.WriteLine($"  API version: {versionResponse.Data?.Version ?? "unknown"}");
    else
        Console.WriteLine("  Warning: version check returned an unexpected response.");

    Console.WriteLine();

    // -----------------------------------------------------------------------
    // Step 2 — Poll the inbox for ready parcels
    // -----------------------------------------------------------------------
    Console.WriteLine("Step 2: Checking inbox for ready parcels...");

    var inboxRequest = new PendingInboxListRequest(MailboxId: 0, PageNo: 1, RecordsPerPage: 25);
    var inboxResponse = await http.PostAsJsonAsync("v2/parcels/pending-inbox-list", inboxRequest, jsonOptions);
    inboxResponse.EnsureSuccessStatusCode();

    var inbox = await inboxResponse.Content.ReadFromJsonAsync<ApiResponse<List<ParcelSummary>>>(jsonOptions);

    var parcels = inbox?.Data ?? [];
    Console.WriteLine($"  Found {parcels.Count} parcel(s) ready for download.");
    Console.WriteLine();

    // -----------------------------------------------------------------------
    // Step 3 — Download each parcel, save to disk, then confirm receipt
    // -----------------------------------------------------------------------
    if (parcels.Count > 0)
    {
        var outputDir = Path.Combine(AppContext.BaseDirectory, "downloads");
        Directory.CreateDirectory(outputDir);

        foreach (var parcel in parcels)
        {
            Console.WriteLine($"  Processing parcel {parcel.ParcelId} — {parcel.FileName}...");

            try
            {
                // Download
                var downloadRequest  = new ParcelIdRequest(ParcelId: parcel.ParcelId);
                var downloadResponse = await http.PostAsJsonAsync("v2/parcels/download", downloadRequest, jsonOptions);
                downloadResponse.EnsureSuccessStatusCode();

                var download = await downloadResponse.Content
                    .ReadFromJsonAsync<ApiResponse<ParcelDownload>>(jsonOptions);

                if (download?.Success != true || download.Data is null)
                {
                    Console.WriteLine($"    Download failed for parcel {parcel.ParcelId} — skipping.");
                    continue;
                }

                // Decode base64 content and write to disk
                var fileBytes = Convert.FromBase64String(download.Data.Content ?? string.Empty);
                var savePath  = Path.Combine(outputDir, download.Data.FileName ?? $"parcel-{parcel.ParcelId}.edi");
                await File.WriteAllBytesAsync(savePath, fileBytes);
                Console.WriteLine($"    Saved to: {savePath} ({fileBytes.Length:N0} bytes)");

                // Confirm download so ECGrid marks the parcel as transferred
                var confirmRequest  = new ParcelIdRequest(ParcelId: parcel.ParcelId);
                var confirmResponse = await http.PostAsJsonAsync("v2/parcels/confirm", confirmRequest, jsonOptions);
                confirmResponse.EnsureSuccessStatusCode();

                var confirm = await confirmResponse.Content.ReadFromJsonAsync<ApiResponse<object>>(jsonOptions);
                Console.WriteLine($"    Confirmed: {confirm?.Success}");
            }
            catch (Exception ex)
            {
                // Per-parcel error handling — one bad file does not stop the loop
                Console.WriteLine($"    Error processing parcel {parcel.ParcelId}: {ex.Message}");
            }
        }
    }

    Console.WriteLine();

    // -----------------------------------------------------------------------
    // Step 4 — Upload a test file to ECGrid
    // Creates a small dummy EDI file when no real file is present so the
    // sample can be run end-to-end without pre-existing data.
    // -----------------------------------------------------------------------
    Console.WriteLine("Step 4: Uploading a test file...");

    var uploadDir  = Path.Combine(AppContext.BaseDirectory, "uploads");
    Directory.CreateDirectory(uploadDir);
    var testFilePath = Path.Combine(uploadDir, "test-edi-file.edi");

    if (!File.Exists(testFilePath))
    {
        // Minimal well-formed X12 ISA envelope used only for demonstration
        var dummyEdi =
            "ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *260101*1200*^*00501*000000001*0*T*:~" +
            "GS*PO*SENDER*RECEIVER*20260101*1200*1*X*005010~" +
            "ST*850*0001~" +
            "BEG*00*NE*TEST001**20260101~" +
            "SE*2*0001~" +
            "GE*1*1~" +
            "IEA*1*000000001~";
        await File.WriteAllTextAsync(testFilePath, dummyEdi);
        Console.WriteLine($"  Created dummy EDI file: {testFilePath}");
    }

    var uploadBytes   = await File.ReadAllBytesAsync(testFilePath);
    var uploadContent = Convert.ToBase64String(uploadBytes);
    var uploadRequest = new UploadRequest(
        FileName: Path.GetFileName(testFilePath),
        Content:  uploadContent,
        Bytes:    uploadBytes.Length);

    var uploadResponse = await http.PostAsJsonAsync("v2/parcels/upload", uploadRequest, jsonOptions);
    uploadResponse.EnsureSuccessStatusCode();

    var uploadResult = await uploadResponse.Content.ReadFromJsonAsync<ApiResponse<UploadResult>>(jsonOptions);

    if (uploadResult?.Success == true)
        Console.WriteLine($"  Upload successful. Parcel ID: {uploadResult.Data?.ParcelId}");
    else
        Console.WriteLine($"  Upload response: success={uploadResult?.Success}");

    Console.WriteLine();
    Console.WriteLine("=== Sample complete ===");
}
catch (HttpRequestException ex)
{
    Console.Error.WriteLine($"HTTP error: {ex.StatusCode} — {ex.Message}");
    return 1;
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Unexpected error: {ex.Message}");
    return 1;
}

return 0;

// ---------------------------------------------------------------------------
// Record types — mirror ECGrid REST API request / response shapes
// ---------------------------------------------------------------------------

/// <summary>Standard ECGrid API envelope wrapping every response payload.</summary>
record ApiResponse<T>(
    [property: JsonPropertyName("success")] bool   Success,
    [property: JsonPropertyName("data")]    T?     Data,
    [property: JsonPropertyName("message")] string? Message);

/// <summary>Payload returned by GET /v2/auth/version.</summary>
record VersionData(
    [property: JsonPropertyName("version")] string? Version);

/// <summary>Request body for POST /v2/parcels/pending-inbox-list.</summary>
record PendingInboxListRequest(
    [property: JsonPropertyName("mailboxId")]       int    MailboxId,
    [property: JsonPropertyName("pageNo")]          int    PageNo,
    [property: JsonPropertyName("recordsPerPage")]  int    RecordsPerPage);

/// <summary>Single parcel entry returned from the inbox list.</summary>
record ParcelSummary(
    [property: JsonPropertyName("parcelId")]  long    ParcelId,
    [property: JsonPropertyName("fileName")]  string? FileName,
    [property: JsonPropertyName("bytes")]     long    Bytes,
    [property: JsonPropertyName("status")]    string? Status);

/// <summary>Request body used for both download and confirm endpoints.</summary>
record ParcelIdRequest(
    [property: JsonPropertyName("parcelId")] long ParcelId);

/// <summary>Payload returned by POST /v2/parcels/download.</summary>
record ParcelDownload(
    [property: JsonPropertyName("parcelId")]  long    ParcelId,
    [property: JsonPropertyName("fileName")]  string? FileName,
    [property: JsonPropertyName("content")]   string? Content,
    [property: JsonPropertyName("bytes")]     long    Bytes);

/// <summary>Request body for POST /v2/parcels/upload.</summary>
record UploadRequest(
    [property: JsonPropertyName("fileName")] string FileName,
    [property: JsonPropertyName("content")]  string Content,
    [property: JsonPropertyName("bytes")]    int    Bytes);

/// <summary>Payload returned by POST /v2/parcels/upload.</summary>
record UploadResult(
    [property: JsonPropertyName("parcelId")] long ParcelId);
