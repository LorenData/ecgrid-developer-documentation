// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: BackgroundService that polls ECGrid inbox and downloads ready parcels - Greg Kolinski
// 2026-05-07: Updated inbox polling to use pending-inbox-list endpoint - Greg Kolinski
// ------------------------------------------------------------

using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace ECGrid_REST_dotnet10_WorkerService;

/// <summary>
/// A long-running background service that polls the ECGrid inbox on a
/// configurable interval, downloads ready parcels, saves them to disk,
/// and confirms each download so ECGrid marks the parcel as transferred.
/// </summary>
public sealed class EcGridPollingWorker : BackgroundService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly IConfiguration     _configuration;
    private readonly ILogger<EcGridPollingWorker> _logger;

    // Shared JSON options — camelCase matches ECGrid REST response property names
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy        = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
        DefaultIgnoreCondition      = JsonIgnoreCondition.WhenWritingNull,
    };

    /// <summary>
    /// Initializes a new instance of <see cref="EcGridPollingWorker"/>.
    /// </summary>
    /// <param name="httpClientFactory">Factory used to create the named <c>ecgrid</c> client.</param>
    /// <param name="configuration">Application configuration (provides <c>ECGrid:PollIntervalSeconds</c>).</param>
    /// <param name="logger">Logger for operational and diagnostic messages.</param>
    public EcGridPollingWorker(
        IHttpClientFactory            httpClientFactory,
        IConfiguration                configuration,
        ILogger<EcGridPollingWorker>  logger)
    {
        _httpClientFactory = httpClientFactory;
        _configuration     = configuration;
        _logger            = logger;
    }

    /// <inheritdoc/>
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // Read poll interval from configuration; fall back to 30 seconds
        var intervalSeconds = _configuration.GetValue<int>("ECGrid:PollIntervalSeconds", 30);
        var interval        = TimeSpan.FromSeconds(intervalSeconds);

        _logger.LogInformation(
            "ECGrid Polling Worker started. Poll interval: {Interval}s.", intervalSeconds);

        // PeriodicTimer is the idiomatic .NET way to schedule recurring work
        // without Thread.Sleep; it respects the cancellation token natively
        using var timer = new PeriodicTimer(interval);

        while (!stoppingToken.IsCancellationRequested &&
               await timer.WaitForNextTickAsync(stoppingToken))
        {
            await PollInboxAsync(stoppingToken);
        }

        _logger.LogInformation("ECGrid Polling Worker stopped.");
    }

    // -----------------------------------------------------------------------
    // Private helpers
    // -----------------------------------------------------------------------

    /// <summary>
    /// Queries the ECGrid inbox, then downloads and confirms each ready parcel.
    /// </summary>
    private async Task PollInboxAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Polling ECGrid inbox at {Time}.", DateTimeOffset.UtcNow);

        List<ParcelSummary> parcels;

        try
        {
            parcels = await GetInboxAsync(cancellationToken);
            _logger.LogInformation("Found {Count} parcel(s) ready for download.", parcels.Count);
        }
        catch (Exception ex)
        {
            // A failure to reach the inbox does not crash the worker; it logs and waits for next tick
            _logger.LogError(ex, "Failed to retrieve inbox list from ECGrid.");
            return;
        }

        // Ensure the output directory exists before processing any parcel
        var outputDir = Path.Combine(AppContext.BaseDirectory, "output");
        Directory.CreateDirectory(outputDir);

        foreach (var parcel in parcels)
        {
            // Per-parcel error handling — one bad file must not stop the rest of the loop
            try
            {
                await ProcessParcelAsync(parcel, outputDir, cancellationToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Error processing parcel {ParcelId} ({FileName}). Skipping.",
                    parcel.ParcelId, parcel.FileName);
            }
        }
    }

    /// <summary>
    /// Downloads a single parcel, writes it to <paramref name="outputDir"/>, and confirms receipt.
    /// </summary>
    private async Task ProcessParcelAsync(
        ParcelSummary parcel, string outputDir, CancellationToken cancellationToken)
    {
        _logger.LogDebug("Downloading parcel {ParcelId} — {FileName}.", parcel.ParcelId, parcel.FileName);

        using var http = _httpClientFactory.CreateClient("ecgrid");

        // --- Download ---
        var downloadRequest  = new ParcelIdRequest(ParcelId: parcel.ParcelId);
        var downloadResponse = await http.PostAsJsonAsync(
            "v2/parcels/download", downloadRequest, JsonOptions, cancellationToken);
        downloadResponse.EnsureSuccessStatusCode();

        var download = await downloadResponse.Content
            .ReadFromJsonAsync<ApiResponse<ParcelDownload>>(JsonOptions, cancellationToken);

        if (download?.Success != true || download.Data is null)
        {
            _logger.LogWarning("Download of parcel {ParcelId} returned success=false.", parcel.ParcelId);
            return;
        }

        // Decode base-64 EDI content before confirming — avoid confirming a corrupt payload
        var fileBytes = Convert.FromBase64String(download.Data.Content ?? string.Empty);
        var fileName  = download.Data.FileName ?? $"parcel-{parcel.ParcelId}.edi";
        var savePath  = Path.Combine(outputDir, fileName);

        await File.WriteAllBytesAsync(savePath, fileBytes, cancellationToken);
        _logger.LogInformation(
            "Saved parcel {ParcelId} → {Path} ({Bytes:N0} bytes).",
            parcel.ParcelId, savePath, fileBytes.Length);

        // --- Confirm ---
        var confirmRequest  = new ParcelIdRequest(ParcelId: parcel.ParcelId);
        var confirmResponse = await http.PostAsJsonAsync(
            "v2/parcels/confirm", confirmRequest, JsonOptions, cancellationToken);
        confirmResponse.EnsureSuccessStatusCode();

        var confirm = await confirmResponse.Content
            .ReadFromJsonAsync<ApiResponse<object>>(JsonOptions, cancellationToken);

        if (confirm?.Success == true)
            _logger.LogInformation("Confirmed parcel {ParcelId}.", parcel.ParcelId);
        else
            _logger.LogWarning("Confirm call for parcel {ParcelId} returned success=false.", parcel.ParcelId);
    }

    /// <summary>
    /// Calls POST /v2/parcels/pending-inbox-list and returns the list of ready parcels.
    /// </summary>
    private async Task<List<ParcelSummary>> GetInboxAsync(CancellationToken cancellationToken)
    {
        using var http = _httpClientFactory.CreateClient("ecgrid");

        var request = new PendingInboxListRequest(
            MailboxId:      0,
            PageNo:         1,
            RecordsPerPage: 25);

        var response = await http.PostAsJsonAsync(
            "v2/parcels/pending-inbox-list", request, JsonOptions, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ApiResponse<List<ParcelSummary>>>(JsonOptions, cancellationToken);

        return result?.Data ?? [];
    }
}

