---
title: Code Samples Overview
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created Code Samples overview page - Greg Kolinski */}

# Code Samples Overview

The ECGrid Developer Portal includes six .NET 10 sample projects under the `/samples` directory. Each project demonstrates a different integration pattern for the ECGrid REST or SOAP APIs.

## Common Conventions

All sample projects share the same foundational conventions:

- **Framework:** .NET 10 (`net10.0`)
- **JSON:** `System.Text.Json` — Newtonsoft.Json is never used
- **HTTP:** `IHttpClientFactory` for all REST samples — `new HttpClient()` is never used directly in production-pattern code
- **Async:** `async`/`await` throughout — no `.Result` or `.Wait()`
- **Configuration:** API keys loaded from `IConfiguration` (user-secrets or environment variables) — never hardcoded in source

## Sample Projects

| Project | Type | Demonstrates |
|---|---|---|
| `ECGrid-REST-dotnet10-Console` | Console (.NET 10) | Basic REST: login, inbox, download, confirm, upload |
| `ECGrid-REST-dotnet10-AspNetCore-MVC` | ASP.NET Core MVC | Full MVC controller with ECGrid REST backend |
| `ECGrid-REST-dotnet10-WorkerService` | Worker Service | Background polling loop with configurable interval |
| `ECGrid-REST-dotnet10-MinimalAPI` | Minimal API | Lightweight proxy for key ECGrid endpoints |
| `ECGrid-SOAP-dotnet10-Console-HttpClient` | Console (.NET 10) | Manual SOAP via HttpClient + XDocument |
| `ECGrid-SOAP-dotnet10-Console-SvcUtil` | Console (.NET 10) | Type-safe SOAP via dotnet-svcutil proxy |

## Prerequisites

Before running any sample, ensure the following are in place:

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) installed
- An active ECGrid API key (obtain from your ECGrid Network Administrator or the ECGrid portal)
- **SOAP samples only:** `dotnet-svcutil` global tool for regenerating the service proxy

  ```bash
  dotnet tool install -g dotnet-svcutil
  ```

## Setting Your API Key

All REST samples read the API key from configuration. The recommended approach during local development is .NET user-secrets:

```bash
# Run this once from within the sample project directory
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
```

Alternatively, set the environment variable directly:

```bash
# Windows (Command Prompt)
set ECGRID__APIKEY=your-key-here

# Windows (PowerShell)
$env:ECGRID__APIKEY = "your-key-here"

# Linux / macOS
export ECGRID__APIKEY=your-key-here
```

The double underscore (`__`) in the environment variable name is the .NET configuration hierarchy separator — it maps to `ECGrid:ApiKey` in `appsettings.json`.

## REST vs SOAP

If you are starting a new integration, use the REST samples. The SOAP samples are provided for teams maintaining or migrating existing SOAP-based integrations.

See [REST vs SOAP](../guides/rest-vs-soap.md) for a full comparison.
