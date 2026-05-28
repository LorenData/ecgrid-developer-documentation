<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial README created for ECGrid Developer Documentation Portal repo - Greg Kolinski | 2026-05-28: Expanded to full developer onboarding guide — repo setup, dual-remote git, local dev, Claude Code workflow - Greg Kolinski -->

# ECGrid Developer Documentation Portal

![Build Status](https://github.com/LorenData/ecgrid-developer-documentation/actions/workflows/deploy.yml/badge.svg)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-brightgreen)

Unified public documentation for the ECGrid B2B EDI platform — covering the **ECGrid REST API (v2.6, active)** and the **ECGridOS SOAP API (v4.1, established)**, as well as the **Transformation API** and the **Data Sync and Catalog API**.

ECGrid is the connectivity, transformation, and content delivery backbone that builders, integrators, and platforms rely on to connect, transact, and scale — 400,000+ trading relationships, 300+ public and private networks, and 25+ years in production. This portal covers the full programmable API surface so your team can provision, transform, deliver, and monitor across a single integration.

| API | Coverage |
|---|---|
| **REST API v2.6** | Networks, Mailboxes, IDs, Partners, Parcels, Interchanges, Callbacks, Carbon Copies, Certificates, Comms, Users, Keys, Reports, Portals |
| **ECGridOS SOAP API v4.1** | Same core resources as REST via the established SOAP interface |
| **Transformation API** | EDI mapping, translation, and simplification |
| **Data Sync and Catalog API** | Product data delivery and catalog management |

.NET 10 code samples for REST and SOAP integration patterns are included.

- **Live site:** https://api.ecgridos.io

## Live API References

| API | Link |
|---|---|
| REST API Swagger UI | https://rest.ecgrid.io/swagger/index.html |
| SOAP Web Service | https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx |
| Transformation API Swagger UI | https://simplify.ecgrid.com/swagger/index.html |
| Data Sync and Catalog API Swagger UI | https://globalproductaccess.com/swagger/index.html |

---

## Developer Onboarding

This section covers everything a new developer needs to get set up and contributing. Read it top to bottom before touching any files.

### Prerequisites

Install these before cloning:

| Tool | Version | Purpose |
|---|---|---|
| [Git](https://git-scm.com/) | Any recent | Source control |
| [Node.js](https://nodejs.org/) | **20.x LTS** | Docusaurus site build |
| [npm](https://www.npmjs.com/) | Included with Node | Package management |
| [.NET SDK](https://dotnet.microsoft.com/download) | **10.0** | C# code samples |
| [Claude Code](https://claude.ai/code) | Latest | AI-assisted development (see below) |

Verify your versions:

```bash
node --version    # should be v20.x.x
npm --version
dotnet --version  # should be 10.x.x
git --version
```

---

### Cloning the Repository

The authoritative source repository is hosted in **Azure DevOps**. Clone from there:

```bash
git clone "https://lorendata-dev.visualstudio.com/ECGrid%20Developer%20Documentation%20Portal/_git/ECGrid%20Developer%20Documentation%20Portal" ecgrid-developer-portal
cd ecgrid-developer-portal
```

You will need to authenticate with your Loren Data Azure DevOps credentials. If you get a credentials prompt, use your `@ld.com` account.

---

### Understanding the Dual-Remote Git Setup

This repo uses a **dual push** configuration. When you run `git push`, Git sends your commits to **two remotes simultaneously**:

1. **Azure DevOps** — the primary source of truth (fetch + push)
2. **GitHub** — push-only target that triggers the live site deployment

You can verify this with:

```bash
git remote -v
```

Expected output:
```
origin  https://lorendata-dev.visualstudio.com/ECGrid%20Developer%20Documentation%20Portal/_git/ECGrid%20Developer%20Documentation%20Portal (fetch)
origin  https://lorendata-dev.visualstudio.com/ECGrid%20Developer%20Documentation%20Portal/_git/ECGrid%20Developer%20Documentation%20Portal (push)
origin  https://github.com/LorenData/ecgrid-developer-documentation.git (push)
```

**Why two remotes?** The Docusaurus site is deployed to GitHub Pages. GitHub Actions watches the `main` branch on GitHub and automatically builds and publishes the site to the `gh-pages` branch whenever `main` is updated. The Azure DevOps push keeps the canonical repo in sync.

If you cloned fresh and only see one push remote, ask Greg to send you the setup command. Do not attempt to add remotes without confirming the URLs.

---

### Pulling the Latest Changes

```bash
git pull origin main
```

This fetches and merges from Azure DevOps (the `fetch` remote). Always pull before starting new work.

---

### Pushing Changes

```bash
git push origin main
```

This pushes to **both** Azure DevOps and GitHub in one command. The GitHub push immediately triggers the CI/CD deploy pipeline. Only push when your changes are complete and the site builds locally without errors.

> **Important:** Per Loren Data AI Use Policy §7.2, **do not commit or push directly from an AI session**. Review all AI-generated changes yourself, then commit and push manually.

---

### Local Development

Install dependencies (run once after cloning, and again after pulling if `package-lock.json` changed):

```bash
cd website
npm install
```

Start the local preview server:

```bash
npm run start
```

The site opens at `http://localhost:3000`. Changes to Markdown files hot-reload automatically. Press `Ctrl+C` to stop.

Verify a production build before pushing (catches config errors that the dev server misses):

```bash
npm run build
```

---

### How Deployment Works

```
You push to main
       │
       ├─► Azure DevOps (source of truth, team access)
       │
       └─► GitHub (LorenData/ecgrid-developer-documentation)
                │
                └─► GitHub Actions (.github/workflows/deploy.yml)
                           │
                           └─► Builds Docusaurus → publishes to gh-pages branch
                                      │
                                      └─► Live site at https://api.ecgridos.io
```

The deploy pipeline runs automatically. You do not manually upload or publish anything. Monitor the build badge at the top of this README or check the Actions tab on GitHub.

---

### Working with Claude Code (AI-Assisted Development)

This project uses [Claude Code](https://claude.ai/code) for AI-assisted documentation generation. The `CLAUDE.md` file at the repo root is the instruction file that Claude Code reads at the start of every session.

**What CLAUDE.md contains:**
- All page templates (REST endpoint, SOAP method, Common Operations)
- Site navigation structure and sidebar positions
- Coding conventions for C# samples
- AI attribution requirements (Loren Data AI Use Policy §8.1–§8.2)
- Live API source URLs that Claude always fetches fresh
- What to avoid (deprecated patterns, hardcoded credentials, etc.)

**How to use Claude Code on this project:**

1. Open a terminal in the repo root
2. Run `claude` to start a session — it automatically reads `CLAUDE.md`
3. Ask Claude to generate, update, or review documentation
4. **Always review the output before committing** — Claude is a tool, not an approver

**Attribution:** Every file that Claude materially modifies gets an AI Attribution comment block at the top (format is in CLAUDE.md). This is required by Loren Data AI Use Policy §8.2. Do not remove or skip these.

---

### Repo Structure

```
ecgrid-developer-portal/
├── CLAUDE.md                          ← Claude Code instructions (read this before using Claude)
├── README.md                          ← This file
├── .github/
│   └── workflows/
│       └── deploy.yml                 ← GitHub Actions — builds and deploys site on push to main
├── website/                           ← Docusaurus 3 site root
│   ├── docs/                          ← All Markdown content (~244 files)
│   │   ├── intro.md
│   │   ├── getting-started/
│   │   ├── guides/
│   │   ├── rest-api/
│   │   ├── soap-api/
│   │   ├── common-operations/
│   │   ├── appendix/
│   │   ├── code-samples/
│   │   └── changelog/
│   ├── static/                        ← Images and static assets
│   ├── src/css/custom.css             ← Brand color overrides
│   ├── docusaurus.config.ts           ← Site config (TypeScript)
│   └── sidebars.ts                    ← Sidebar structure (TypeScript)
└── samples/                           ← .NET 10 C# code samples
    ├── README.md
    ├── rest/
    │   ├── ECGrid-REST-dotnet10-Console/
    │   ├── ECGrid-REST-dotnet10-AspNetCore-MVC/
    │   ├── ECGrid-REST-dotnet10-WorkerService/
    │   └── ECGrid-REST-dotnet10-MinimalAPI/
    └── soap/
        ├── ECGrid-SOAP-dotnet10-Console-HttpClient/
        └── ECGrid-SOAP-dotnet10-Console-SvcUtil/
```

---

### Common Tasks

**Add a new documentation page:**
1. Create the `.md` file in the correct `docs/` subfolder (follow the nav structure in `CLAUDE.md`)
2. Add a `_category_.json` in the folder if it doesn't exist
3. Run `npm run start` and verify it appears in the sidebar
4. Run `npm run build` to confirm no build errors
5. Commit and push

**Update an existing page:**
1. Edit the `.md` file directly
2. Preview with `npm run start`
3. Commit and push

**Add or update a C# sample:**
1. Work inside the relevant project under `samples/`
2. Follow the coding conventions in `CLAUDE.md` — no hardcoded keys, use `IHttpClientFactory`, `System.Text.Json` only
3. The samples are referenced from the docs but are not automatically published — just keep them in the repo

---

### Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Active development — all changes go here |
| `gh-pages` | Auto-generated by GitHub Actions — **never edit manually** |

There are no feature branches at this time. All work happens on `main`. If that changes, this section will be updated.

---

### Getting Help

- **Site not building?** Run `npm run build` locally first and read the error output — it usually identifies the exact file and line.
- **Push rejected?** Make sure you pulled first (`git pull origin main`), then push again.
- **Claude generating wrong output?** Check that `CLAUDE.md` is up to date and that you're running Claude Code from the repo root.
- **Questions about the API?** Start at the live Swagger UI links in the Live API References section above.
- **Azure DevOps access issues?** Contact Greg Kolinski (gkolinski@ld.com).

---

## License

Proprietary — Copyright &copy; Loren Data Corp. All rights reserved.

This repository and its contents are not licensed for public redistribution or reuse without written permission from Loren Data Corp.
