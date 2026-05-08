// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: Manual SOAP client using HttpClient + XDocument - Greg Kolinski
// ------------------------------------------------------------

using System.Net.Http.Headers;
using System.Xml.Linq;

namespace ECGrid.Soap.HttpClient;

/// <summary>
/// Lightweight manual SOAP client for the ECGridOS v4.1 API.
/// Wraps raw HTTP calls in typed async methods — no WCF or generated proxy required.
/// </summary>
public sealed class EcGridSoapClient
{
    private readonly System.Net.Http.HttpClient _http;

    // SOAP namespace declared in the ECGridOS WSDL
    private static readonly XNamespace Ns = "http://www.ecgridos.net/";

    // Standard SOAP 1.1 envelope namespace
    private static readonly XNamespace SoapNs = "http://schemas.xmlsoap.org/soap/envelope/";

    /// <summary>
    /// Initializes the client using a named HttpClient from IHttpClientFactory.
    /// The factory manages connection pooling and lifetime — never call new HttpClient() directly.
    /// </summary>
    /// <param name="factory">The DI-registered HttpClient factory.</param>
    public EcGridSoapClient(IHttpClientFactory factory)
    {
        _http = factory.CreateClient("ecgridsoap");
    }

    // -----------------------------------------------------------------------
    // Auth
    // -----------------------------------------------------------------------

    /// <summary>
    /// Authenticates with ECGridOS and returns an active session token.
    /// Store this token and pass it as the first argument to every subsequent call.
    /// </summary>
    /// <param name="userName">ECGrid user name (email address).</param>
    /// <param name="password">ECGrid account password.</param>
    /// <returns>A session ID string valid for the duration of the session.</returns>
    public async Task<string> LoginAsync(string userName, string password)
    {
        const string action = "http://www.ecgridos.net/Login";
        var body = $"""
            <Login xmlns="http://www.ecgridos.net/">
              <UserName>{Escape(userName)}</UserName>
              <Password>{Escape(password)}</Password>
            </Login>
            """;

        var doc = await PostSoapAsync(action, body);
        // ECGridOS returns the session ID as the text content of <LoginResult>
        return doc.Descendants(Ns + "LoginResult").First().Value;
    }

    /// <summary>
    /// Terminates the active session associated with the supplied session ID.
    /// Always call this in a finally block to avoid leaving orphaned sessions on the server.
    /// </summary>
    /// <param name="sessionId">Active session token obtained from <see cref="LoginAsync"/>.</param>
    /// <returns><c>true</c> if the session was successfully terminated.</returns>
    public async Task<bool> LogoutAsync(string sessionId)
    {
        const string action = "http://www.ecgridos.net/Logout";
        var body = $"""
            <Logout xmlns="http://www.ecgridos.net/">
              <SessionID>{Escape(sessionId)}</SessionID>
            </Logout>
            """;

        var doc = await PostSoapAsync(action, body);
        var raw = doc.Descendants(Ns + "LogoutResult").FirstOrDefault()?.Value;
        return bool.TryParse(raw, out var result) && result;
    }

    // -----------------------------------------------------------------------
    // Parcels
    // -----------------------------------------------------------------------

    /// <summary>
    /// Returns a list of parcels waiting in the inbound queue for the specified mailbox.
    /// Each tuple contains the parcel ID and original file name.
    /// </summary>
    /// <param name="sessionId">Active session token.</param>
    /// <param name="networkId">Network ID (0 = use session default).</param>
    /// <param name="mailboxId">Mailbox ID (0 = use session default).</param>
    /// <returns>List of (parcelId, fileName) tuples; empty list when the inbox is clear.</returns>
    public async Task<List<(long ParcelId, string FileName)>> ParcelInBoxAsync(
        string sessionId, int networkId = 0, int mailboxId = 0)
    {
        const string action = "http://www.ecgridos.net/ParcelInBox";
        var body = $"""
            <ParcelInBox xmlns="http://www.ecgridos.net/">
              <SessionID>{Escape(sessionId)}</SessionID>
              <NetworkID>{networkId}</NetworkID>
              <MailboxID>{mailboxId}</MailboxID>
            </ParcelInBox>
            """;

        var doc = await PostSoapAsync(action, body);

        // The response contains zero or more <ParcelIDInfo> elements.
        return doc
            .Descendants(Ns + "ParcelIDInfo")
            .Select(p => (
                ParcelId: long.Parse(p.Element(Ns + "ParcelID")?.Value ?? "0"),
                FileName: p.Element(Ns + "FileName")?.Value ?? string.Empty))
            .ToList();
    }

