<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Root samples README covering all 6 .NET 10 projects - Greg Kolinski -->

# ECGrid API — .NET 10 Sample Projects

This directory contains six ready-to-run .NET 10 sample projects covering the
**ECGrid REST API (v2.6)** and **ECGridOS SOAP API (v4.1)**. Each project is
self-contained and demonstrates a different hosting model or integration technique.

---

## Sample Projects

| Project | Type | API | Demonstrates |
|---|---|---|---|
| [`rest/ECGrid-REST-dotnet10-Console`](rest/ECGrid-REST-dotnet10-Console/) | Console App | REST | Minimal single-file console polling loop; `IHttpClientFactory`; upload and download workflow |
| [`rest/ECGrid-REST-dotnet10-AspNetCore-MVC`](rest/ECGrid-REST-dotnet10-AspNetCore-MVC/) | ASP.NET Core MVC | REST | Controller-based web app; dependency injection; typed service wrappers |
| [`rest/ECGrid-REST-dotnet10-MinimalAPI`](rest/ECGrid-REST-dotnet10-MinimalAPI/) | ASP.NET Core Minimal API | REST | Thin proxy routes; multipart upload forwarding; named `HttpClient` |
| [`rest/ECGrid-REST-dotnet10-WorkerService`](rest/ECGrid-REST-dotnet10-WorkerService/) | Worker Service | REST | Background-service inbox polling; `IHostedService`; graceful shutdown |
| [`soap/ECGrid-SOAP-dotnet10-Console-HttpClient`](soap/ECGrid-SOAP-dotnet10-Console-HttpClient/) | Console App | SOAP | Manual SOAP envelope construction; `XDocument` parsing; no generated proxy |
| [`soap/ECGrid-SOAP-dotnet10-Console-SvcUtil`](soap/ECGrid-SOAP-dotnet10-Console-SvcUtil/) | Console App | SOAP | `dotnet-svcutil` generated typed proxy; `BasicHttpsBinding`; WCF client pattern |

---

## Common Prerequisites

All projects share these requirements:

| Requirement | Version / Notes |
|---|---|
| .NET SDK | 10.0 or later — [download](https://dotnet.microsoft.com/download) |
| ECGrid account | Contact [Loren Data](https://www.lorendata.com) to obtain credentials |
| REST API key | Required for all `rest/` projects — generate in the ECGrid portal |
| SOAP credentials | Username + password — required for all `soap/` projects |

---

## Setting Credentials

### REST Projects

Each REST project reads its API key from `appsettings.json` or an environment variable.

**Option A — `appsettings.json`** (local development only; do not commit real keys):

```json
{
  "ECGrid": {
    "ApiKey": "your-api-key-here",
    "BaseUrl": "https://rest.ecgrid.io"
  }
}
```

**Option B — Environment variable** (CI/CD, containers, production):

```bash
# Linux / macOS / WSL
export ECGrid__ApiKey="your-api-key-here"

# Windows PowerShell
$env:ECGrid__ApiKey = "your-api-key-here"
```

### SOAP Projects

Each SOAP project reads a username and password from `appsettings.json` or environment variables.

**Option A — `appsettings.json`**:

```json
{
  "ECGrid": {
    "UserName": "your-username",
    "Password": "your-password"
  }
}
```

**Option B — Environment variable**:

```bash
export ECGrid__UserName="your-username"
export ECGrid__Password="your-password"
```

> **Security note:** Never commit real API keys or passwords to source control.
> Use a secrets manager (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault)
> or the [.NET Secret Manager](https://learn.microsoft.com/aspnet/core/security/app-secrets)
> for local development.

---

## Running a Sample

```bash
# Navigate to the project you want to run
cd rest/ECGrid-REST-dotnet10-Console

# Restore NuGet packages and run
dotnet run
```

All projects target `net10.0`. No additional SDK components are needed beyond the
standard .NET 10 SDK.

---

## Key Design Patterns Used

All samples follow these conventions from the Loren Data coding standards:

- `IHttpClientFactory` — never `new HttpClient()` in production code paths
- `System.Text.Json` — never Newtonsoft.Json
- `async`/`await` throughout — no `.Result` or `.Wait()`
- Configuration via `IConfiguration` — credentials always come from settings, never from source
- Top-level statements in Console projects to keep entry points concise
- XML doc comments (`/// <summary>`) on all public methods in non-entry-point files

---

## Project Index by Use Case

| I want to... | Use this project |
|---|---|
| See the simplest possible REST integration | `rest/ECGrid-REST-dotnet10-Console` |
| Build a web UI over ECGrid REST | `rest/ECGrid-REST-dotnet10-AspNetCore-MVC` |
| Proxy ECGrid REST behind my own API | `rest/ECGrid-REST-dotnet10-MinimalAPI` |
| Poll ECGrid on a schedule in the background | `rest/ECGrid-REST-dotnet10-WorkerService` |
| Call SOAP with no generated code | `soap/ECGrid-SOAP-dotnet10-Console-HttpClient` |
| Call SOAP with full type safety | `soap/ECGrid-SOAP-dotnet10-Console-SvcUtil` |

---

## Documentation Links

- [ECGrid Developer Portal](https://developers.ecgrid.com)
- [REST API Overview](../website/docs/rest-api/overview.md)
- [SOAP API Overview](../website/docs/soap-api/overview.md)
- [Authentication & API Keys](../website/docs/getting-started/authentication-api-keys.md)
- [REST vs SOAP Guide](../website/docs/guides/rest-vs-soap.md)
- [Connecting via SOAP](../website/docs/guides/connecting-via-soap.md)
- [Code Samples — Overview](../website/docs/code-samples/overview.md)

---

## Feedback

Open an issue or pull request on the
[LorenData/ECGrid-API repository](https://github.com/LorenData/ECGrid-API)
or contact [developer-support@lorendata.com](mailto:developer-support@lorendata.com).
