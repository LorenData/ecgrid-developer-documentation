---
title: list-catalog-products
sidebar_position: 3
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-20: datasync_catalog_list-products tool reference - Greg Kolinski
*/}

# list-catalog-products

List the products that belong to one specific GPA catalog. Use when you have a catalog id (from [list-catalogs](./list-catalogs.md)) and want the products inside it. Supports the same paging, search, sort, and product filters as [list-products](../product/list-products.md), scoped to the given catalog.

This lists products the caller **owns** within the catalog — it is not a buyer-facing browse of another company's catalog.

Company-scoped callers are auto-scoped. Host / NetworkAdmin callers must pass `companyId`.

## Tool Name

`datasync_catalog_list-products`

## Credential Required

`X-DataSync-API-Key` — your GPA Personal Access Token (PAT)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.catalogId` | string | **Yes** | The catalog's GUID id whose products to list. |
| `request.page` | integer \| null | No | 1-based page number. Omit for the first page. |
| `request.pageSize` | integer \| null | No | Page size (max 1000). Omit for backend default. |
| `request.search` | string \| null | No | Free-text search across product name and SKU. |
| `request.sortBy` | string \| null | No | Field to sort by. |
| `request.sortDesc` | boolean \| null | No | Sort descending when `true`. |
| `request.status` | string \| null | No | Filter by lifecycle status: `Active`, `Draft`, or `Archived`. |
| `request.productCategoryGlobal` | string \| null | No | Filter by global product-category code. |
| `request.currencyCodeIso` | string \| null | No | Filter by ISO currency code (e.g. `USD`). |
| `request.priceFrom` | number \| null | No | Minimum selling price (inclusive). |
| `request.priceTo` | number \| null | No | Maximum selling price (inclusive). |
| `request.stockFrom` | integer \| null | No | Minimum available quantity (inclusive). |
| `request.stockTo` | integer \| null | No | Maximum available quantity (inclusive). |
| `request.skuInternalIdentifier` | string \| null | No | Filter by internal SKU identifier. |
| `request.companyId` | string \| null | No | Target company GUID. Required for Host / NetworkAdmin callers; ignored for company-scoped callers. |

## Response

Returns a page of products plus pagination totals.

```json
{
  "totalCount": 124,
  "totalPages": 2,
  "products": [
    {
      "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
      "name": "Men's Polo Shirt",
      "skuInternalIdentifier": "SKU-POLO-M-BLU",
      "status": "Active",
      "productCategoryGlobal": "Apparel",
      "price": 29.99,
      "currencyCodeIso": "USD",
      "availableQuantity": 500
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
    "name": "datasync_catalog_list-products",
    "arguments": {
      "request": {
        "catalogId": "c3d4e5f6-a7b8-9012-cdef-123456789012",
        "status": "Active",
        "search": "polo"
      }
    }
  }
}
```

## Example Prompts

- `What products are in catalog X?`
- `List active products in the Apparel Spring 2026 catalog`
- `Find polo shirts in my spring catalog`

## See Also

- [list-catalogs](./list-catalogs.md) — get a catalogId
- [list-products](../product/list-products.md) — list all products across all catalogs
- [get-product-details](../product/get-product-details.md) — get the full record for a single product