// ---------------------------------------------------------------------------
// Record types — mirror ECGrid REST API request / response shapes
// ---------------------------------------------------------------------------

/// <summary>Standard ECGrid API envelope wrapping every response payload.</summary>
file record ApiResponse<T>(
    [property: JsonPropertyName("success")] bool    Success,
    [property: JsonPropertyName("data")]    T?      Data,
    [property: JsonPropertyName("message")] string? Message);

/// <summary>Request body for POST /v2/parcels/pending-inbox-list.</summary>
file record PendingInboxListRequest(
    [property: JsonPropertyName("mailboxId")]      int    MailboxId,
    [property: JsonPropertyName("pageNo")]         int    PageNo,
    [property: JsonPropertyName("recordsPerPage")] int    RecordsPerPage);

/// <summary>Single parcel entry returned from the inbox list.</summary>
file record ParcelSummary(
    [property: JsonPropertyName("parcelId")]  long    ParcelId,
    [property: JsonPropertyName("fileName")]  string? FileName,
    [property: JsonPropertyName("bytes")]     long    Bytes,
    [property: JsonPropertyName("status")]    string? Status);

/// <summary>Request body used for both download and confirm endpoints.</summary>
file record ParcelIdRequest(
    [property: JsonPropertyName("parcelId")] long ParcelId);

/// <summary>Payload returned by POST /v2/parcels/download.</summary>
file record ParcelDownload(
    [property: JsonPropertyName("parcelId")]  long    ParcelId,
    [property: JsonPropertyName("fileName")]  string? FileName,
    [property: JsonPropertyName("content")]   string? Content,
    [property: JsonPropertyName("bytes")]     long    Bytes);
