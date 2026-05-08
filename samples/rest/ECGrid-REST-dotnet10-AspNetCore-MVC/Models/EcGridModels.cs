// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: ECGrid REST API model/record types for MVC sample - Greg Kolinski
// 2026-05-07: Updated InboxListRequest to PendingInboxListRequest for pending-inbox-list - Greg Kolinski
// ------------------------------------------------------------

using System.Text.Json.Serialization;

namespace ECGrid_REST_dotnet10_AspNetCore_MVC.Models;

// ---------------------------------------------------------------------------
// Generic API envelope — every ECGrid REST response uses this wrapper
// ---------------------------------------------------------------------------

/// <summary>
/// Standard response envelope returned by all ECGrid REST endpoints.
/// </summary>
/// <typeparam name="T">The type of the <c>data</c> payload.</typeparam>
public record ApiResponse<T>(
    [property: JsonPropertyName("success")] bool    Success,
    [property: JsonPropertyName("data")]    T?      Data,
    [property: JsonPropertyName("message")] string? Message);

// ---------------------------------------------------------------------------
// Request bodies
// ---------------------------------------------------------------------------

/// <summary>Request body for POST /v2/parcels/pending-inbox-list.</summary>
public record PendingInboxListRequest(
    [property: JsonPropertyName("mailboxId")]      int    MailboxId,
    [property: JsonPropertyName("pageNo")]         int    PageNo,
    [property: JsonPropertyName("recordsPerPage")] int    RecordsPerPage);

/// <summary>Request body for POST /v2/parcels/download and POST /v2/parcels/confirm.</summary>
public record ParcelIdRequest(
    [property: JsonPropertyName("parcelId")] long ParcelId);

/// <summary>Request body for POST /v2/parcels/upload.</summary>
public record UploadRequest(
    [property: JsonPropertyName("fileName")] string FileName,
    [property: JsonPropertyName("content")]  string Content,
    [property: JsonPropertyName("bytes")]    int    Bytes);

// ---------------------------------------------------------------------------
// Response / view model types
// ---------------------------------------------------------------------------

/// <summary>
/// Summary of a single parcel returned by the inbox-list endpoint.
/// Used as a view model on the Inbox page.
/// </summary>
public record ParcelSummary(
    [property: JsonPropertyName("parcelId")]  long    ParcelId,
    [property: JsonPropertyName("fileName")]  string? FileName,
    [property: JsonPropertyName("bytes")]     long    Bytes,
    [property: JsonPropertyName("status")]    string? Status,
    [property: JsonPropertyName("createdOn")] string? CreatedOn);

/// <summary>
/// Full parcel payload returned by POST /v2/parcels/download.
/// The <c>Content</c> field is a base-64 encoded EDI file body.
/// </summary>
public record ParcelDownload(
    [property: JsonPropertyName("parcelId")]  long    ParcelId,
    [property: JsonPropertyName("fileName")]  string? FileName,
    [property: JsonPropertyName("content")]   string? Content,
    [property: JsonPropertyName("bytes")]     long    Bytes);

/// <summary>
/// Minimal result returned by POST /v2/parcels/upload.
/// </summary>
public record UploadResult(
    [property: JsonPropertyName("parcelId")] long ParcelId);
