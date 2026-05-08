// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: EcGridService implementation using IHttpClientFactory - Greg Kolinski
// 2026-05-07: Updated inbox polling to use pending-inbox-list endpoint - Greg Kolinski
// ------------------------------------------------------------

using ECGrid_REST_dotnet10_AspNetCore_MVC.Models;
using System.Net.Http.Json;
using System.Text.Json;

namespace ECGrid_REST_dotnet10_AspNetCore_MVC.Services;

/// <summary>
/// Implements <see cref="IEcGridService"/> by calling the ECGrid REST API
/// through the named <c>ecgrid</c> HttpClient registered in <c>Program.cs</c>.
/// </summary>
public sealed class EcGridService : IEcGridService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<EcGridService> _logger;

    // Shared options keep camelCase deserialization consistent across all calls
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy        = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
    };

    /// <summary>
    /// Initializes a new instance of <see cref="EcGridService"/>.
    /// </summary>
    /// <param name="httpClientFactory">Factory that creates the named <c>ecgrid</c> client.</param>
    /// <param name="logger">Logger for diagnostic output.</param>
    public EcGridService(IHttpClientFactory httpClientFactory, ILogger<EcGridService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger            = logger;
    }

    /// <inheritdoc/>
    public async Task<IEnumerable<ParcelSummary>> GetInboxAsync(
        int mailboxId = 0, CancellationToken cancellationToken = default)
    {
        using var http = _httpClientFactory.CreateClient("ecgrid");

        var request = new PendingInboxListRequest(
            MailboxId:      mailboxId,
            PageNo:         1,
            RecordsPerPage: 25);

        var response = await http.PostAsJsonAsync("v2/parcels/pending-inbox-list", request, JsonOptions, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ApiResponse<List<ParcelSummary>>>(JsonOptions, cancellationToken);

        if (result?.Success != true)
        {
            _logger.LogWarning("Inbox list returned success=false: {Message}", result?.Message);
            return Enumerable.Empty<ParcelSummary>();
        }

        return result.Data ?? Enumerable.Empty<ParcelSummary>();
    }

    /// <inheritdoc/>
    public async Task<ParcelDownload?> DownloadParcelAsync(
        long parcelId, CancellationToken cancellationToken = default)
    {
        using var http = _httpClientFactory.CreateClient("ecgrid");

        var request  = new ParcelIdRequest(ParcelId: parcelId);
        var response = await http.PostAsJsonAsync("v2/parcels/download", request, JsonOptions, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ApiResponse<ParcelDownload>>(JsonOptions, cancellationToken);

        if (result?.Success != true)
        {
            _logger.LogWarning("Download of parcel {ParcelId} returned success=false: {Message}",
                parcelId, result?.Message);
            return null;
        }

        return result.Data;
    }

    /// <inheritdoc/>
    public async Task<bool> ConfirmDownloadAsync(
        long parcelId, CancellationToken cancellationToken = default)
    {
        using var http = _httpClientFactory.CreateClient("ecgrid");

        var request  = new ParcelIdRequest(ParcelId: parcelId);
        var response = await http.PostAsJsonAsync("v2/parcels/confirm", request, JsonOptions, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ApiResponse<object>>(JsonOptions, cancellationToken);

        if (result?.Success != true)
            _logger.LogWarning("Confirm of parcel {ParcelId} returned success=false: {Message}",
                parcelId, result?.Message);

        return result?.Success == true;
    }

    /// <inheritdoc/>
    public async Task<long> UploadParcelAsync(
        string fileName, byte[] content, CancellationToken cancellationToken = default)
    {
        using var http = _httpClientFactory.CreateClient("ecgrid");

        var base64Content = Convert.ToBase64String(content);
        var request = new UploadRequest(
            FileName: fileName,
            Content:  base64Content,
            Bytes:    content.Length);

        var response = await http.PostAsJsonAsync("v2/parcels/upload", request, JsonOptions, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ApiResponse<UploadResult>>(JsonOptions, cancellationToken);

        if (result?.Success != true || result.Data is null)
        {
            _logger.LogWarning("Upload of {FileName} returned success=false: {Message}",
                fileName, result?.Message);
            throw new InvalidOperationException($"ECGrid upload failed: {result?.Message}");
        }

        return result.Data.ParcelId;
    }
}