    /// <summary>
    /// Downloads the raw EDI content of a parcel as a byte array.
    /// The parcel remains in the inbound queue until confirmed — see <see cref="ParcelDownloadConfirmAsync"/>.
    /// </summary>
    /// <param name="sessionId">Active session token.</param>
    /// <param name="parcelId">Numeric parcel identifier from the inbox list.</param>
    /// <returns>Raw EDI bytes for the parcel.</returns>
    public async Task<byte[]> ParcelDownloadAsync(string sessionId, long parcelId)
    {
        const string action = "http://www.ecgridos.net/ParcelDownload";
        var body = $"""
            <ParcelDownload xmlns="http://www.ecgridos.net/">
              <SessionID>{Escape(sessionId)}</SessionID>
              <ParcelID>{parcelId}</ParcelID>
            </ParcelDownload>
            """;

        var doc = await PostSoapAsync(action, body);
        // ECGridOS returns file content base64-encoded inside <ParcelDownloadResult>
        var base64 = doc.Descendants(Ns + "ParcelDownloadResult").First().Value;
        return Convert.FromBase64String(base64);
    }

    /// <summary>
    /// Confirms that a parcel has been successfully received and processed.
    /// ECGridOS will not re-deliver the parcel after confirmation.
    /// Always call this after saving the downloaded content to durable storage.
    /// </summary>
    /// <param name="sessionId">Active session token.</param>
    /// <param name="parcelId">Parcel ID to confirm.</param>
    /// <returns><c>true</c> if confirmation was accepted by the server.</returns>
    public async Task<bool> ParcelDownloadConfirmAsync(string sessionId, long parcelId)
    {
        const string action = "http://www.ecgridos.net/ParcelDownloadConfirm";
        var body = $"""
            <ParcelDownloadConfirm xmlns="http://www.ecgridos.net/">
              <SessionID>{Escape(sessionId)}</SessionID>
              <ParcelID>{parcelId}</ParcelID>
            </ParcelDownloadConfirm>
            """;

        var doc = await PostSoapAsync(action, body);
        var raw = doc.Descendants(Ns + "ParcelDownloadConfirmResult").FirstOrDefault()?.Value;
        return bool.TryParse(raw, out var result) && result;
    }

    // -----------------------------------------------------------------------
    // Internal helpers
    // -----------------------------------------------------------------------

    /// <summary>
    /// Wraps an operation-specific XML fragment in a complete SOAP 1.1 envelope,
    /// POSTs it to the ECGridOS endpoint, and returns the parsed response document.
    /// </summary>
    /// <param name="soapAction">Value for the SOAPAction HTTP header.</param>
    /// <param name="bodyXml">Inner XML content to place inside the SOAP Body element.</param>
    /// <returns>Parsed <see cref="XDocument"/> containing the SOAP response.</returns>
    private async Task<XDocument> PostSoapAsync(string soapAction, string bodyXml)
    {
        var envelope = $"""
            <?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope
              xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xmlns:xsd="http://www.w3.org/2001/XMLSchema">
              <soap:Body>
                {bodyXml}
              </soap:Body>
            </soap:Envelope>
            """;

        using var request = new HttpRequestMessage(HttpMethod.Post, string.Empty)
        {
            Content = new StringContent(envelope, System.Text.Encoding.UTF8, "text/xml")
        };

        // SOAPAction header is required by the ECGridOS SOAP 1.1 endpoint
        request.Headers.Add("SOAPAction", soapAction);

        var response = await _http.SendAsync(request);
        response.EnsureSuccessStatusCode();

        var xml = await response.Content.ReadAsStringAsync();
        return XDocument.Parse(xml);
    }

    /// <summary>
    /// Escapes characters that would break the hand-built XML fragments.
    /// Input values come from configuration, not from untrusted user input, but we
    /// still sanitise to prevent accidental injection via special characters in credentials.
    /// </summary>
    private static string Escape(string value) =>
        System.Security.SecurityElement.Escape(value) ?? value;
}
