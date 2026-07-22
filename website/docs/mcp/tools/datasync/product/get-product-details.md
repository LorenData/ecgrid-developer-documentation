---
title: get-product-details
sidebar_position: 5
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-20: datasync_product_get-product-details tool reference - Greg Kolinski
*/}

# get-product-details

Get the full detail of a single GPA (Global Product Access) product by its GUID id. Use when you already have a product id (from [list-products](./list-products.md) or [list-catalog-products](../catalog/list-catalog-products.md)) and want the complete record: SKU, name, description, pricing, currency, available quantity, and status.

Pass an optional `catalogId` to scope catalog data and price visibility to one catalog. Returns NOT_FOUND when no product matches the id or it is not visible to the caller.

Company-scoped callers are auto-scoped. Host / NetworkAdmin callers must pass `companyId`.

## Tool Name

`datasync_product_get-product-details`

## Credential Required

`X-DataSync-API-Key` — your GPA Personal Access Token (PAT)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.productId` | string | **Yes** | The product's GUID id. |
| `request.catalogId` | string \| null | No | Optional catalog GUID to scope catalog data and price visibility. |
| `request.companyId` | string \| null | No | Target company GUID. Required for Host / NetworkAdmin callers; ignored for company-scoped callers. |

## Response

Returns the full product record.

```json
{
  "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "name": "Men's Polo Shirt",
  "description": "Classic fit cotton polo shirt, available in multiple colors.",
  "skuInternalIdentifier": "SKU-POLO-M-BLU",
  "status": "Active",
  "productCategoryGlobal": "Apparel",
  "price": 29.99,
  "currencyCodeIso": "USD",
  "availableQuantity": 500,
  "created": "2025-11-01T00:00:00Z",
  "modified": "2026-06-15T08:45:00Z"
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Product GUID |
| `name` | string | Product name |
| `description` | string | Full product description |
| `skuInternalIdentifier` | string | Internal SKU identifier |
| `status` | string | Lifecycle status: Active, Draft, or Archived |
| `productCategoryGlobal` | string | Global product-category code |
| `price` | number | Selling price (may be catalog-scoped when `catalogId` supplied) |
| `currencyCodeIso` | string | ISO currency code (e.g. USD) |
| `availableQuantity` | integer | Current available stock quantity |
| `created` | string | ISO 8601 creation timestamp |
| `modified` | string | ISO 8601 last-modified timestamp |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "datasync_product_get-product-details",
    "arguments": {
      "request": {
        "productId": "d4e5f6a7-b8c9-0123-defa-234567890123"
      }
    }
  }
}
```

## Example Prompts

- `Show the full details for product d4e5f6a7-...`
- `What is the price and stock level for SKU-POLO-M-BLU?`
- `Get the description of product X`

## See Also

- [list-products](./list-products.md) — search and browse products to find a productId
- [list-catalog-products](../catalog/list-catalog-products.md) — products scoped to one catalog
