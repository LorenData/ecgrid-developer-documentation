---
title: ChatGPT
sidebar_position: 3
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-07: ChatGPT connection guide - Greg Kolinski
2026-07-07: Add JavaScript tab to Responses API example - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Connect ChatGPT to ECGrid

There are two ways to use ECGrid capabilities in ChatGPT, depending on your goal.

| Approach | What it gives you |
|---|---|
| **Custom GPT** (Actions) | Full ECGrid REST API inside a purpose-built GPT |
| **OpenAI Responses API** | Programmatic ECGrid MCP tool access for developers building apps |

---

## Option 1 — Custom GPT with ECGrid REST API (Recommended)

A Custom GPT is a purpose-built version of ChatGPT that can call the ECGrid REST API directly using OpenAI's **Actions** feature. You import the ECGrid OpenAPI spec, add your API key, and ChatGPT can look up mailboxes, query interchanges, check partner status, and perform any other ECGrid operation — no MCP required.

**Who can use this:** ChatGPT Plus, Pro, Team, Business, and Enterprise accounts.

### Step 1 — Open the GPT Editor

In [chat.openai.com](https://chat.openai.com), click your profile picture → **My GPTs** → **Create a GPT** → **Configure** tab.

Give your GPT a name and description, for example:
- **Name:** ECGrid Assistant
- **Description:** Helps manage EDI trading partners, mailboxes, interchanges, and parcels on ECGrid.

### Step 2 — Add the ECGrid Action

In the **Configure** tab, scroll to **Actions** and click **Create new action**.

In the **Schema** field, import or paste the ECGrid OpenAPI spec URL:

```
https://rest.ecgrid.io/swagger/v2/swagger.json
```

Click **Import from URL**. ChatGPT will fetch and parse the spec, listing all available ECGrid REST endpoints.

### Step 3 — Configure Authentication

After importing the schema, click **Authentication** and configure:

| Field | Value |
|---|---|
| Authentication type | `API Key` |
| API key | Your ECGrid API key |
| Auth type | `Custom` |
| Custom header name | `X-APIKey` |

:::caution Keep your API key secure
Enter your API key in the Authentication dialog — never paste it into the GPT's instructions or the schema. OpenAI stores it encrypted and does not expose it in the GPT configuration UI.
:::

### Step 4 — Set Instructions (Optional)

In the **Instructions** box you can give the GPT context about ECGrid, for example:

```
You are an ECGrid EDI assistant. ECGrid is a B2B EDI network that routes electronic
trading documents between businesses. You can look up mailboxes, trading partners,
interchanges, and parcels. When a user asks about EDI traffic, use the ECGrid API
tools to retrieve live data. Always show network and mailbox IDs when displaying results.
```

### Step 5 — Save and Test

Click **Save** (top right) → choose **Only me** or **Anyone with the link** for access.

Open your new GPT and test with prompts like:

```
What mailboxes are on network 7?
Show me the interchange status for interchange 123456789
Are there any pending parcels in mailbox 142's inbox?
```

### What the Custom GPT Can Do

The ECGrid REST API has 121 endpoints across 16 categories. Through the Custom GPT Actions your GPT can:

- Look up mailboxes, networks, trading partners, and comm records
- List inbox/outbox parcels and interchanges
- Query interchange status and document counts
- Check callback registrations and carbon copy rules
- Retrieve user and key/value data

For the full endpoint list, see the [ECGrid REST API reference](../../rest-api/overview.md).

---

## Option 2 — OpenAI Responses API (Developers)

If you are building an application using the OpenAI Responses API, you can connect it directly to the ECGrid MCP server by passing `X-APIKey` as a custom header. Headers are supplied per-request alongside the tool configuration.

<Tabs groupId="lang">
<TabItem value="python" label="Python">

```python
from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY from environment

response = client.responses.create(
    model="gpt-4o",
    tools=[
        {
            "type": "mcp",
            "server_label": "ecgrid",
            "server_url": "https://mcp.ecgrid.io/mcp",
            "headers": {
                "X-APIKey": "YOUR_ECGRID_API_KEY"
            },
            "require_approval": "never"
        }
    ],
    input="List the pending parcels in mailbox 142 on network 7"
)

print(response.output_text)
```

</TabItem>
<TabItem value="javascript" label="JavaScript">

```javascript
import OpenAI from "openai";

const client = new OpenAI(); // uses OPENAI_API_KEY from environment

const response = await client.responses.create({
  model: "gpt-4o",
  tools: [
    {
      type: "mcp",
      server_label: "ecgrid",
      server_url: "https://mcp.ecgrid.io/mcp",
      headers: {
        "X-APIKey": "YOUR_ECGRID_API_KEY",
      },
      require_approval: "never",
    },
  ],
  input: "List the pending parcels in mailbox 142 on network 7",
});

console.log(response.output_text);
```

</TabItem>
</Tabs>

:::caution Headers per request
The Responses API does not store headers between requests. Supply `X-APIKey` in the `headers` field on every call.
:::

The Responses API path gives you programmatic access to all 41 ECGrid MCP tools with the full tool schema, resources, and prompts.

---

## See Also

- [Authentication](../authentication.md) — ECGrid API key format and how to obtain one
- [Claude Desktop](./claude-desktop.md) — connect Claude Desktop for the full MCP experience including UI components
- [Tools Reference](../tools/overview.md) — all 41 ECGrid MCP tools
- [ECGrid REST API](../../rest-api/overview.md) — full REST reference used by the Custom GPT Actions path
