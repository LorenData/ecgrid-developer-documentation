---
title: Error Codes
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created error codes reference page for REST and SOAP APIs - Greg Kolinski */}

# Error Codes

This page documents the error response formats and common error codes for both the ECGrid REST API (v2.6) and the ECGridOS SOAP API (v4.1).

---

## REST API Errors

### Error Response Format

All REST API errors return a consistent JSON envelope with `success: false`.

```json
{
  "success": false,
  "errorCode": "InvalidAPIKey",
  "message": "The provided API key is not valid or has been revoked.",
  "data": null
}
```

| Field | Type | Description |
|---|---|---|
| `success` | boolean | Always `false` for error responses |
| `errorCode` | string | Machine-readable error code (see table below) |
| `message` | string | Human-readable description of the error |
| `data` | null | Always `null` on error |

### Common REST Error Codes

| Error Code | HTTP Status | Description |
|---|---|---|
| `InvalidAPIKey` | 401 | The API key in the `X-API-Key` header is missing, invalid, or has been revoked. |
| `InvalidSession` | 401 | The Bearer token in the `Authorization` header is expired, malformed, or invalid. |
| `AccessDenied` | 403 | The authenticated user or API key does not have sufficient `AuthLevel` for the requested operation. |
| `ObjectNotFound` | 404 | The requested resource (mailbox, parcel, interchange, etc.) does not exist or is not accessible to the caller. |
| `InvalidParameter` | 400 | One or more request parameters are missing, the wrong type, or fail a validation constraint. Check the `message` field for details on which parameter failed. |
| `RateLimitExceeded` | 429 | The caller has exceeded the allowed request rate. Wait before retrying. Check the `Retry-After` response header for the recommended delay. |
| `InternalError` | 500 | An unexpected server-side error occurred. If this persists, contact ECGrid support. |

### Authentication Header Reference

| Scenario | Header |
|---|---|
| API key authentication | `X-API-Key: <your-api-key>` |
| JWT Bearer authentication | `Authorization: Bearer <token>` |

See [Authentication & API Keys](../getting-started/authentication-api-keys) for how to obtain and use credentials.

---

## SOAP API Errors

### Error Response Format

The ECGridOS SOAP API returns errors as standard SOAP Faults. The fault detail contains an `ECGridOSSOAPErrorCode` element that identifies the specific error.

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <soap:Fault>
      <faultcode>soap:Client</faultcode>
      <faultstring>Invalid Session ID</faultstring>
      <detail>
        <ECGridOSSOAPErrorCode>Authentication</ECGridOSSOAPErrorCode>
      </detail>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>
```

| Element | Description |
|---|---|
| `faultcode` | `soap:Client` for caller errors; `soap:Server` for server-side errors |
| `faultstring` | Human-readable error description |
| `ECGridOSSOAPErrorCode` | Machine-readable ECGridOS error category |

### Common SOAP ECGridOSSOAPErrorCode Values

| Code | Description |
|---|---|
| `Authentication` | The `SessionID` parameter is missing, expired, or invalid. Obtain a new session via `Login()`. |
| `Authorization` | The session does not have sufficient permission for the requested operation. |
| `ObjectNotFound` | The requested object (network, mailbox, ECGrid ID, etc.) does not exist. |
| `InvalidParameter` | One or more method parameters are invalid or out of range. |
| `SystemError` | An unexpected server-side error occurred. Contact ECGrid support if the issue persists. |

:::caution Established API
The SOAP API is in maintenance mode. For new integrations, use the [REST API](../rest-api/overview) instead.
:::

---

## Handling Errors in C#

### REST — Checking for Errors

```csharp
// .NET 10 — check the success flag before using data
var response = await httpClient.GetAsync("https://rest.ecgrid.io/v2/mailbox/12345");
var json = await response.Content.ReadFromJsonAsync<ApiResponse<MailboxInfo>>();

if (json is null || !json.Success)
{
    Console.Error.WriteLine($"Error [{json?.ErrorCode}]: {json?.Message}");
    return;
}

// Safe to use json.Data here
```

### SOAP — Catching SOAP Faults

```csharp
// .NET 10 — dotnet-svcutil generated proxy
try
{
    var result = await client.MailboxInfoAsync(sessionID, mailboxID);
}
catch (FaultException ex)
{
    // ex.Message contains the faultstring
    Console.Error.WriteLine($"SOAP Fault: {ex.Message}");
}
```

---

## See Also

- [Authentication & API Keys](../getting-started/authentication-api-keys)
- [Authentication & Session Management](../guides/authentication-session-management)
- [Error Handling & Troubleshooting](../guides/error-handling-troubleshooting)
- [ENUMs Reference](./enums) — `AuthLevel` enum for permission levels
