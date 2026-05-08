<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial README created for ECGrid Developer Documentation Portal repo - Greg Kolinski -->

# ECGrid Developer Documentation Portal

![Build Status](https://github.com/LorenData/ecgrid-developer-documention/actions/workflows/deploy.yml/badge.svg)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-brightgreen)

Unified public documentation site for the **ECGrid REST API (v2.6, active)** and **ECGridOS SOAP API (v4.1, legacy)**, built with [Docusaurus 3](https://docusaurus.io/). Also includes six .NET 10 sample projects covering REST and SOAP integration patterns.

- **Live site:** https://developersdev.ecgrid.com
- **Live Swagger UI:** https://rest.ecgrid.io/swagger/index.html

---

## Getting Started

Run the documentation site locally:

```bash
cd website
npm install
npm run start
```

The dev server starts at `http://localhost:3000` with hot reload enabled.

---

## Build

Generate a production build:

```bash
cd website
npm run build
```

Output is written to `website/build/`. GitHub Actions deploys this directory to the `gh-pages` branch on every push to `main`.

---

## Repository Structure

```
├── website/          # Docusaurus 3 site
│   ├── docs/         # ~255 markdown files
│   ├── src/          # Custom CSS and React components
│   └── static/       # Images and static assets
└── samples/          # .NET 10 sample projects
    ├── rest/         # 4 REST API samples
    └── soap/         # 2 SOAP API samples
```

---

## Samples

Six ready-to-run .NET 10 projects under `/samples`:

| Project | API | Pattern |
|---|---|---|
| `rest/ECGrid-REST-dotnet10-Console` | REST | Console app — HttpClient + IHttpClientFactory |
| `rest/ECGrid-REST-dotnet10-AspNetCore-MVC` | REST | ASP.NET Core MVC web app |
| `rest/ECGrid-REST-dotnet10-WorkerService` | REST | Background Worker Service |
| `rest/ECGrid-REST-dotnet10-MinimalAPI` | REST | ASP.NET Core Minimal API |
| `soap/ECGrid-SOAP-dotnet10-Console-HttpClient` | SOAP | Console app — raw HttpClient |
| `soap/ECGrid-SOAP-dotnet10-Console-SvcUtil` | SOAP | Console app — dotnet-svcutil generated proxy |

All samples load API keys from environment variables or `IConfiguration` — no credentials are hardcoded.

---

## Contributing

1. Fork the repository and create a feature branch off `main`.
2. For doc changes, edit or add Markdown files under `website/docs/`.
3. For sample changes, follow the coding conventions in `CLAUDE.md`.
4. Verify the site builds cleanly (`npm run build`) before opening a pull request.
5. Pull requests targeting `main` trigger an automated build check via GitHub Actions.

Loren Data AI Use Policy §7.2: commits and merges to any branch are a human responsibility — do not configure automated tools to push or merge on your behalf.

---

## License

Proprietary — Copyright &copy; Loren Data Corp. All rights reserved.

This repository and its contents are not licensed for public redistribution or reuse without written permission from Loren Data Corp.
