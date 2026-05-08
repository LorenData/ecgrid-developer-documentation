// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: MVC controller exposing ECGrid parcel inbox, download, and upload actions - Greg Kolinski
// ------------------------------------------------------------

using ECGrid_REST_dotnet10_AspNetCore_MVC.Services;
using Microsoft.AspNetCore.Mvc;

namespace ECGrid_REST_dotnet10_AspNetCore_MVC.Controllers;

/// <summary>
/// MVC controller that exposes ECGrid parcel operations as HTTP endpoints.
/// All heavy lifting is delegated to <see cref="IEcGridService"/> so the
/// controller remains thin and unit-testable.
/// </summary>
public sealed class EcGridController : Controller
{
    private readonly IEcGridService _ecGridService;
    private readonly ILogger<EcGridController> _logger;

    /// <summary>
    /// Initializes a new instance of <see cref="EcGridController"/>.
    /// </summary>
    /// <param name="ecGridService">The ECGrid service abstraction.</param>
    /// <param name="logger">Logger for diagnostic output.</param>
    public EcGridController(IEcGridService ecGridService, ILogger<EcGridController> logger)
    {
        _ecGridService = ecGridService;
        _logger        = logger;
    }

    // -----------------------------------------------------------------------
    // GET /ECGrid/Inbox
    // -----------------------------------------------------------------------

    /// <summary>
    /// Displays a list of parcels currently in the ECGrid inbox with status <c>InBoxReady</c>.
    /// </summary>
    [HttpGet]
    public async Task<IActionResult> Inbox(CancellationToken cancellationToken)
    {
        try
        {
            var parcels = await _ecGridService.GetInboxAsync(cancellationToken: cancellationToken);
            return View(parcels);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Failed to retrieve inbox.");
            return View("Error", new ErrorViewModel(ex.Message));
        }
    }

    // -----------------------------------------------------------------------
    // POST /ECGrid/Download/{parcelId}
    // -----------------------------------------------------------------------

    /// <summary>
    /// Downloads the specified parcel from ECGrid, confirms the download, and
    /// returns the file bytes to the browser.
    /// </summary>
    /// <param name="parcelId">The ECGrid parcel ID to download.</param>
    /// <param name="cancellationToken">Propagates notification that the request has been aborted.</param>
    [HttpPost]
    [Route("ECGrid/Download/{parcelId:long}")]
    public async Task<IActionResult> Download(long parcelId, CancellationToken cancellationToken)
    {
        try
        {
            var download = await _ecGridService.DownloadParcelAsync(parcelId, cancellationToken);

            if (download is null)
                return NotFound($"Parcel {parcelId} could not be downloaded.");

            // Decode the base-64 content returned by ECGrid
            var fileBytes = Convert.FromBase64String(download.Content ?? string.Empty);
            var fileName  = download.FileName ?? $"parcel-{parcelId}.edi";

            // Confirm after successful decode so we don't confirm a corrupted download
            await _ecGridService.ConfirmDownloadAsync(parcelId, cancellationToken);

            // Return as a downloadable file attachment
            return File(fileBytes, "application/octet-stream", fileName);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Failed to download parcel {ParcelId}.", parcelId);
            return StatusCode(StatusCodes.Status502BadGateway, "ECGrid API error: " + ex.Message);
        }
    }

    // -----------------------------------------------------------------------
    // GET /ECGrid/Upload  (form display)
    // POST /ECGrid/Upload (form submit)
    // -----------------------------------------------------------------------

    /// <summary>
    /// Displays the file upload form.
    /// </summary>
    [HttpGet]
    public IActionResult Upload() => View();

    /// <summary>
    /// Accepts a file upload from the browser form, sends it to ECGrid, and
    /// redirects back to the inbox on success.
    /// </summary>
    /// <param name="file">The file selected by the user.</param>
    /// <param name="cancellationToken">Propagates notification that the request has been aborted.</param>
    [HttpPost]
    public async Task<IActionResult> Upload(IFormFile file, CancellationToken cancellationToken)
    {
        if (file is null || file.Length == 0)
        {
            ModelState.AddModelError(string.Empty, "Please select a file to upload.");
            return View();
        }

        try
        {
            using var memoryStream = new MemoryStream();
            await file.CopyToAsync(memoryStream, cancellationToken);
            var content = memoryStream.ToArray();

            var parcelId = await _ecGridService.UploadParcelAsync(file.FileName, content, cancellationToken);

            _logger.LogInformation("Uploaded {FileName} as parcel {ParcelId}.", file.FileName, parcelId);
            TempData["UploadSuccess"] = $"File '{file.FileName}' uploaded successfully. Parcel ID: {parcelId}";

            return RedirectToAction(nameof(Inbox));
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Failed to upload {FileName}.", file.FileName);
            ModelState.AddModelError(string.Empty, "ECGrid upload failed: " + ex.Message);
            return View();
        }
    }
}

// ---------------------------------------------------------------------------
// Minimal view model for the shared error view
// ---------------------------------------------------------------------------

/// <summary>View model carrying an error message to the shared Error view.</summary>
public record ErrorViewModel(string Message);
