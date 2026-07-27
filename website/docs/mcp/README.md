# ECGrid MCP Server

**You create the experience. We power the connections.**

ECGrid is programmable B2B infrastructure for builders — ISVs, platforms, system integrators, and enterprise IT teams. The ECGrid MCP Server brings ECGrid's full B2B connectivity layer directly into AI agents, AI assistants, and AI-powered applications via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).

Connect your AI to ECGrid and it can do what you do today — look up trading partners, check transaction status, manage mailboxes, monitor your network — through natural language or automated agent workflows, using your existing API key.

> **This document is self-contained.** Everything you need to connect, verify, and build is here. If you get stuck at any step, you can paste this entire document into Claude or any AI assistant and ask it to walk you through the process for your specific environment.
>
> Full documentation is also available at the [ECGrid Developer Portal](https://api.ecgridos.io/).

---

## Who This Is For

### ECGrid Customers — Supercharge Your AI Assistant with B2B Capabilities

You're already on ECGrid. Now connect your AI assistant directly to your account. Instead of logging into the portal to look something up, just ask your AI — and get an answer instantly.

- Ask Claude (or any MCP-compatible AI tool) about your trading partners, transaction history, mailboxes, and network status in plain language
- Let your AI handle routine ECGrid lookups so your team doesn't have to
- Replace repetitive portal navigation with a conversation
- A subset of tools render an **interactive UI component** directly in your AI client — a visual, browsable view of your ECGrid data alongside the AI's response, with no extra setup required

You need your ECGrid API key and about 5 minutes. No coding required.

> **Just getting started?** See the [Quick Start](#quick-start) section below.

---

### Developers — Add ECGrid B2B Capabilities to Any AI

You're building something — a portal, a chatbot, an AI agent, an automation workflow. The ECGrid MCP Server lets you wire full B2B connectivity into whatever you're building without writing a custom integration for every ECGrid operation.

- **Build an AI assistant for your ECGrid portal** — give your users a natural language interface to their ECGrid data right inside your application
- **Add B2B capabilities to an existing AI agent** — if you already have an AI agent or chatbot, connecting it to the ECGrid MCP Server adds EDI, AS2, and MFT capabilities as native tools — no bespoke API code per feature
- **Automate B2B workflows with AI** — build agents that monitor, react to, and act on ECGrid events as part of a larger automated pipeline
- **Extend your company's existing AI** — if your organization already runs an internal AI assistant or copilot, ECGrid MCP lets you add B2B connectivity as a capability layer without rebuilding anything
- **All tools return structured JSON data** for programmatic consumption in your application — a subset of tools additionally render an **interactive UI component** in compatible AI clients (Claude Desktop, Claude.ai); both modes use the same tool call and return the same data

Each new tool your integration picks up automatically via `tools/list` — no redeployment needed on your end.

> **Building an agent?** See the companion [ECGrid MCP Agent Guide](ECGrid-MCP-Agent-Guide.md) for a complete walkthrough with code examples.

---

## What Is MCP?

The Model Context Protocol (MCP) is an open standard that lets AI tools connect to external services as native capabilities. Once the ECGrid MCP Server is connected, your AI can call ECGrid operations directly — no custom integration code required per tool.

- **AI desktop users**: add one config block, restart your app — ECGrid tools are available immediately
- **Developers**: call the MCP server over HTTP from your application or agent

---

## Quick Start

**You have an API key. Here's all you need:**

**1. Get your API key** from the [ECGrid Developer Portal](https://api.ecgridos.io/) → account settings.

**2. Add this block to your `claude_desktop_config.json`** and replace `YOUR_API_KEY_HERE`:

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.ecgrid.io/mcp",
        "--header",
        "X-APIKey:YOUR_API_KEY_HERE",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

Config file location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**3. Restart Claude Desktop.**

**4. Test it** — type this prompt: `Test the ECGrid MCP connection`

That's it. Need more detail? Read on.

---

## Let Claude Install It For You

**The fastest way to connect — paste one prompt and let Claude do the rest.**

There are two versions of the install prompt below depending on where you are running Claude. Both accomplish the same thing — the difference is how much Claude can do automatically versus guide you through.

---

### Option A — Claude Desktop (Fully Automated)

> **Use this if you are already inside Claude Desktop.** Claude Desktop has computer use capabilities — it can open a terminal, check for Node.js, ask your permission to install it if missing, locate and edit your config file, and verify the connection, all without you touching the command line.

Copy the prompt below and paste it into your Claude Desktop conversation:

```
I want to connect the ECGrid MCP server to Claude Desktop. Please set it up for me by doing the following — ask my permission before taking any action that changes my system:

1. Ask me for my ECGrid API key (I can get it from https://api.ecgridos.io/ → account settings if I don't have it handy)
2. Open a terminal and run `node --version` to check if Node.js is installed
   - If Node.js v18 or higher is installed: confirm it and continue
   - If Node.js is missing or below v18: tell me what you found, ask my permission, then download and run the LTS installer from https://nodejs.org — wait for me to confirm before proceeding
3. Locate my claude_desktop_config.json file:
   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
   - Windows: %APPDATA%\Claude\claude_desktop_config.json
4. Read the file if it exists — check whether it already has an "mcpServers" section or other content
5. Add the ECGrid MCP block in the correct location, safely merging with any existing content — do not duplicate keys or add a second "mcpServers" section
6. Fill in my API key in the X-APIKey line — no spaces around the colon
7. Show me the final file contents before saving and ask my permission to save
8. After I confirm, save the file and ask me to fully restart Claude Desktop
9. After I restart, test the connection by running: Test the ECGrid MCP connection

The ECGrid MCP server URL is https://mcp.ecgrid.io/mcp. Authentication uses the X-APIKey header. The config block to add is:

{
  "ecgrid-mcp": {
    "command": "npx",
    "args": [
      "-y",
      "mcp-remote",
      "https://mcp.ecgrid.io/mcp",
      "--header",
      "X-APIKey:PLACEHOLDER",
      "--transport",
      "http-only"
    ]
  }
}

This block goes inside the "mcpServers" section of the config file, which itself lives inside the outer { } of the file.
```

> Claude will ask your permission before installing Node.js, before saving the config file, and before any other action that changes your system. You stay in control at every step.

---

### Option B — Claude.ai Web, Mobile, or Any Other Claude (Step-by-Step Guidance)

> **Use this if you are on claude.ai, the Claude mobile app, or any Claude conversation outside Claude Desktop.** Claude will guide you through each step conversationally, telling you exactly what to run and what to paste.

Copy the prompt below and paste it into any Claude conversation:

```
I want to connect the ECGrid MCP server to Claude Desktop so I can interact with my ECGrid account using AI. Please guide me through the setup step by step:

1. Ask me for my ECGrid API key (I can get it from https://api.ecgridos.io/ → account settings)
2. Ask what OS I'm on (macOS or Windows)
3. Tell me how to open a terminal and run `node --version` — then ask me what I see so you can tell me whether Node.js is installed, too old, or missing. If it's missing or too old, give me the exact steps to install the LTS version from https://nodejs.org
4. Tell me exactly where to find my claude_desktop_config.json file and how to open it:
   - If I'm on macOS: warn me that the Library folder is hidden by default, and give me all three methods to reach it (Go to Folder, Terminal open command, and Cmd+Shift+. toggle)
   - If I'm on Windows: remind me that AppData is also hidden if browsing manually, and that the easiest fix is to paste %APPDATA%\Claude\ directly into the File Explorer address bar
   - For either OS: mention they can also open it directly from Claude Desktop via Settings → Developer → Edit Config
5. Ask me to paste the current contents of the file so you can see what's already there
6. Give me the exact final file contents to paste in — with my API key filled in, correctly merged with anything already in my file
7. Tell me how to save the file and fully restart Claude Desktop
8. Give me a test prompt to run after I restart to confirm the connection is working

The ECGrid MCP server URL is https://mcp.ecgrid.io/mcp and it uses an X-APIKey header. The mcpServers block must be placed inside the outer { } of the config file — not appended after it.
```

---

### Option C — Paste This Entire Document into Claude

If you want Claude to have the full context — all troubleshooting, auth levels, tool reference, and developer docs — paste this entire README into any Claude conversation and say:

```
Please install the ECGrid MCP server on my Claude Desktop using the instructions in this document.
```

Claude will read the full document and guide you through setup with access to every detail needed to handle edge cases and troubleshoot on the spot.

---

### What Claude Will Do

Regardless of which option you use, Claude will:

- Ask for your ECGrid API key — used only to build the config, never stored or transmitted by Claude
- Check whether Node.js is installed and at the right version — and help you install it if not (with your permission in Option A)
- Locate your config file and check what's already in it — handling hidden folder navigation on both macOS and Windows
- Generate the correct merged config with your key filled in
- Save the file (Option A, with permission) or show you exactly what to paste (Options B and C)
- Confirm the connection is working with a test prompt after restart

---

## What You Need

| Requirement | Who Needs It | Details |
|---|---|---|
| ECGrid API Key | Everyone | From your ECGrid account — see below |
| Node.js v18 or later | Claude Desktop users only | See note below — not needed for developers or other MCP tools |
| npx | Claude Desktop users only | Included automatically with Node.js — no separate install |
| HTTP client | Developers only | Any language or framework that can make HTTP POST requests |

### A Note on Node.js

**Node.js is not required by ECGrid.** It is required by Claude Desktop.

Here's the simple version: Claude Desktop currently can't talk directly to remote servers like the ECGrid MCP Server on its own — it needs a small local helper program to make that connection. Node.js provides that helper. That's the only reason you're installing it.

This is a Claude Desktop limitation, not something ECGrid requires. Anthropic is working on native remote server support, and when that ships, Node.js won't be needed at all. For now it's a quick one-time install that takes about two minutes, runs quietly in the background when needed, and has no noticeable effect on your computer.

**What this means in practice:**

- **Claude Desktop users** — install Node.js once, and you're done. You are not installing it for ECGrid; you are installing it because Claude Desktop needs it to bridge the gap to any remote MCP server. Once Claude Desktop adds this natively, this step goes away entirely.
- **Developers building agents or chatbots** — Node.js is not required. You call `https://mcp.ecgrid.io/mcp` directly over HTTP from your application. No bridge, no local process, no Node.js dependency in your project.
- **Cursor, Windsurf, and other MCP tools** — check your tool's documentation. Many already support remote MCP servers natively and do not require Node.js.

If you already have Node.js installed, nothing changes — move on to the next step.

---

## Step 1 — Get Your ECGrid API Key

Your ECGrid API Key is the same key used to access the ECGrid OS API. No new account or separate credential is needed.

1. Go to the [ECGrid Developer Portal](https://api.ecgridos.io/)
2. Log in with your ECGrid account
3. Navigate to your account settings
4. Copy your API Key

> **Keep your API key private.** Do not share it, commit it to source control, or include it in client-side code. Treat it like a password. Each key is scoped to your account, network, and permission level.

---

## Step 2 — Check and Install Node.js (Claude Desktop Users Only)

> **Skip this step if you are a developer calling the MCP server directly from your application.** Node.js is not needed for HTTP-based integrations.
>
> **Not a developer?** This is a one-time install. It takes about two minutes, runs quietly when needed, and has no noticeable effect on your computer. You will not need to think about it again after this step.

### Check if Node.js is already installed

You need to open a terminal — a plain text window where you type commands. It looks more intimidating than it is. You only need to type one thing.

---

> #### Opening a terminal on macOS
>
> **Method 1 — Spotlight (easiest):**
> 1. Press `Cmd + Space` on your keyboard — a search bar appears in the middle of your screen
> 2. Type `Terminal` and press Enter
> 3. A window opens with a blinking cursor — this is your terminal
>
> **Method 2 — Finder:**
> 1. Open Finder
> 2. Click **Applications** in the sidebar
> 3. Open the **Utilities** folder
> 4. Double-click **Terminal**

---

> #### Opening a terminal on Windows
>
> **Method 1 — Start menu (easiest):**
> 1. Press the **Windows key** on your keyboard (or click the Start button)
> 2. Type `cmd` and press Enter
> 3. A black window opens with a blinking cursor — this is your terminal (called Command Prompt)
>
> **Method 2 — Search bar:**
> 1. Click the search bar on your taskbar (the magnifying glass icon)
> 2. Type `Command Prompt` and click the result
>
> **Method 3 — Run dialog:**
> 1. Press `Windows key + R` at the same time
> 2. Type `cmd` and press Enter

---

Once your terminal is open, type this exactly and press Enter:

```
node --version
```

**What you see tells you what to do:**

| What you see | What it means | What to do |
|---|---|---|
| `v18.0.0` or higher (e.g. `v20.11.0`, `v22.x.x`) | ✅ Node.js is installed and ready | Skip to Step 3 |
| A version lower than `v18` (e.g. `v16.x.x`) | ⚠️ Node.js is installed but too old | Install the LTS version from [nodejs.org](https://nodejs.org) |
| `'node' is not recognized` or `command not found` | ❌ Node.js is not installed | Follow the install steps below |

> **Nothing happened or you see an error?** Make sure you typed `node --version` exactly as shown, with a space before the two dashes, and pressed Enter. If you see a message about not being able to find the command, Node.js is not installed — continue to the install steps below.

### Install Node.js (if needed)

1. Go to [nodejs.org](https://nodejs.org) in your browser
2. Click the green **LTS** button — LTS stands for Long Term Support and is the recommended version for most people
3. The download starts automatically — open the file when it finishes
4. The installer opens — click **Next** or **Continue** through each screen and accept all defaults
5. When it says the installation is complete, click **Finish** or **Close**
6. **Important:** close your terminal window completely and open a new one (the same steps as above)
7. Type `node --version` again and press Enter — you should now see a number like `v20.11.0`

If you see a version number, you're done. Move on to Step 3.

> `npx` is included automatically with Node.js — you do not need to install it separately.

---

## Step 3 — Connect Your AI Tool

### Claude Desktop

**3a. Find your config file**

The Claude Desktop config file is a plain text file called `claude_desktop_config.json`.

> **Easiest method — open it directly from Claude Desktop:**
> 1. Open Claude Desktop
> 2. Click the **hamburger menu** (☰) in the top-left corner
> 3. Go to **Settings** → **Developer**
> 4. Click **Edit Config**
>
> This opens the exact config file Claude Desktop is reading — in your default text editor, at the correct path, no hunting required. This works on both macOS and Windows regardless of where the file is stored.

If you prefer to find the file manually, the locations are:

**Config file location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

---

> #### ⚠️ macOS — The Library Folder Is Hidden
>
> On macOS, the `Library` folder in your home directory is hidden by default. You will not see it if you browse in Finder normally. Use one of these methods to reach it:
>
> **Method 1 — Go to Folder (easiest):**
> 1. Open Finder
> 2. In the menu bar, click **Go** → **Go to Folder** (or press `Cmd + Shift + G`)
> 3. Paste this path exactly and press Enter:
>    ```
>    ~/Library/Application Support/Claude/
>    ```
> 4. The Claude folder will open — you should see `claude_desktop_config.json` if it already exists
>
> **Method 2 — Terminal (always works):**
> Open Terminal and run:
> ```
> open ~/Library/Application\ Support/Claude/
> ```
> This opens the folder in Finder directly.
>
> **Method 3 — Show hidden files permanently:**
> In Finder, press `Cmd + Shift + .` (period) to toggle hidden files on. The `Library` folder will appear in your home directory. Press the same shortcut again to hide them when you're done.

---

> #### ⚠️ Windows — The AppData Folder Is Hidden
>
> On Windows, the `AppData` folder in your user directory is also hidden by default. If you try to browse to `C:\Users\YourName\` in File Explorer, you won't see `AppData`.
>
> **The easiest fix — use the address bar shortcut:**
> 1. Open File Explorer
> 2. Click the address bar at the top
> 3. Paste `%APPDATA%\Claude\` and press Enter
>
> Windows automatically expands `%APPDATA%` to the correct path and opens the Claude folder directly — you never need to see or navigate through `AppData` at all.
>
> **If you want to browse hidden folders manually:**
> In File Explorer, click **View** in the menu bar → check **Hidden items**. The `AppData` folder will appear in your user directory. You can uncheck it when you're done.

---

If the config file does not exist yet in the Claude folder, you will create it in the next step.

---

**3b. Add the ECGrid MCP block**

> **Important — read before editing:** The config file is a JSON file. JSON has strict formatting rules. Every `{` must have a matching `}`, every item except the last must end with a comma, and nothing should be added outside the outermost `{` and `}`. If the formatting is wrong, Claude Desktop will fail to start. When in doubt, paste your finished file into [jsonlint.com](https://jsonlint.com) to check it before saving.

---

**If the file does not exist yet** — create a new file, name it `claude_desktop_config.json`, and paste in the following exactly:

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.ecgrid.io/mcp",
        "--header",
        "X-APIKey:YOUR_API_KEY_HERE",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

---

**If the file already exists and is empty or contains only `{}`** — replace the entire contents with the block above.

---

**If the file already exists and has other content** — you need to add the `"ecgrid-mcp"` block inside the existing file without breaking what's already there.

The config file is a single JSON object — everything lives inside one pair of outer `{` `}` braces. The `"mcpServers"` section is one entry inside that object, and each MCP server is one entry inside `"mcpServers"`.

Here is what a file with existing content might look like, and exactly where to add the ECGrid block:

```json
{
  "preferences": {
    "theme": "dark"
  },
  "mcpServers": {
    "some-other-tool": {
      "command": "npx",
      "args": ["-y", "some-other-package"]
    },
    "ecgrid-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.ecgrid.io/mcp",
        "--header",
        "X-APIKey:YOUR_API_KEY_HERE",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

**The rules when merging:**
- The `"ecgrid-mcp"` block goes **inside** the `"mcpServers": { }` section — not outside it, not at the bottom of the file
- Add a comma after the closing `}` of the previous MCP server entry before adding the `"ecgrid-mcp"` block
- Do **not** add a second `"mcpServers"` section — there should only ever be one
- Do **not** paste the outer `{` and `}` again — they are already there

**If your file has no `"mcpServers"` section yet** — add the entire `"mcpServers": { ... }` block as a new entry inside the outer `{` `}`, with a comma after the preceding section:

```json
{
  "preferences": {
    "theme": "dark"
  },
  "mcpServers": {
    "ecgrid-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.ecgrid.io/mcp",
        "--header",
        "X-APIKey:YOUR_API_KEY_HERE",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

> **Not sure if your file is formatted correctly?** Paste the whole thing into [jsonlint.com](https://jsonlint.com) — it will highlight exactly where any error is.

---

**3c. Replace the placeholder**

Find this line in your config:

```
"X-APIKey:YOUR_API_KEY_HERE",
```

Replace `YOUR_API_KEY_HERE` with your actual ECGrid API Key. The finished line should look like:

```
"X-APIKey:abc123yourkeyhere",
```

Rules for this line:
- No spaces around the colon between `X-APIKey` and your key
- Keep the opening quote before `X-APIKey`
- Keep the closing quote and comma at the end
- Your key goes directly after the colon — no spaces

---

**3d. Save the file and restart Claude Desktop**

Save the file, then **fully close and reopen Claude Desktop** — not just minimize it. The ECGrid tools will be available after the restart.

---

### Cursor / Windsurf / Other MCP-Compatible Tools

Use the same server URL (`https://mcp.ecgrid.io/mcp`) and `X-APIKey` header. Many of these tools support remote MCP servers natively — check your tool's documentation for its config format. Node.js is not required if your tool connects to remote MCP servers directly.

**Cursor** (`~/.cursor/mcp.json` or via Settings → MCP):

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "url": "https://mcp.ecgrid.io/mcp",
      "headers": {
        "X-APIKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**Windsurf** (via Settings → MCP Servers → Add Server, or `~/.codeium/windsurf/mcp_config.json`):

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "serverUrl": "https://mcp.ecgrid.io/mcp",
      "headers": {
        "X-APIKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

> Config formats vary by tool version — if these don't match exactly, check your tool's documentation or paste this README into Claude and ask: *"How do I add this MCP server to [tool name]?"*

---

## Step 4 — Verify Your Connection

Once configured, test your connection by typing one of these prompts directly into your AI assistant:

- `What tools are available for the ECGrid MCP?`
- `Test the ECGrid MCP connection`
- `Run the ECGrid hello world tool with my name`
- `Connect to ECGrid and tell me my auth level`
- `What network ID does the ECGrid MCP return for me?`

A successful response will return your ECGrid login name, auth level, network ID, and current server time. If you see an error instead, go to the **Troubleshooting** section below.

---

## Developer Reference

> **AI-as-consumer model:** The ECGrid MCP Server is designed for AI agent consumption. Tools return structured data objects that an AI agent interprets and formats for the end user — the raw JSON is never presented directly to a human. As a result, some characteristics of the raw HTTP response may look unexpected when inspected manually in Postman or a terminal:
>
> - **SSE envelope** — responses arrive as `event: message / data: {...}` stream lines, not plain JSON
> - **`content[0].text` is a JSON string** — the MCP protocol wraps tool results as a JSON string inside `TextContent.text`; the AI parses this automatically, but a developer wiring up a direct HTTP integration must parse it a second time
> - **`\u0022` character escaping** — HTML-safe encoding makes raw output look different from what the AI ultimately receives; all values decode correctly after parsing
>
> If you are inspecting raw responses and something looks odd, it is almost certainly one of the above — expected behavior, not a bug.

### HTTP Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/mcp` | JSON-RPC entry point — `initialize`, `tools/list`, `tools/call` |
| `GET` | `/mcp` | Server-sent event stream for server-initiated notifications |
| `GET` | `/health/live` | Liveness probe — always returns `200 {"status":"healthy"}` if the process is running |
| `GET` | `/health/ready` | Readiness probe — `200` when healthy or degraded, `503` when unhealthy |

Health probes are anonymous and exempt from rate limiting. All other endpoints require authentication.

POST body size is capped at **64 KB**. Oversized requests return `413`. Non-JSON POST bodies return `415`.

---

### Testing with MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is an official open-source tool for interactively exploring and testing any MCP server. With Node.js installed, run:

```bash
npx @modelcontextprotocol/inspector "https://mcp.ecgrid.io/mcp" --header "X-APIKey:YOUR_API_KEY_HERE"
```

This opens a browser-based UI where you can browse available tools, inspect their schemas, and call them manually — useful for verifying your API key and exploring new tools as they are released.

---

### Initialization

Every MCP client must send an `initialize` request before calling any tools. MCP-compatible AI tools and SDKs handle this automatically. If you are building a custom agent from scratch, this must be your first request.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "your-client-name",
      "version": "1.0"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "logging": {},
      "tools": {}
    },
    "serverInfo": {
      "name": "ECGrid.Mcp.Server",
      "version": "1.0.0.0"
    }
  }
}
```

**Capabilities:**

| Capability | Description |
|---|---|
| `tools` | Server exposes callable tools via `tools/list` and `tools/call` |
| `logging` | Server supports MCP logging notifications |

**Protocol version:** `2024-11-05` — the MCP spec version this server implements. Pass this exact string in your `initialize` request. The server version is returned in `serverInfo.version`.

---

### Calling Tools

```
POST https://mcp.ecgrid.io/mcp
Content-Type: application/json
Accept: application/json, text/event-stream
X-APIKey: YOUR_API_KEY_HERE
```

**List available tools:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

**Call a tool:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "TOOL_NAME",
    "arguments": {
      "request": {
        "fieldName": "value"
      }
    }
  }
}
```

`tools/list` returns each tool's name, description, and full input schema. Check it periodically to pick up new tools as they are added. See the [ECGrid MCP Release Notes](ECGrid-MCP-Release-Notes.md) for what's new.

---

### Response Format

The ECGrid MCP Server returns all responses as **Server-Sent Events (SSE)**. This is the only supported response format — plain JSON is not available.

Every response arrives as an SSE envelope:

```
event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}
```

**Required `Accept` header:** The server requires that your request declares both media types or it returns a `406 Not Acceptable` error:

```
Accept: application/json, text/event-stream
```

**To parse the response**, read the body as text, find the `data:` line, strip the `data: ` prefix, and parse the remainder as JSON. The code examples below handle this correctly.

> MCP-compatible AI tools (Claude Desktop, Cursor, Windsurf, etc.) handle SSE parsing automatically. This only affects developers making direct HTTP calls.
>
> **New to SSE?** Server-Sent Events is a standard W3C protocol for streaming data over HTTP. See the [MDN SSE reference](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) for a full explanation of the format, including how `event:` and `data:` lines work, connection handling, and client implementations across languages.

> **Note on `\u0022` in raw output:** When reading the raw SSE stream, quote characters inside string values appear as `\u0022` rather than `"`. This is standard `System.Text.Json` HTML-safe encoding behavior and is expected — both forms are valid JSON and decode identically. Parse with any standard JSON library and the values will read correctly.

> **Tool result structure — two-step parse:** ECGrid MCP tools return structured data objects intended for AI agent consumption. The MCP protocol wraps the result as a JSON string inside `content[0].text`. After parsing the SSE envelope and the JSON-RPC response, parse `content[0].text` a second time to access the structured data:
>
> ```
> SSE data: line
>   → JSON.parse() → JSON-RPC result
>     → result.content[0].text  (this is a JSON string)
>       → JSON.parse() → { message, loginName, authLevel, networkId, ... }
> ```
>
> This is by design. The `text` field carries structured object data for the AI to interpret and present to the user — the AI agent handles formatting, not the raw JSON. The code examples in the Agent Guide implement this pattern.

---

### Code Examples

The following examples show the complete flow for a custom agent: initialize, list tools, and call `hello-world`. Replace `YOUR_API_KEY_HERE` with your ECGrid API key.

#### C#

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

var client = new HttpClient();
client.DefaultRequestHeaders.Add("X-APIKey", "YOUR_API_KEY_HERE");
client.DefaultRequestHeaders.Add("Accept", "application/json, text/event-stream"); // required by server

var baseUrl = "https://mcp.ecgrid.io/mcp";

async Task<JsonElement> PostAsync(object payload)
{
    var json = JsonSerializer.Serialize(payload);
    var response = await client.PostAsync(baseUrl,
        new StringContent(json, Encoding.UTF8, "application/json"));
    response.EnsureSuccessStatusCode();

    // Response is SSE — extract the data: line and parse as JSON
    var body = await response.Content.ReadAsStringAsync();
    var dataLine = body.Split('\n')
        .FirstOrDefault(l => l.StartsWith("data: "))
        ?.Substring(6) ?? body;
    return JsonDocument.Parse(dataLine).RootElement;
}

// Step 1 — Initialize
var initResult = await PostAsync(new {
    jsonrpc = "2.0", id = 1, method = "initialize",
    @params = new {
        protocolVersion = "2024-11-05",
        capabilities = new { },
        clientInfo = new { name = "my-agent", version = "1.0" }
    }
});
Console.WriteLine($"Server: {initResult.GetProperty("result").GetProperty("serverInfo")}");

// Step 2 — List tools
var toolsResult = await PostAsync(new {
    jsonrpc = "2.0", id = 2, method = "tools/list", @params = new { }
});
Console.WriteLine($"Tools: {toolsResult.GetProperty("result").GetProperty("tools")}");

// Step 3 — Call hello-world
var helloResult = await PostAsync(new {
    jsonrpc = "2.0", id = 3, method = "tools/call",
    @params = new {
        name = "hello-world",
        arguments = new { request = new { name = "My Agent" } }
    }
});
Console.WriteLine($"Response: {helloResult.GetProperty("result")}");
```

#### JavaScript (Node.js / Browser fetch)

```javascript
const BASE_URL = "https://mcp.ecgrid.io/mcp";
const API_KEY = "YOUR_API_KEY_HERE";

async function mcpPost(payload) {
  const res = await fetch(BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json, text/event-stream", // required by server
      "X-APIKey": API_KEY,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  // Response is SSE — extract the data: line and parse as JSON
  const text = await res.text();
  const dataLine = text.split("\n").find(l => l.startsWith("data: "));
  return JSON.parse(dataLine.slice(6));
}

// Step 1 — Initialize
const init = await mcpPost({
  jsonrpc: "2.0", id: 1, method: "initialize",
  params: {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "my-agent", version: "1.0" },
  },
});
console.log("Server:", init.result.serverInfo);

// Step 2 — List tools
const tools = await mcpPost({
  jsonrpc: "2.0", id: 2, method: "tools/list", params: {},
});
console.log("Tools:", tools.result.tools);

// Step 3 — Call hello-world
const hello = await mcpPost({
  jsonrpc: "2.0", id: 3, method: "tools/call",
  params: {
    name: "hello-world",
    arguments: { request: { name: "My Agent" } },
  },
});
console.log("Response:", hello.result);
```

#### Python

```python
import httpx
import json

BASE_URL = "https://mcp.ecgrid.io/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",  # required by server
    "X-APIKey": "YOUR_API_KEY_HERE",
}

def mcp_post(payload: dict) -> dict:
    response = httpx.post(BASE_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    # Response is SSE — extract the data: line and parse as JSON
    for line in response.text.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:])
    raise ValueError("No data line found in SSE response")

# Step 1 — Initialize
init = mcp_post({
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "my-agent", "version": "1.0"},
    },
})
print("Server:", init["result"]["serverInfo"])

# Step 2 — List tools
tools = mcp_post({
    "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {},
})
print("Tools:", json.dumps(tools["result"]["tools"], indent=2))

# Step 3 — Call hello-world
hello = mcp_post({
    "jsonrpc": "2.0", "id": 3, "method": "tools/call",
    "params": {
        "name": "hello-world",
        "arguments": {"request": {"name": "My Agent"}},
    },
})
print("Response:", hello["result"])
```

> For a full agent implementation guide including session handling, tool discovery patterns, and error handling, see the [ECGrid MCP Agent Guide](ECGrid-MCP-Agent-Guide.md).

---

### Authentication

All `/mcp` requests require exactly one of the following:

| Method | Header | Format |
|---|---|---|
| API Key | `X-APIKey` | Your ECGrid API key from the [ECGrid Developer Portal](https://api.ecgridos.io/) |
| Bearer JWT | `Authorization: Bearer <token>` | HS256 JWT — contact [ECGrid Support](https://ecgrid.freshdesk.com/support/home) if your integration requires JWT auth |

Sending both headers, or neither, returns `401`. The raw API key never appears in server logs.

**Auth Levels**

The `authLevel` field returned in tool responses identifies the permission tier of the API key used. The levels available to ECGrid customers and developers are:

| Auth Level | Access Type | Description |
|---|---|---|
| `TPUser` | Read-only | Trading partner — read-only access scoped to a single trading partner relationship. |
| `MailboxUser` | Standard | Mailbox-level user — standard access to a specific mailbox within a network. |
| `MailboxAdmin` | Admin | Mailbox-level admin — elevated access to manage a specific mailbox. |
| `NetworkUser` | Standard | Network-level user — standard access across all mailboxes within your ECGrid network. |
| `NetworkAdmin` | Admin | Network-level admin — full administrative access across your ECGrid network. Broadest level available to customers. |

If a tool requires a minimum auth level, that requirement is noted in the tool's documentation. If your key does not have sufficient access for an operation, review your account at the [ECGrid Developer Portal](https://api.ecgridos.io/) or contact [ECGrid Support](https://ecgrid.freshdesk.com/support/home).

---

### Rate Limiting

Rate limiting is enforced per IP address and fires **before** authentication — a `429` or `503` can be returned even for requests that would otherwise be rejected with `401`.

| Limit | Value | Rejection | `Retry-After` |
|---|---|---|---|
| Per-IP request rate | 100 requests / minute | `429 Too Many Requests` | 60 seconds |
| Global concurrency | 500 simultaneous requests | `503 Service Unavailable` | 1 second |

Both `429` and `503` responses include a JSON body:
```json
{
  "code": "RATE_LIMITED",
  "retryable": true
}
```

Health probes (`/health/live`, `/health/ready`) are exempt from rate limiting.

---

### Error Responses

All errors follow the JSON-RPC 2.0 error format:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Description of the error"
  }
}
```

**HTTP status codes:**

| Code | Meaning |
|---|---|
| `200` | Success |
| `400` | Bad request — malformed JSON or invalid JSON-RPC structure |
| `401` | Unauthorized — missing, invalid, or ambiguous credential |
| `404` | Not found — unrecognized path |
| `406` | Not Acceptable — `Accept` header missing or invalid; use `Accept: application/json, text/event-stream` |
| `413` | Payload too large — POST body exceeds 64 KB |
| `415` | Unsupported media type — POST body is not JSON |
| `429` | Too many requests — per-IP rate limit exceeded |
| `503` | Service unavailable — global concurrency cap reached |

---

### Health Probes

Use these endpoints to monitor server availability or integrate with a load balancer or uptime checker.

**Liveness** — is the process running?
```
GET https://mcp.ecgrid.io/health/live
```
Always returns `200 {"status":"healthy"}` if the server process is up. No authentication required.

**Readiness** — is the server ready to handle requests?
```
GET https://mcp.ecgrid.io/health/ready
```
Returns `200` when healthy or degraded. Returns `503` when the server is not ready to accept traffic. No authentication required.

---

## Available Tools

New tools are released regularly. Use `tools/list` to always get the current complete list at runtime. See the [ECGrid MCP Release Notes](ECGrid-MCP-Release-Notes.md) for the full history of tool additions including structured JSON response shapes for every tool.

**Response modes:** All tools return **structured JSON data** designed for AI agent and developer consumption — the AI interprets the data and presents it to the user in plain language; developers use it directly in their applications. A subset of tools additionally render an **interactive UI component** in compatible AI clients (Claude Desktop, Claude.ai) — a visual, browsable widget presented alongside the AI's response. Both modes use the same tool call and return the same data; the UI component is a presentation layer available in supported clients. The [ECGrid MCP Release Notes](ECGrid-MCP-Release-Notes.md) identify which tools include interactive UI components.

---

### `hello-world`

Verifies your connection and returns your authenticated ECGrid identity. Use this as a first test after setup, or as a connectivity check in your application.

**Returns:** Structured JSON — message (greeting), loginName, authLevel, networkId, mailboxId, serverTimeUtc.

**Auth level required:** Any

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.name` | string or null | No | Optional display name. Falls back to your ECGrid `loginName` if omitted. Max 256 characters. |

**Example request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "hello-world",
    "arguments": {
      "request": {
        "name": "Your Name"
      }
    }
  }
}
```

**Example response:**
```json
{
  "message": "Hello, Your Name, from ECGrid MCP server.",
  "loginName": "your-login",
  "authLevel": "NetworkUser",
  "networkId": "47",
  "mailboxId": "0",
  "serverTimeUtc": "2026-05-19T19:00:00Z"
}
```

**Response fields:**

| Field | Description |
|---|---|
| `message` | Greeting confirming the name passed in (or your loginName) |
| `loginName` | Your ECGrid account login name |
| `authLevel` | Your account's permission tier — see Auth Levels above |
| `networkId` | The ECGrid network your account belongs to |
| `mailboxId` | Your mailbox ID (0 = network-level account) |
| `serverTimeUtc` | Current ECGrid server time in UTC |

**Example prompts (AI desktop tools):**
- `What tools are available for the ECGrid MCP?`
- `Test the ECGrid MCP connection`
- `Run the ECGrid hello world tool with my name`
- `Connect to ECGrid and tell me my auth level`
- `What network ID does the ECGrid MCP return for me?`

---

## Other AI Platforms

The ECGrid MCP Server uses the open MCP standard. Any AI tool or platform that supports MCP natively can connect using the server URL and API key above — no additional setup required.

For AI platforms that do not yet support MCP natively — including ChatGPT, Grok, and others — direct MCP connection is not currently available. However, ECGrid provides a full REST API that any AI platform, custom integration, or GPT Action can call directly:

- **ECGrid REST API**: [rest.ecgrid.io](https://rest.ecgrid.io/index.html) — full interactive documentation
- **OpenAPI / Swagger spec**: [rest.ecgrid.io/swagger/v2/swagger.json](https://rest.ecgrid.io/swagger/v2/swagger.json) — machine-readable spec, suitable for import into ChatGPT Custom Actions, LangChain, or any OpenAPI-compatible toolchain

The REST API uses the same ECGrid API key (`X-APIKey` header) and covers the full breadth of ECGrid operations. If you are integrating ECGrid into a platform that doesn't support MCP, the REST API is the right path.

The chat loop pattern in the [ECGrid MCP Agent Guide](ECGrid-MCP-Agent-Guide.md) uses the Anthropic API, but the same structure applies to any LLM with tool/function calling support — OpenAI, Gemini, and others. The ECGrid client and conversation history management are identical; only the LLM client and tool schema format change.

> Questions about REST API integration? Visit the [ECGrid Developer Portal](https://api.ecgridos.io/) or contact [ECGrid Support](https://ecgrid.freshdesk.com/support/home).

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid or missing API key | Verify `X-APIKey` value — no spaces around the colon |
| `406 Not Acceptable` | Missing or incorrect `Accept` header | Set `Accept: application/json, text/event-stream` on every request |
| `429 Too Many Requests` | Per-IP rate limit hit | Wait 60 seconds and retry — check `Retry-After` header |
| `503 Service Unavailable` | Server concurrency cap reached | Wait 1 second and retry — this is transient |
| `Connection refused` | Incorrect server URL | Use `https://mcp.ecgrid.io/mcp` exactly |
| Tool not appearing in AI assistant | Config not loaded | Fully restart the AI application after saving the config file |
| Can't find the config file | Unsure of location | Open Claude Desktop → hamburger menu → Settings → Developer → Edit Config |
| Can't find the config file on macOS | Library folder is hidden | See Step 3a — use Go → Go to Folder, or run `open ~/Library/Application\ Support/Claude/` in Terminal |
| Can't find the config file on Windows | AppData folder is hidden | See Step 3a — paste `%APPDATA%\Claude\` directly into the File Explorer address bar |
| `node: command not found` or `npx: command not found` | Node.js not installed | See Step 2 — Claude Desktop users only; developers do not need Node.js |
| Node.js version too old | Version below v18 | Install the LTS version from [nodejs.org](https://nodejs.org) |
| JSON parse error on config file | Malformed JSON | Paste your config into [jsonlint.com](https://jsonlint.com) to find the error |
| ECGrid block not working despite no error | `mcpServers` block placed outside the main object or duplicated | Re-read Step 3b — the block must be inside the single outer `{ }` |
| `loginName` shows unexpected value | Wrong API key | Confirm the key matches your ECGrid account at the [ECGrid Developer Portal](https://api.ecgridos.io/) |
| `413 Payload Too Large` | Request body over 64 KB | Reduce request payload size |
| Empty or no `tools/list` response | Server unreachable or bad auth | Check API key and network connectivity; verify URL |

> **Still stuck?** Paste this entire document into Claude or any AI assistant and describe what you're seeing. The AI can read these instructions and help you diagnose the issue step by step.

---

## Support & Links

- **ECGrid Developer Portal**: [api.ecgridos.io](https://api.ecgridos.io/)
- **ECGrid REST API**: [rest.ecgrid.io](https://rest.ecgrid.io/index.html)
- **ECGrid REST API Swagger spec**: [rest.ecgrid.io/swagger/v2/swagger.json](https://rest.ecgrid.io/swagger/v2/swagger.json)
- **ECGrid Support**: [ecgrid.freshdesk.com/support/home](https://ecgrid.freshdesk.com/support/home)
- **ECGrid Platform**: [ecgrid.com](https://ecgrid.com)
- **Loren Data Corp**: [ld.com](https://www.ld.com)

---

## Related Documents

- [ECGrid MCP Agent Guide](ECGrid-MCP-Agent-Guide.md) — full developer walkthrough for building agents and chatbots
- [ECGrid MCP Release Notes](ECGrid-MCP-Release-Notes.md) — tool additions and changes by sprint

---

## License

Copyright © Loren Data Corp. All rights reserved.

---

## Change Log

| Date | Version | Changes |
|---|---|---|
| 2026-05-19 | 0.1 | Initial draft |
| 2026-05-19 | 0.2 | Updated server URL to mcp.ecgrid.io; expanded for dual audience; added developer HTTP call pattern and tool discovery section |
| 2026-05-19 | 0.3 | Full self-service revision: step-by-step Claude Desktop walkthrough, merge instructions, verification prompts, response field table, troubleshooting additions |
| 2026-05-19 | 0.4 | Clarified Node.js requirement — Claude Desktop only, not needed for developers or direct HTTP integrations |
| 2026-05-19 | 0.5 | Added Developer Reference section: HTTP endpoint table, initialize handshake, server capabilities, rate limiting, error format, health probe documentation |
| 2026-05-19 | 0.6 | Added Auth Levels table (TP, Mailbox, Network); added ECGrid Support link; updated Support & Links section |
| 2026-05-19 | 0.7 | Removed DELETE /mcp endpoint; added Quick Start section; added MCP Inspector one-liner; added C#/JS/Python code examples; replaced all "contractors" references with "developers"; added Developer Portal link; added Related Documents section |
| 2026-05-19 | 0.8 | Expanded Who This Is For — customers and developer sections rewritten |
| 2026-05-19 | 0.9 | Added Other AI Platforms section — non-MCP platforms directed to ECGrid REST API with Swagger spec |
| 2026-05-19 | 1.0 | Added Let Claude Install It For You section |
| 2026-05-19 | 1.1 | Expanded Step 2 Node.js check/install; expanded Step 3b JSON merge instructions with all four file states |
| 2026-05-19 | 1.2 | Replaced single install prompt with three options: Option A (Claude Desktop automated), Option B (web/mobile guided), Option C (full document paste) |
| 2026-05-19 | 1.3 | Step 3a — macOS hidden Library folder documented with three access methods |
| 2026-05-19 | 1.4 | Step 3a — Windows AppData hidden folder documented with address bar shortcut and View > Hidden Items toggle |
| 2026-05-19 | 1.5 | Auth Levels table updated — full customer-facing enum: TPUser, MailboxUser, MailboxAdmin, NetworkUser, NetworkAdmin |
| 2026-05-19 | 1.6 | Added Response Format section; updated code examples with Accept header |
| 2026-05-21 | 1.7 | Corrected Response Format — SSE only, 406 on incorrect Accept header; all code examples updated to parse SSE data: line |
| 2026-05-21 | 1.8 | Added \u0022 unicode escaping note — expected System.Text.Json behavior, not a bug |
| 2026-05-21 | 1.9 | Added MDN SSE reference link for developers unfamiliar with the protocol |
| 2026-05-21 | 2.0 | Step 3a — added Settings → Developer → Edit Config as the primary method to open the config file; manual paths retained as fallback; Option B install prompt updated to mention Edit Config; troubleshooting row added for config file not found |
| 2026-05-21 | 2.1 | Added tool result two-step parse note to Response Format — content[0].text is a JSON string by MCP design; structured data intended for AI agent consumption, not direct display |
| 2026-05-21 | 2.2 | Added AI-as-consumer model callout to Developer Reference — explains SSE envelope, content[0].text JSON string, and \u0022 escaping as expected raw output characteristics |
| 2026-05-21 | 2.3 | Rewrote Node.js note — plain language framing, clear that Claude Desktop requires it not ECGrid, calming one-time install language, future-looking note that it goes away; added non-developer reassurance callout to Step 2 header |
| 2026-05-21 | 2.4 | Added Cursor and Windsurf config examples to Step 3; added non-Anthropic platform note to Other AI Platforms section |
| 2026-05-21 | 2.5 | Step 2 — expanded terminal instructions for both macOS (2 methods) and Windows (3 methods) with step-by-step callout boxes; added troubleshooting note for common node --version mistakes; expanded Node.js installer steps |
| 2026-07-06 | 2.6 | Who This Is For — added interactive UI component bullet to Customers section; added structured JSON + UI component bullet to Developers section; Available Tools section updated with response modes callout explaining structured JSON (all tools) and interactive UI components (subset of tools, identified in Release Notes); hello-world tool entry updated with Returns field; full tool inventory documented in ECGrid MCP Release Notes v1.0 |
