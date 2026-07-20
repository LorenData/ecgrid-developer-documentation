---
title: list-products
sidebar_position: 4
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-20: datasync_product_list-products tool reference - Greg Kolinski
*/}

# list-products

List products in the GPA (Global Product Access) system for a company. Use to browse or search a company's full product set across all catalogs — e.g. "show my products", "find products with SKU containing ABC", or page through the full catalog. Supports paging, free-text search, sorting, and product filters.

To list products scoped to one catalog, use [list-catalog-products](./list-catalog-products.md). For the full detail of a single product, use [get-product-details](./get-product-details.md).

Company-scoped callers (CompanyAdmin / CompanyUser) are auto-scoped. Host / NetworkAdmin callers must pass `companyId` — use [list-companies](./list-companies.md) first to get the target company's id.

## Tool Name

`datasync_product_list-products`

## Credential Required

`X-DataSync-API-Key` — your GPA Personal Access Token (PAT)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
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
| `request.catalogId` | string \| null | No | Restrict to products published in this catalog GUID. |
| `request.skuInternalIdentifier` | string \| null | No | Filter by internal SKU identifier. |
| `request.companyId` | string \| null | No | Target company GUID. Required for Host / NetworkAdmin callers; ignored for company-scoped callers. |

## Response

Returns a page of product records plus pagination totals.

```json
{
  "totalCount": 850,
  "totalPages": 9,
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

## Response Fields

| Field | Type | Description |
|---|---|---|
| `totalCount` | integer | Total number of products matching the filter |
| `totalPages` | integer | Total pages at the requested page size |
| `products` | array | Page of product records |
| `products[].id` | string | Product GUID — use as `productId` in [get-product-details](./get-product-details.md) |
| `products[].name` | string | Product name |
| `products[].skuInternalIdentifier` | string | Internal SKU identifier |
| `products[].status` | string | Lifecycle status: Active, Draft, or Archived |
| `products[].productCategoryGlobal` | string | Global product-category code |
| `products[].price` | number | Selling price |
| `products[].currencyCodeIso` | string | ISO currency code (e.g. USD) |
| `products[].availableQuantity` | integer | Current available stock quantity |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "datasync_product_list-products",
    "arguments": {
      "request": {
        "search": "polo",
        "status": "Active",
        "currencyCodeIso": "USD"
      }
    }
  }
}
```

## Example Prompts

- `Show my products`
- `Find products with SKU containing ABC`
- `List all active products priced under $50`
- `Show products in the Apparel category`

## See Also

- [get-product-details](./get-product-details.md) — full record for a single product by id
- [list-catalog-products](./list-catalog-products.md) — products scoped to one catalog
- [list-catalogs](./list-catalogs.md) — browse available catalogs
