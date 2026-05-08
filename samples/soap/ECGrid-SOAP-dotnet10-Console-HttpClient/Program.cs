// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: SOAP HttpClient console entry point - Greg Kolinski
// ------------------------------------------------------------

using ECGrid.Soap.HttpClient;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

// ---------------------------------------------------------------------------
// 1. Build configuration — credentials come from appsettings.json or
//    environment variables (e.g. ECGRID__USERNAME, ECGRID__PASSWORD).
//    Never hardcode credentials in source.
// ---------------------------------------------------------------------------
var config = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false)
    .AddEnvironmentVariables()
    .Build();

var ecgridSection = config.GetSection("ECGrid");
var userName = ecgridSection["UserName"] ?? throw new InvalidOperationException("ECGrid:UserName is required.");
var password  = ecgridSection["Password"] ?? throw new InvalidOperationException("ECGrid:Password is required.");
var baseUrl   = ecgridSection["BaseUrl"]  ?? "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";

// ---------------------------------------------------------------------------
// 2. Configure DI — IHttpClientFactory manages socket lifetime so we never
//    instantiate HttpClient directly.
// ---------------------------------------------------------------------------
var services = new ServiceCollection();

services.AddHttpClient("ecgridsoap", client =>
{
    // The base address must end with the ASMX path; individual requests post
    // to this same URL using an empty relative path.
    client.BaseAddress = new Uri(baseUrl);
    // SOAP 1.1 requires text/xml; the content type is also set per-request
    // inside PostSoapAsync, but setting a default here ensures consistency.
    client.DefaultRequestHeaders.Add("Accept", "text/xml");
});

services.AddTransient<EcGridSoapClient>();

var provider = services.BuildServiceProvider();
var soapClient = provider.GetRequiredService<EcGridSoapClient>();

// ---------------------------------------------------------------------------
// 3. Run the inbound file polling workflow
// ---------------------------------------------------------------------------
string? sessionId = null;

try
{
    // Step 1 — Authenticate
    Console.WriteLine("Logging in...");
    sessionId = await soapClient.LoginAsync(userName, password);
    Console.WriteLine($"Session established: {sessionId[..8]}…");

    // Step 2 — Check inbox
    Console.WriteLine("Checking inbound queue...");
    var parcels = await soapClient.ParcelInBoxAsync(sessionId);

    if (parcels.Count == 0)
    {
        Console.WriteLine("Inbox is empty.");
        return;
    }

    Console.WriteLine($"Found {parcels.Count} parcel(s) in inbox.");

    // Step 3 — Download, save, then confirm each parcel
    // Confirm only AFTER the file is successfully saved to durable storage.
    // Confirming before saving risks data loss if the process crashes mid-loop.
    foreach (var (parcelId, fileName) in parcels)
    {
        Console.WriteLine($"  Downloading parcel {parcelId} ({fileName})...");
        var data = await soapClient.ParcelDownloadAsync(sessionId, parcelId);

        // Sanitize the server-supplied file name before writing to disk
        var safeName = Path.GetFileName(fileName);
        if (string.IsNullOrWhiteSpace(safeName))
            safeName = $"parcel_{parcelId}.edi";

        var outputPath = Path.Combine(AppContext.BaseDirectory, "downloads", safeName);
        Directory.CreateDirectory(Path.GetDirectoryName(outputPath)!);
        await File.WriteAllBytesAsync(outputPath, data);
        Console.WriteLine($"    Saved to: {outputPath}");

        // Step 4 — Confirm download so ECGridOS removes it from the queue
        var confirmed = await soapClient.ParcelDownloadConfirmAsync(sessionId, parcelId);
        Console.WriteLine($"    Confirmed: {confirmed}");
    }

    Console.WriteLine("All parcels processed successfully.");
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error: {ex.Message}");
    Environment.ExitCode = 1;
}
finally
{
    // Always log out to release the server-side session, even if an error occurred
    if (sessionId is not null)
    {
        try
        {
            await soapClient.LogoutAsync(sessionId);
            Console.WriteLine("Session terminated.");
        }
        catch (Exception logoutEx)
        {
            Console.Error.WriteLine($"Logout warning: {logoutEx.Message}");
        }
    }
}
