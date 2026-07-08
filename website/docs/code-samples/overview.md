---
title: Code Samples Overview
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created Code Samples overview page - Greg Kolinski | 2026-07-08: Add language quick-starts section; update sample project table and titles; add GitHub samples link - Greg Kolinski */}

# Code Samples

This section has two types of content:

- **Language quick-starts** (C#, JavaScript, Python, Java) — self-contained copy-paste snippets covering authentication, mailboxes, interchanges, callbacks, and error handling. Start here if you want to make your first API call in your language of choice.
- **Sample projects** — full .NET 10 projects under `/samples` that demonstrate complete integration patterns (console polling loop, web application, background service, Minimal API proxy, and SOAP).

> Real, runnable sample projects for all supported languages will be published at [github.com/LorenData/ecgrid-samples](https://github.com/LorenData/ecgrid-samples). That repository is being built out — check back for updates.

## Common Conventions (.NET samples)

All .NET sample projects share the same foundational conventions:

- **Framework:** .NET 10 (`net10.0`)
- **JSON:** `System.Text.Json` — Newtonsoft.Json is never used
- **HTTP:** `IHttpClientFactory` for all REST samples — `new HttpClient()` is never used directly in production-pattern code
- **Async:** `async`/`await` throughout — no `.Result` or `.Wait()`
- **Configuration:** API keys loaded from `IConfiguration` (user-secrets or environment variables) — never hardcoded in source

## Sample Projects

| Project | Pattern | Demonstrates |
|---|---|---|
| REST Console | Console (.NET 10) | Basic REST: inbox check, download, confirm, upload |
| Web Application | ASP.NET Core MVC | MVC controller backed by ECGrid REST |
| Minimal API | ASP.NET Core | Lightweight proxy for common ECGrid endpoints |
| Background Service | Worker Service | Background polling loop with configurable interval |
| SOAP — HttpClient | Console (.NET 10) | Manual SOAP envelope construction via HttpClient |
| SOAP — SvcUtil | Console (.NET 10) | Type-safe SOAP via dotnet-svcutil proxy |

## Prerequisites (.NET samples)

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0)
- An active ECGrid API key (from your network administrator or portal)
- **SOAP samples only:** `dotnet-svcutil` global tool

  ```bash
  dotnet tool install -g dotnet-svcutil
  ```

## Setting Your API Key (.NET samples)

```bash
# Run from within the sample project directory
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
```

Or via environment variable:

```bash
# Windows (PowerShell)
$env:ECGRID__APIKEY = "your-key-here"

# Linux / macOS
export ECGRID__APIKEY=your-key-here
```

The double underscore (`__`) maps to `ECGrid:ApiKey` in `appsettings.json`.

## REST vs SOAP

For new integrations use the REST samples. SOAP samples are for teams maintaining or migrating existing SOAP-based code.

See [REST vs SOAP](../getting-started/rest-vs-soap.md) for a comparison.
