{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-06-17: Code examples section - Christian Nichols */}

---
title: JavaScript / Node.js
sidebar_position: 2
---

# JavaScript / Node.js Examples

These examples use the native `fetch` API available in Node.js 18+ and all modern browsers. No dependencies required.

**Base URL:** `https://rest.ecgrid.io`

---

## Setup

```js
const BASE_URL = 'https://rest.ecgrid.io';

async function ecgrid(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json();
    throw Object.assign(new Error(error.title ?? 'ECGrid API error'), {
      status:  response.status,
      detail:  error.detail,
      traceId: error.traceId,
    });
  }

  return response.json();
}
```

---

## Authentication

```js
// POST /v2/auth/login
async function login(apiKey) {
  const result = await ecgrid('/v2/auth/login', {
    method: 'POST',
    body: JSON.stringify({ apiKey }),
  });

  return result.data.sessionKey;
}

const sessionKey = await login('YOUR_API_KEY');
console.log('Session key:', sessionKey);
```

All subsequent calls pass the session key as a Bearer token:

```js
// Helper that injects the session key automatically
function makeClient(sessionKey) {
  return function(path, options = {}) {
    return ecgrid(path, {
      ...options,
      headers: {
        Authorization: `Bearer ${sessionKey}`,
        ...options.headers,
      },
    });
  };
}

const api = makeClient(sessionKey);
```

### Handling session expiry

```js
async function withRetry(apiKey, fn) {
  let sessionKey = await login(apiKey);
  let api = makeClient(sessionKey);

  try {
    return await fn(api);
  } catch (err) {
    if (err.status === 401) {
      // Re-authenticate and retry once
      sessionKey = await login(apiKey);
      api = makeClient(sessionKey);
      return fn(api);
    }
    throw err;
  }
}

// Usage
const result = await withRetry('YOUR_API_KEY', async (api) => {
  return api('/v2/mailboxes/list', {
    method: 'POST',
    body: JSON.stringify({ networkId: 5050, mailboxId: 0, showInactive: false }),
  });
});
```

---

## Mailboxes

### Get a mailbox by ID

```js
// GET /v2/mailboxes/{id}
const result = await api(`/v2/mailboxes/1234`);
const { mailboxName, networkName } = result.data;
console.log(`${mailboxName} on ${networkName}`);
```

### List mailboxes on a network

```js
// POST /v2/mailboxes/list
const result = await api('/v2/mailboxes/list', {
  method: 'POST',
  body: JSON.stringify({
    networkId:    5050,
    mailboxId:    0,
    showInactive: false,
  }),
});

result.data.forEach(mb => {
  console.log(`${mb.mailboxId}: ${mb.mailboxName}`);
});
```

---

## Interchanges

### List inbound interchanges

```js
// POST /v2/interchanges/inbox-list
const today     = new Date().toISOString().split('T')[0];
const weekAgo   = new Date(Date.now() - 7 * 86400000).toISOString().split('T')[0];

const result = await api('/v2/interchanges/inbox-list', {
  method: 'POST',
  body: JSON.stringify({
    networkId:  5050,
    mailboxId:  0,
    startDate:  weekAgo,
    endDate:    today,
    pageSize:   50,
    pageIndex:  1,
  }),
});

result.data.forEach(ix => {
  console.log(`${ix.interchangeId} | From: ${ix.senderEDIId} | ${ix.statusDescription}`);
});
```

---

## Callbacks

### Create a webhook callback

```js
// POST /v2/callbacks/create
const result = await api('/v2/callbacks/create', {
  method: 'POST',
  body: JSON.stringify({
    networkId:         5050,
    mailboxId:         0,
    userId:            1001,
    systemObject:      'Interchange',
    objectStatus:      5,           // 5 = Ready
    direction:         'InBox',
    frequency:         60,
    maxRetries:        24,
    url:               'https://your-system.com/webhook/ecgrid',
    httpAuthentication: null,
    status:            'Active',
  }),
});

console.log('Callback event ID:', result.data.callBackEventId);
```

### List callbacks for a mailbox

```js
// POST /v2/callbacks/event-list
const result = await api('/v2/callbacks/event-list', {
  method: 'POST',
  body: JSON.stringify({
    networkId:    5050,
    mailboxId:    0,
    showInactive: false,
  }),
});

result.data.forEach(cb => {
  console.log(`${cb.callBackEventId}: ${cb.url} [${cb.statusDescription}]`);
});
```

---

## Keys (Metadata)

### Create a metadata key

```js
// POST /v2/keys/create
await api('/v2/keys/create', {
  method: 'POST',
  body: JSON.stringify({
    key:          'integration.vendorCode',
    systemObject: 'Mailbox',
    objectId:     1234,
    visibility:   'Private',
    value:        'ACME-001',
    meta:         'Vendor code for ACME Corp integration',
    daysToLive:   -1,   // -1 = no expiry
  }),
});

console.log('Key created.');
```

### List all keys on an object

```js
// POST /v2/keys/list
const result = await api('/v2/keys/list', {
  method: 'POST',
  body: JSON.stringify({
    systemObject: 'Mailbox',
    objectId:     1234,
  }),
});

result.data.forEach(k => {
  console.log(`${k.key}: ${k.value}`);
});
```

---

## Error Handling

The `ecgrid` helper throws on non-2xx responses. Errors include `status`, `detail`, and `traceId`:

```js
try {
  const result = await api('/v2/mailboxes/list', {
    method: 'POST',
    body: JSON.stringify({ networkId: 5050, mailboxId: 0, showInactive: false }),
  });
} catch (err) {
  console.error(`${err.status}: ${err.message}`);
  console.error('Detail:', err.detail);
  console.error('Trace ID:', err.traceId);

  // Include traceId when contacting ECGrid support
}
```
