// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: Worker Service host setup for ECGrid REST API polling sample - Greg Kolinski
// ------------------------------------------------------------

using ECGrid_REST_dotnet10_WorkerService;

var builder = Host.CreateApplicationBuilder(args);

// ---------------------------------------------------------------------------
// Named HttpClient "ecgrid" — base address and auth header are set once here
// so the worker never constructs an HttpClient directly
// ---------------------------------------------------------------------------
var apiKey  = builder.Configuration["ECGrid:ApiKey"]  ?? throw new InvalidOperationException("ECGrid:ApiKey is not configured.");
var baseUrl = builder.Configuration["ECGrid:BaseUrl"] ?? "https://rest.ecgrid.io";

builder.Services.AddHttpClient("ecgrid", client =>
{
    client.BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/");
    // X-API-Key is the authentication header for all ECGrid REST calls
    client.DefaultRequestHeaders.Add("X-API-Key", apiKey);
    client.DefaultRequestHeaders.Add("Accept", "application/json");
});

// ---------------------------------------------------------------------------
// Register the background worker — IHostedService keeps it running for the
// lifetime of the process
// ---------------------------------------------------------------------------
builder.Services.AddHostedService<EcGridPollingWorker>();

var host = builder.Build();
await host.RunAsync();
