---
title: list-catalogs
sidebar_position: 2
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-20: datasync_catalog_list-catalogs tool reference - Greg Kolinski
*/}

# list-catalogs

List catalogs in the GPA (Global Product Access) system for a company. Use to browse or search catalogs, find a specific catalog by name, or see product and subscriber counts per catalog. Supports paging, free-text search, sorting, and filters by name, description, status, and type.

Company-scoped callers (CompanyAdmin / CompanyUser) are auto-scoped to their own company. Host / NetworkAdmin callers must pass `companyId` — use [list-companies](./list-companies.md) first to get the target company's id.

## Tool Name

`datasync_catalog_list-catalogs`

## Credential Required

`X-DataSync-API-Key` — your GPA Personal Access Token (PAT)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.page` | integer \| null | No | 1-based page number. Omit for the first page. |
| `request.pageSize` | integer \| null | No | Page size (max 1000). Omit for backend default. |
| `request.search` | string \| null | No | Free-text search across catalog name and description. |
| `request.sortBy` | string \| null | No | Field to sort by. |
| `request.sortDesc` | boolean \| null | No | Sort descending when `true`. |
| `request.name` | string \| null | No | Filter by catalog name. |
| `request.description` | string \| null | No | Filter by catalog description. |
| `request.status` | string \| null | No | Filter by lifecycle status: `Active`, `Archived`, or `Draft`. |
| `request.type` | string \| null | No | Filter by visibility type: `Public` or `Private`. |
| `request.companyId` | string \| null | No | Target company GUID. Required for Host / NetworkAdmin callers; ignored for company-scoped callers. |

## Response

Returns a page of catalog records plus pagination totals.

```json
{
  "totalCount": 3,
  "totalPages": 1,
  "catalogs": [
    {
      "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "name": "Apparel Spring 2026",
      "description": "Spring seasonal apparel catalog",
      "status": "Active",
      "type": "Public",
      "productCount": 412,
      "subscriberCount": 7,
      "created": "2026-01-15T00:00:00Z",
      "modified": "2026-06-01T10:22:00Z"
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `totalCount` | integer | Total number of catalogs matching the filter |
| `totalPages` | integer | Total number of pages at the requested page size |
| `catalogs` | array | Page of catalog records |
| `catalogs[].id` | string | Catalog GUID — use as `catalogId` in other tools |
| `catalogs[].name` | string | Catalog name |
| `catalogs[].description` | string | Catalog description |
| `catalogs[].status` | string | Lifecycle status: Active, Archived, or Draft |
| `catalogs[].type` | string | Visibility type: Public or Private |
| `catalogs[].productCount` | integer | Number of products in the catalog |
| `catalogs[].subscriberCount` | integer | Number of subscribers to the catalog |
| `catalogs[].created` | string | ISO 8601 creation timestamp |
| `catalogs[].modified` | string | ISO 8601 last-modified timestamp |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "datasync_catalog_list-catalogs",
    "arguments": {
      "request": {
        "status": "Active",
        "type": "Public"
      }
    }
  }
}
```

## Example Prompts

- `Show my catalogs`
- `Find the Apparel catalog`
- `List all active public catalogs`
- `How many products are in each of my catalogs?`

## See Also

- [list-catalog-products](./list-catalog-products.md) — list products within a specific catalog
- [list-products](./list-products.md) — list all products for a company across all catalogs
- [list-companies](./list-companies.md) — get a companyId (Host / NetworkAdmin)
