// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: IEcGridService interface for ECGrid REST API MVC sample - Greg Kolinski
// ------------------------------------------------------------

using ECGrid_REST_dotnet10_AspNetCore_MVC.Models;

namespace ECGrid_REST_dotnet10_AspNetCore_MVC.Services;

/// <summary>
/// Defines the ECGrid parcel operations surfaced by this sample application.
/// </summary>
public interface IEcGridService
{
    /// <summary>
    /// Returns parcels in the mailbox inbox that have status <c>InBoxReady</c>.
    /// </summary>
    /// <param name="mailboxId">
    /// ECGrid mailbox ID to query. Pass <c>0</c> to use the account default.
    /// </param>
    /// <param name="cancellationToken">Propagates notification that the operation should be cancelled.</param>
    /// <returns>A collection of <see cref="ParcelSummary"/> records.</returns>
    Task<IEnumerable<ParcelSummary>> GetInboxAsync(int mailboxId = 0, CancellationToken cancellationToken = default);

    /// <summary>
    /// Downloads the binary content of a single parcel from ECGrid.
    /// </summary>
    /// <param name="parcelId">The unique ECGrid parcel identifier.</param>
    /// <param name="cancellationToken">Propagates notification that the operation should be cancelled.</param>
    /// <returns>A <see cref="ParcelDownload"/> record containing the base-64 encoded file content.</returns>
    Task<ParcelDownload?> DownloadParcelAsync(long parcelId, CancellationToken cancellationToken = default);

    /// <summary>
    /// Confirms receipt of a downloaded parcel, marking it as <c>InBoxTransferred</c> on ECGrid.
    /// Always call this after a successful download so the parcel is not re-delivered.
    /// </summary>
    /// <param name="parcelId">The unique ECGrid parcel identifier.</param>
    /// <param name="cancellationToken">Propagates notification that the operation should be cancelled.</param>
    /// <returns><c>true</c> if the confirmation was accepted by ECGrid.</returns>
    Task<bool> ConfirmDownloadAsync(long parcelId, CancellationToken cancellationToken = default);

    /// <summary>
    /// Uploads a file to ECGrid for delivery to the configured trading partner.
    /// </summary>
    /// <param name="fileName">The original file name (used for EDI routing and logging).</param>
    /// <param name="content">The raw file bytes to upload.</param>
    /// <param name="cancellationToken">Propagates notification that the operation should be cancelled.</param>
    /// <returns>The ECGrid parcel ID assigned to the uploaded file.</returns>
    Task<long> UploadParcelAsync(string fileName, byte[] content, CancellationToken cancellationToken = default);
}
