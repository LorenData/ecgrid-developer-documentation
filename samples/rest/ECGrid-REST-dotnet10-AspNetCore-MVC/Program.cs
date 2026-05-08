// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: ASP.NET Core MVC startup for ECGrid REST API sample - Greg Kolinski
// ------------------------------------------------------------

using ECGrid_REST_dotnet10_AspNetCore_MVC.Services;

var builder = WebApplication.CreateBuilder(args);

// ---------------------------------------------------------------------------
// MVC — add controllers and Razor views
// ---------------------------------------------------------------------------
builder.Services.AddControllersWithViews();

// ---------------------------------------------------------------------------
// Named HttpClient "ecgrid" — base address and auth header configured once;
// IHttpClientFactory injects a correctly scoped instance wherever needed
// ---------------------------------------------------------------------------
var apiKey  = builder.Configuration["ECGrid:ApiKey"]  ?? throw new InvalidOperationException("ECGrid:ApiKey is not configured.");
var baseUrl = builder.Configuration["ECGrid:BaseUrl"] ?? "https://rest.ecgrid.io";

builder.Services.AddHttpClient("ecgrid", client =>
{
    client.BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/");
    // X-API-Key authenticates every REST call
    client.DefaultRequestHeaders.Add("X-API-Key", apiKey);
    client.DefaultRequestHeaders.Add("Accept", "application/json");
});

// ---------------------------------------------------------------------------
// Application services — scoped lifetime matches the HTTP request lifetime
// ---------------------------------------------------------------------------
builder.Services.AddScoped<IEcGridService, EcGridService>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

// Standard MVC route — ECGrid controller is the default landing page
app.MapControllerRoute(
    name:    "default",
    pattern: "{controller=ECGrid}/{action=Inbox}/{id?}");

app.Run();
