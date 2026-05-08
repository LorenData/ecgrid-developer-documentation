// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: ECGrid REST Minimal API proxy sample - Greg Kolinski
// 2026-05-07: Updated /inbox route to proxy pending-inbox-list endpoint - Greg Kolinski
// ------------------------------------------------------------

using System.Net.Http.Headers;

var builder = WebApplication.CreateBuilder(args);

// Bind ECGrid configuration section
var ecgridSection = builder.Configuration.GetSection("ECGrid");
var baseUrl = ecgridSection["BaseUrl"] ?? "https://rest.ecgrid.io";
var apiKey  = ecgridSection["ApiKey"]  ?? throw new InvalidOperationException(
    "ECGrid:ApiKey is required. Set it in appsettings.json or via the ECGRID__APIKEY environment variable.");

// Register a named HttpClient for all ECGrid REST calls.
// Default request headers are applied once here so individual route handlers
// do not have to repeat them — the factory reuses the underlying socket pool.
builder.Services.AddHttpClient("ecgrid", client =>
{
    client.BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/");
    client.DefaultRequestHeaders.Add("X-API-Key", apiKey);
    client.DefaultRequestHeaders.Accept.Add(
        new MediaTypeWithQualityHeaderValue("application/json"));
});

var app = builder.Build();

// ---------------------------------------------------------------------------
// GET /inbox
// Fetches pending inbound parcels for the authenticated mailbox by
// proxying to POST /v2/parcels/pending-inbox-list on the ECGrid REST API.
// ---------------------------------------------------------------------------
app.MapGet("/inbox", async (IHttpClientFactory factory) =>
{
    var http = factory.CreateClient("ecgrid");

    // pending-inbox-list returns only parcels awaiting download for the API key's mailbox
    var response = await http.PostAsJsonAsync("v2/parcels/pending-inbox-list", new { });

    if (!response.IsSuccessStatusCode)
    {
        var error = await response.Content.ReadAsStringAsync();
        return Results.Problem(
            detail:     error,
            statusCode: (int)response.StatusCode,
            title:      "ECGrid pending-inbox-list error");
    }

    var json = await response.Content.ReadFromJsonAsync<object>();
    return Results.Ok(json);
});

// ---------------------------------------------------------------------------
// GET /parcel/{id}
// Returns metadata for a single parcel by proxying to GET /v2/parcels/{id}.
// ---------------------------------------------------------------------------
app.MapGet("/parcel/{id:long}", async (long id, IHttpClientFactory factory) =>
{
    var http = factory.CreateClient("ecgrid");

    var response = await http.GetAsync($"v2/parcels/{id}");

    if (!response.IsSuccessStatusCode)
    {
        var error = await response.Content.ReadAsStringAsync();
        return Results.Problem(
            detail:     error,
            statusCode: (int)response.StatusCode,
            title:      "ECGrid parcel lookup error");
    }

    var json = await response.Content.ReadFromJsonAsync<object>();
    return Results.Ok(json);
});

// ---------------------------------------------------------------------------
// POST /upload
// Accepts a multipart/form-data request containing an EDI file and proxies it
// to POST /v2/parcels/upload on the ECGrid REST API, returning the new parcel ID.
//
// Expected form fields:
//   file      — the EDI file (required)
//   mailboxId — destination mailbox ID (optional; defaults to API-key mailbox)
// ---------------------------------------------------------------------------
app.MapPost("/upload", async (HttpRequest request, IHttpClientFactory factory) =>
{
    if (!request.HasFormContentType)
        return Results.BadRequest("Request must be multipart/form-data.");

    var form = await request.ReadFormAsync();
    var file = form.Files.GetFile("file");

    if (file is null || file.Length == 0)
        return Results.BadRequest("A non-empty 'file' field is required.");

    var http = factory.CreateClient("ecgrid");

    // Build a multipart form matching the ECGrid upload contract.
    using var content = new MultipartFormDataContent();
    await using var stream = file.OpenReadStream();
    var fileContent = new StreamContent(stream);
    fileContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
    content.Add(fileContent, "file", file.FileName);

    // Forward optional mailboxId if provided by the caller.
    if (form.TryGetValue("mailboxId", out var mailboxId) && !string.IsNullOrWhiteSpace(mailboxId))
        content.Add(new StringContent(mailboxId!), "mailboxId");

    var response = await http.PostAsync("v2/parcels/upload", content);

    if (!response.IsSuccessStatusCode)
    {
        var error = await response.Content.ReadAsStringAsync();
        return Results.Problem(
            detail:     error,
            statusCode: (int)response.StatusCode,
            title:      "ECGrid upload error");
    }

    var result = await response.Content.ReadFromJsonAsync<object>();
    return Results.Ok(result);
});

// ---------------------------------------------------------------------------
// POST /confirm/{id}
// Confirms download of a parcel by proxying to POST /v2/parcels/confirm on the
// ECGrid REST API.  Call this after successfully processing a downloaded parcel.
// ---------------------------------------------------------------------------
app.MapPost("/confirm/{id:long}", async (long id, IHttpClientFactory factory) =>
{
    var http = factory.CreateClient("ecgrid");

    var response = await http.PostAsJsonAsync("v2/parcels/confirm", new { parcelID = id });

    if (!response.IsSuccessStatusCode)
    {
        var error = await response.Content.ReadAsStringAsync();
        return Results.Problem(
            detail:     error,
            statusCode: (int)response.StatusCode,
            title:      "ECGrid confirm error");
    }

    var result = await response.Content.ReadFromJsonAsync<object>();
    return Results.Ok(result);
});

app.Run();
