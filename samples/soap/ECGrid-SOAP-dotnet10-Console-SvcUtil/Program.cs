// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: SOAP svcutil proxy console entry point - Greg Kolinski
// ------------------------------------------------------------

using System.ServiceModel;
using ECGrid.Soap;
using Microsoft.Extensions.Configuration;

// ---------------------------------------------------------------------------
// NOTE: EcGridOSClientProxy.cs in this project is a STUB.
// Before running, generate the real proxy:
//
//   dotnet tool install -g dotnet-svcutil
//   dotnet-svcutil https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL \
//       --outputDir . --namespace *,ECGrid.Soap
//
// Then delete or replace EcGridOSClientProxy.cs with the generated file.
// Program.cs does NOT need to change — the constructor and method signatures
// are identical between the stub and the generated output.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// 1. Load credentials from configuration — never hardcode
// ---------------------------------------------------------------------------
var config = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false)
    .AddEnvironmentVariables()
    .Build();

var ecgridSection = config.GetSection("ECGrid");
var userName = ecgridSection["UserName"] ?? throw new InvalidOperationException("ECGrid:UserName is required.");
var password  = ecgridSection["Password"] ?? throw new InvalidOperationException("ECGrid:Password is required.");

// ---------------------------------------------------------------------------
// 2. Configure WCF binding and endpoint
//    BasicHttpsBinding matches the ECGridOS HTTPS/SOAP 1.1 transport.
// ---------------------------------------------------------------------------
var binding = new BasicHttpsBinding
{
    MaxReceivedMessageSize = 10 * 1024 * 1024, // 10 MB — accommodate large EDI files
    Security =
    {
        Mode = BasicHttpsSecurityMode.Transport
    }
};

var endpoint = new EndpointAddress("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx");
var client   = new ECGridOSClient(binding, endpoint);

// ---------------------------------------------------------------------------
// 3. Polling workflow: login → check inbox → download → confirm → logout
// ---------------------------------------------------------------------------
string? sessionId = null;

try
{
    // Step 1 — Authenticate via the generated proxy
    Console.WriteLine("Logging in...");
    sessionId = await client.LoginAsync(userName, password);
    Console.WriteLine($"Session established: {sessionId[..8]}…");

    // Step 2 — List parcels in the inbound queue
    // NetworkID = 0 and MailboxID = 0 resolve to the session-default mailbox
    Console.WriteLine("Checking inbound queue...");
    var parcels = await client.ParcelInBoxAsync(sessionId, networkID: 0, mailboxID: 0);

    if (parcels is null || parcels.Length == 0)
    {
        Console.WriteLine("Inbox is empty.");
        return;
    }

    Console.WriteLine($"Found {parcels.Length} parcel(s) in inbox.");

    // Step 3 — Download and confirm each parcel
    // The confirm call MUST happen only after the file is safely written to disk.
    foreach (var parcel in parcels)
    {
        Console.WriteLine($"  Downloading parcel {parcel.ParcelID} ({parcel.FileName})...");
        var data = await client.ParcelDownloadAsync(sessionId, parcel.ParcelID);

        var safeName = Path.GetFileName(parcel.FileName);
        if (string.IsNullOrWhiteSpace(safeName))
            safeName = $"parcel_{parcel.ParcelID}.edi";

        var outputPath = Path.Combine(AppContext.BaseDirectory, "downloads", safeName);
        Directory.CreateDirectory(Path.GetDirectoryName(outputPath)!);
        await File.WriteAllBytesAsync(outputPath, data);
        Console.WriteLine($"    Saved to: {outputPath}");

        var confirmed = await client.ParcelDownloadConfirmAsync(sessionId, parcel.ParcelID);
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
    // Release the server-side session regardless of success or failure
    if (sessionId is not null)
    {
        try
        {
            await client.LogoutAsync(sessionId);
            Console.WriteLine("Session terminated.");
        }
        catch (Exception logoutEx)
        {
            Console.Error.WriteLine($"Logout warning: {logoutEx.Message}");
        }
    }

    // Close or abort the WCF channel cleanly
    if (client.State == CommunicationState.Faulted)
        client.Abort();
    else
        await client.CloseAsync();
}
