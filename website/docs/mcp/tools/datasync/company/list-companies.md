---
title: list-companies
sidebar_position: 1
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-20: datasync_company_list-companies tool reference - Greg Kolinski
*/}

# list-companies

List the GPA companies you can act on behalf of. Use this first when you are a Host or NetworkAdmin and need a `companyId` to pass to the product and catalog tools — it returns each company's id, name, and email so you can pick the target.

A Host sees every company. A NetworkAdmin sees the companies in their network. Company-scoped callers (CompanyAdmin / CompanyUser) are auto-scoped to their own company and do not need this tool.

## Tool Name

`datasync_company_list-companies`

## Credential Required

`X-DataSync-API-Key` — your GPA Personal Access Token (PAT)

## Auth Role

Host or NetworkAdmin only. Company-scoped callers receive an authorization error.

## Parameters

This tool takes no input parameters.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request` | object | Yes | Empty object — no fields required |

## Response

Returns a list of companies, each with an id, name, and email address.

```json
{
  "companies": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Acme Corporation",
      "email": "edi@acme.example.com"
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "name": "Beta Supplies Inc.",
      "email": "catalog@betasupplies.example.com"
    }
  ]
}
```

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "datasync_company_list-companies",
    "arguments": {
      "request": {}
    }
  }
}
```

## Example Prompts

- `List the companies I can manage in GPA`
- `What companies are on my network in DataSync?`
- `Show me all GPA companies`

## See Also

- [list-catalogs](../catalog/list-catalogs.md) — browse catalogs for a company
- [list-products](../product/list-products.md) — browse products for a company
