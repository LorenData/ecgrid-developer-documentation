#!/usr/bin/env python3
"""
add_tabs_guides2.py
Add multi-language code tabs to guide/*.md and code-samples/*.md files.
Date: 2026-05-08
"""
import re, os

BASE = r"E:\LD_Code\ECGrid Developer Documentation Portal\website\docs"
TABS_IMPORT = "import Tabs from '@theme/Tabs';\nimport TabItem from '@theme/TabItem';\n"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def ensure_tabs_import(text):
    if "import Tabs from '@theme/Tabs'" in text:
        return text
    m = re.search(r'\{/\*.*?\*/\}', text, re.DOTALL)
    if m:
        p = m.end()
        return text[:p] + '\n\n' + TABS_IMPORT + text[p:]
    return text

def update_attribution(text, desc):
    def repl(m):
        return m.group(1) + '\n| 2026-05-08: ' + desc + ' - Greg Kolinski\n' + m.group(2)
    return re.sub(r'(\{/\* AI Attribution.*?)(\*/\})', repl, text, flags=re.DOTALL, count=1)

def _tab(value, label, lang, code, default=False):
    d = ' default' if default else ''
    return f'<TabItem value="{value}" label="{label}"{d}>\n\n```{lang}\n{code}\n```\n\n</TabItem>'

def rest_block(curl, java, nodejs, python):
    """Closure: takes csharp, returns REST 5-tab block (no heading)."""
    def builder(csharp):
        items = '\n'.join([
            _tab('curl', 'cURL', 'bash', curl),
            _tab('csharp', 'C#', 'csharp', csharp, True),
            _tab('java', 'Java', 'java', java),
            _tab('nodejs', 'Node.js', 'javascript', nodejs),
            _tab('python', 'Python', 'python', python),
        ])
        return '<Tabs groupId="lang">\n' + items + '\n</Tabs>'
    return builder

def soap_block(java, nodejs, python):
    """Closure: takes csharp, returns SOAP 4-tab block (no heading)."""
    def builder(csharp):
        items = '\n'.join([
            _tab('csharp', 'C#', 'csharp', csharp, True),
            _tab('java', 'Java', 'java', java),
            _tab('nodejs', 'Node.js', 'javascript', nodejs),
            _tab('python', 'Python', 'python', python),
        ])
        return '<Tabs groupId="lang">\n' + items + '\n</Tabs>'
    return builder

def replace_code_block(text, heading, builder):
    """Find heading, then replace the first ```csharp...``` block after it with builder(csharp)."""
    head_m = re.search(re.escape(heading) + r'\n', text)
    if not head_m:
        print(f'  WARN: heading not found: {heading!r}')
        return text
    after_pos = head_m.end()
    after = text[after_pos:]
    code_m = re.search(r'```csharp\n(.*?)```', after, re.DOTALL)
    if not code_m:
        print(f'  WARN: no csharp block after: {heading!r}')
        return text
    csharp = code_m.group(1).rstrip()
    abs_start = after_pos + code_m.start()
    abs_end = after_pos + code_m.end()
    return text[:abs_start] + builder(csharp) + text[abs_end:]

def process_file(rel, sections, desc):
    """Read file, apply all section replacements, update attribution, write."""
    path = os.path.join(BASE, rel.replace('/', os.sep))
    print(f'Processing {rel}...')
    with open(path, encoding='utf-8') as f:
        text = f.read()
    text = ensure_tabs_import(text)
    for heading, builder in sections:
        text = replace_code_block(text, heading, builder)
    text = update_attribution(text, desc)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Done.')

# ─── Shared SOAP raw-HTTP code for Java / Node.js / Python ───────────────────
# Used across multiple files where the non-C# tabs show raw HTTP SOAP.

SOAP_LOGIN_JAVA = '''\
// Java 11+ — SOAP Login via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""+ ns + "\\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";

var request = HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + "Login\\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(request, BodyHandlers.ofString());
// Extract SessionID from response XML, then use in subsequent calls\
'''

SOAP_LOGIN_NODEJS = '''\
// Node.js 18+ — SOAP Login via raw HTTP
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>
    <ecg:Login>
      <ecg:Email>user@example.com</ecg:Email>
      <ecg:Password>YourPassword1!</ecg:Password>
    </ecg:Login>
  </soap:Body>
</soap:Envelope>`;

const response = await fetch(endpoint, {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    SOAPAction: `"${ns}Login"`
  },
  body: envelope
});
const xml = await response.text();
// Extract SessionID from xml, then use in subsequent calls\
'''

SOAP_LOGIN_PYTHON = '''\
# Python — SOAP Login via raw HTTP
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:ecg="' + ns + '">'
    '<soap:Body><ecg:Login>'
    '<ecg:Email>user@example.com</ecg:Email>'
    '<ecg:Password>YourPassword1!</ecg:Password>'
    '</ecg:Login></soap:Body></soap:Envelope>'
)

resp = requests.post(endpoint, data=envelope.encode(), headers={
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": f'"{ns}Login"'
})
resp.raise_for_status()
# Extract session_id from resp.text, then use in subsequent calls\
'''

# ─── authentication-session-management.md ────────────────────────────────────

AUTH_API_KEY_CURL = '''\
# API key in X-API-Key header — set once, reuse on every request
curl -s \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  https://rest.ecgrid.io/v2/mailboxes/12345 | jq .\
'''

AUTH_API_KEY_JAVA = '''\
// Java 11+ — X-API-Key header on every request
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;

var client = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/12345"))
    .header("X-API-Key", apiKey)
    .GET()
    .build();

var response = client.send(request, BodyHandlers.ofString());
System.out.println(response.body());\
'''

AUTH_API_KEY_NODEJS = '''\
// Node.js 18+ — X-API-Key header on every request
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/mailboxes/12345', {
  headers: { 'X-API-Key': apiKey }
});

const data = await response.json();
console.log(data);\
'''

AUTH_API_KEY_PYTHON = '''\
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

resp = session.get("https://rest.ecgrid.io/v2/mailboxes/12345")
resp.raise_for_status()
print(resp.json())\
'''

AUTH_JWT_CURL = '''\
# Step 1 — login to obtain a Bearer token
TOKEN=$(curl -s -X POST https://rest.ecgrid.io/v2/auth/login \\
  -H "Content-Type: application/json" \\
  -d \'{"email":"user@example.com","password":"YourPassword1!"}\' \\
  | jq -r \'.data.token\')

# Step 2 — use the token in subsequent requests
curl -s -H "Authorization: Bearer $TOKEN" \\
  -X POST https://rest.ecgrid.io/v2/auth/session | jq .\
'''

AUTH_JWT_JAVA = '''\
// Java 11+ — login then use Bearer token
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();

// Step 1 — login
String loginBody = "{\\"email\\":\\"user@example.com\\",\\"password\\":\\"YourPassword1!\\"}";
var loginReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/login"))
    .header("Content-Type", "application/json")
    .POST(BodyPublishers.ofString(loginBody))
    .build();

var loginResp = http.send(loginReq, BodyHandlers.ofString());
// Parse token from loginResp.body() using a JSON library
String token = "...extracted from JSON...";

// Step 2 — use the token
var req = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/session"))
    .header("Authorization", "Bearer " + token)
    .POST(BodyPublishers.noBody())
    .build();
var resp = http.send(req, BodyHandlers.ofString());
System.out.println(resp.body());\
'''

AUTH_JWT_NODEJS = '''\
// Node.js 18+ — login then use Bearer token
// Step 1 — login
const loginResp = await fetch('https://rest.ecgrid.io/v2/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'YourPassword1!' })
});
const loginData = await loginResp.json();
const token = loginData.data.token;

// Step 2 — use the token
const resp = await fetch('https://rest.ecgrid.io/v2/auth/session', {
  method: 'POST',
  headers: { Authorization: `Bearer ${token}` }
});
console.log(await resp.json());\
'''

AUTH_JWT_PYTHON = '''\
import requests

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

# Step 1 — login
login = session.post(
    "https://rest.ecgrid.io/v2/auth/login",
    json={"email": "user@example.com", "password": "YourPassword1!"}
)
login.raise_for_status()
token = login.json()["data"]["token"]

# Step 2 — use the token
session.headers.update({"Authorization": f"Bearer {token}"})
resp = session.post("https://rest.ecgrid.io/v2/auth/session")
print(resp.json())\
'''

AUTH_SOAP_JAVA = '''\
// Java 11+ — SOAP Login → MailboxInfo → Logout
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login
String loginEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";

var loginResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + "Login\\"")
    .POST(BodyPublishers.ofString(loginEnv)).build(), BodyHandlers.ofString());

// Extract sessionId from loginResp.body() using an XML parser
String sessionId = "...extracted...";

// Use sessionId for subsequent calls (e.g., MailboxInfo), then Logout
String logoutEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\">"
    + "<soap:Body><ecg:Logout><ecg:SessionID>" + sessionId + "</ecg:SessionID></ecg:Logout></soap:Body></soap:Envelope>";

http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + "Logout\\"")
    .POST(BodyPublishers.ofString(logoutEnv)).build(), BodyHandlers.ofString());\
'''

AUTH_SOAP_NODEJS = '''\
// Node.js 18+ — SOAP Login → MailboxInfo → Logout
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

async function soapCall(action, body) {
  const env = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>${body}</soap:Body>
</soap:Envelope>`;
  const r = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}${action}"` },
    body: env
  });
  return r.text();
}

// Login — extract SessionID from the XML response
const loginXml = await soapCall('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>YourPassword1!</ecg:Password></ecg:Login>');

const sessionId = '...extracted from loginXml...';

// Use sessionId for subsequent calls, then Logout
await soapCall('Logout', `<ecg:Logout><ecg:SessionID>${sessionId}</ecg:SessionID></ecg:Logout>`);\
'''

AUTH_SOAP_PYTHON = '''\
# Python — SOAP Login → MailboxInfo → Logout
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

def soap_call(action, body):
    env = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:ecg="' + ns + '">'
        '<soap:Body>' + body + '</soap:Body></soap:Envelope>'
    )
    return requests.post(endpoint, data=env.encode(), headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f\'"{ns}{action}"\'
    })

# Login — extract session_id from XML response
login_resp = soap_call("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>YourPassword1!</ecg:Password></ecg:Login>")
session_id = "...extracted from login_resp.text..."

# Use session_id for subsequent calls, then Logout
soap_call("Logout", f"<ecg:Logout><ecg:SessionID>{session_id}</ecg:SessionID></ecg:Logout>")\
'''

# ─── error-handling-troubleshooting.md ───────────────────────────────────────

ERR_REST_CURL = '''\
# Check HTTP status and parse error JSON
RESPONSE=$(curl -s -w "\\n%{http_code}" \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  https://rest.ecgrid.io/v2/mailboxes/99999)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -1)

if [ "$HTTP_CODE" -ge 400 ]; then
  ERROR_CODE=$(echo "$BODY" | jq -r '.errorCode')
  MESSAGE=$(echo "$BODY" | jq -r '.message')
  echo "Error [$HTTP_CODE] [$ERROR_CODE]: $MESSAGE" >&2
fi\
'''

ERR_REST_JAVA = '''\
// Java 11+ — structured error handling for REST API calls
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/99999"))
    .header("X-API-Key", apiKey)
    .GET()
    .build();

var response = http.send(request, BodyHandlers.ofString());
int status = response.statusCode();

if (status >= 400) {
    // Parse error JSON — use a JSON library (e.g. Jackson) in production
    String body = response.body();
    // Extract errorCode and message from body
    System.err.println("Error [" + status + "] from API: " + body);
    // Throw appropriate exception based on status
    if (status == 401) throw new SecurityException("Unauthorized: check API key");
    if (status == 404) throw new java.util.NoSuchElementException("Resource not found");
    throw new RuntimeException("API error " + status + ": " + body);
}\
'''

ERR_REST_NODEJS = '''\
// Node.js 18+ — structured error handling for REST API calls
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/mailboxes/99999', {
  headers: { 'X-API-Key': apiKey }
});

if (!response.ok) {
  let errorCode = 'Unknown', message = response.statusText;
  try {
    const err = await response.json();
    errorCode = err.errorCode ?? errorCode;
    message   = err.message   ?? message;
  } catch { /* non-JSON error body */ }

  const err = new Error(`[${response.status}] [${errorCode}] ${message}`);
  err.status = response.status;
  throw err;
}

const data = await response.json();\
'''

ERR_REST_PYTHON = '''\
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

resp = session.get("https://rest.ecgrid.io/v2/mailboxes/99999")

if not resp.ok:
    try:
        err = resp.json()
        error_code = err.get("errorCode", "Unknown")
        message    = err.get("message", resp.reason)
    except Exception:
        error_code, message = "Unknown", resp.text

    raise Exception(f"[{resp.status_code}] [{error_code}] {message}")

data = resp.json()\
'''

ERR_SOAP_JAVA = '''\
// Java 11+ — detect SOAP faults in the raw XML response
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Build and send a SOAP request
String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\">"
    + "<soap:Body><!-- operation here --></soap:Body></soap:Envelope>";

var response = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + "OperationName\\"")
    .POST(BodyPublishers.ofString(envelope)).build(), BodyHandlers.ofString());

String responseXml = response.body();

// Check for SOAP Fault in response
if (responseXml.contains("<soap:Fault>") || responseXml.contains("<faultstring>")) {
    // Parse faultstring and detail/ECGridOSSOAPErrorCode using an XML parser
    System.err.println("SOAP Fault received: " + responseXml);
    throw new RuntimeException("SOAP Fault: check responseXml for details");
}\
'''

ERR_SOAP_NODEJS = '''\
// Node.js 18+ — detect SOAP faults in the raw XML response
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body><!-- operation here --></soap:Body>
</soap:Envelope>`;

const response = await fetch(endpoint, {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    SOAPAction: `"${ns}OperationName"`
  },
  body: envelope
});

const xml = await response.text();

// Check for SOAP Fault
if (xml.includes('<soap:Fault>') || xml.includes('<faultstring>')) {
  // Use an XML parser to extract faultstring and ECGridOSSOAPErrorCode
  throw new Error(`SOAP Fault received. Raw XML: ${xml.slice(0, 500)}`);
}\
'''

ERR_SOAP_PYTHON = '''\
# Python — detect SOAP faults in the raw XML response
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:ecg="' + ns + '">'
    '<soap:Body><!-- operation here --></soap:Body></soap:Envelope>'
)

resp = requests.post(endpoint, data=envelope.encode(), headers={
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": f\'"{ns}OperationName"\'
})
resp.raise_for_status()

# Check for SOAP Fault
if "<soap:Fault>" in resp.text or "<faultstring>" in resp.text:
    # Use xml.etree.ElementTree to parse faultstring and ECGridOSSOAPErrorCode
    raise Exception(f"SOAP Fault received: {resp.text[:500]}")\
'''

ERR_RETRY_CURL = '''\
#!/usr/bin/env bash
# Exponential backoff retry for REST API calls
URL="https://rest.ecgrid.io/v2/parcels/pending-inbox-list"
MAX_ATTEMPTS=3
DELAY=1

for attempt in $(seq 1 $MAX_ATTEMPTS); do
  HTTP_CODE=$(curl -s -o /tmp/ecgrid_resp.json -w "%{http_code}" \\
    -X POST "$URL" \\
    -H "X-API-Key: $ECGRID_API_KEY" \\
    -H "Content-Type: application/json" \\
    -d \'{"mailboxId":0,"pageNo":1,"recordsPerPage":25}\')

  if [ "$HTTP_CODE" -eq 200 ]; then
    cat /tmp/ecgrid_resp.json
    exit 0
  fi

  if [ "$HTTP_CODE" -ne 429 ] && [ "$HTTP_CODE" -lt 500 ]; then
    echo "Non-retryable error: $HTTP_CODE" >&2
    cat /tmp/ecgrid_resp.json >&2
    exit 1
  fi

  echo "Attempt $attempt/$MAX_ATTEMPTS failed ($HTTP_CODE). Retrying in ${DELAY}s..." >&2
  sleep $DELAY
  DELAY=$((DELAY * 2))
done

echo "All $MAX_ATTEMPTS attempts failed." >&2
exit 1\
'''

ERR_RETRY_JAVA = '''\
// Java 11+ — exponential backoff retry
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;

static HttpResponse<String> sendWithRetry(
    HttpClient http, String url, String body, String apiKey,
    int maxAttempts) throws Exception {

    long delayMs = 1000;
    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
        var request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/json")
            .header("X-API-Key", apiKey)
            .POST(BodyPublishers.ofString(body))
            .build();

        var response = http.send(request, BodyHandlers.ofString());
        int status = response.statusCode();
        boolean isTransient = status == 429 || status >= 500;

        if (!isTransient || attempt == maxAttempts) return response;

        Thread.sleep(delayMs);
        delayMs *= 2; // double the delay each attempt
    }
    throw new IllegalStateException("Retry loop exited without returning.");
}\
'''

ERR_RETRY_NODEJS = '''\
// Node.js 18+ — exponential backoff retry
async function fetchWithRetry(url, options, maxAttempts = 3) {
  let delay = 1000;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const response = await fetch(url, options);
    const isTransient = response.status === 429 || response.status >= 500;

    if (!isTransient || attempt === maxAttempts) return response;

    // Honour Retry-After header if provided
    const retryAfter = response.headers.get('Retry-After');
    const waitMs = retryAfter ? parseInt(retryAfter, 10) * 1000 : delay;

    await new Promise(resolve => setTimeout(resolve, waitMs));
    delay *= 2;
  }
}

// Usage
const response = await fetchWithRetry(
  'https://rest.ecgrid.io/v2/parcels/pending-inbox-list',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-API-Key': process.env.ECGRID_API_KEY },
    body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
  }
);\
'''

ERR_RETRY_PYTHON = '''\
# Python — exponential backoff retry
import time, os, requests

def post_with_retry(url, payload, api_key, max_attempts=3):
    delay = 1.0
    for attempt in range(1, max_attempts + 1):
        resp = requests.post(url,
            json=payload,
            headers={"X-API-Key": api_key, "Content-Type": "application/json"})

        is_transient = resp.status_code == 429 or resp.status_code >= 500
        if not is_transient or attempt == max_attempts:
            return resp

        retry_after = resp.headers.get("Retry-After")
        wait = float(retry_after) if retry_after else delay
        time.sleep(wait)
        delay *= 2
    raise RuntimeError("Retry loop exited without returning.")

# Usage
response = post_with_retry(
    "https://rest.ecgrid.io/v2/parcels/pending-inbox-list",
    {"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25},
    os.environ["ECGRID_API_KEY"]
)\
'''

# ─── connecting-via-soap.md ───────────────────────────────────────────────────
# All three options are SOAP — show Java/Node.js/Python as raw HTTP SOAP

SOAP_CONNECT_JAVA = '''\
// Java 11+ — manual SOAP envelope construction and dispatch
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Build the SOAP envelope for any method
String methodName = "Login";
String soapBody = "<ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login>";

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\">"
    + "<soap:Body>" + soapBody + "</soap:Body></soap:Envelope>";

var request = HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + methodName + "\\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // parse XML to extract result\
'''

SOAP_CONNECT_NODEJS = '''\
// Node.js 18+ — manual SOAP envelope construction and dispatch
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

async function sendSoap(methodName, soapBody) {
  const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>${soapBody}</soap:Body>
</soap:Envelope>`;

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/xml; charset=utf-8',
      SOAPAction: `"${ns}${methodName}"`
    },
    body: envelope
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.text(); // parse XML to extract result
}

// Example: Login
const xml = await sendSoap('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>YourPassword1!</ecg:Password></ecg:Login>');\
'''

SOAP_CONNECT_PYTHON = '''\
# Python — manual SOAP envelope construction and dispatch
import requests

ENDPOINT = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
NS = "http://www.ecgridos.net/"

def send_soap(method_name, soap_body):
    envelope = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:ecg="' + NS + '">'
        '<soap:Body>' + soap_body + '</soap:Body></soap:Envelope>'
    )
    resp = requests.post(ENDPOINT, data=envelope.encode(), headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f\'"{NS}{method_name}"\'
    })
    resp.raise_for_status()
    return resp.text  # parse XML to extract result

# Example: Login
xml = send_soap("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>YourPassword1!</ecg:Password></ecg:Login>")\
'''

# svcutil option — note C# uses generated proxy; other langs use raw HTTP
SOAP_SVCUTIL_JAVA = '''\
// Java 11+ — no svcutil equivalent; use raw HTTP SOAP
// For a typed approach in Java, consider JAX-WS with wsimport:
//   wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL
//
// Raw HTTP approach (same as Option 1):
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login envelope
String loginEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";

var loginResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + "Login\\"")
    .POST(BodyPublishers.ofString(loginEnv)).build(), BodyHandlers.ofString());

// Extract sessionId and use it in subsequent calls\
'''

SOAP_SVCUTIL_NODEJS = '''\
// Node.js 18+ — no svcutil equivalent; use raw HTTP SOAP
// For a typed approach in Node.js, consider the 'soap' npm package:
//   npm install soap
//
// Raw HTTP approach (same as Option 1):
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

const loginEnv = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>
    <ecg:Login>
      <ecg:Email>user@example.com</ecg:Email>
      <ecg:Password>YourPassword1!</ecg:Password>
    </ecg:Login>
  </soap:Body>
</soap:Envelope>`;

const loginResp = await fetch(endpoint, {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}Login"` },
  body: loginEnv
});
const xml = await loginResp.text();
// Extract sessionId from xml and use in subsequent calls\
'''

SOAP_SVCUTIL_PYTHON = '''\
# Python — no svcutil equivalent; use raw HTTP SOAP
# For a typed approach in Python, consider the 'zeep' library:
#   pip install zeep
#   from zeep import Client
#   client = Client("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL")
#
# Raw HTTP approach (same as Option 1):
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

login_env = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:ecg="' + ns + '">'
    '<soap:Body><ecg:Login>'
    '<ecg:Email>user@example.com</ecg:Email>'
    '<ecg:Password>YourPassword1!</ecg:Password>'
    '</ecg:Login></soap:Body></soap:Envelope>'
)
login_resp = requests.post(endpoint, data=login_env.encode(), headers={
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": f\'"{ns}Login"\'
})
# Extract session_id from login_resp.text and use in subsequent calls\
'''

# CoreWCF — show raw HTTP as the cross-language equivalent
SOAP_COREWCF_JAVA   = SOAP_SVCUTIL_JAVA.replace("no svcutil", "no CoreWCF").replace("wsimport", "wsimport")
SOAP_COREWCF_NODEJS = SOAP_SVCUTIL_NODEJS.replace("no svcutil", "no CoreWCF").replace("soap' npm", "soap' npm")
SOAP_COREWCF_PYTHON = SOAP_SVCUTIL_PYTHON.replace("no svcutil", "no CoreWCF").replace("zeep", "zeep")

# ─── migrating-soap-to-rest.md ────────────────────────────────────────────────

MIG_SOAP_JAVA = '''\
// Java 11+ — SOAP parcel download workflow (before migration)
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login — extract sessionId from XML response
String loginEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\"><soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>pass</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";
// Send login, extract sessionId from response XML...
String sessionId = "...";

// ParcelInBox — extract parcel IDs from XML response
String inboxEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\"><soap:Body><ecg:ParcelInBox>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "</ecg:ParcelInBox></soap:Body></soap:Envelope>";
// Send inbox request, parse parcel list from XML...

// For each parcel: ParcelDownload → save file → ParcelDownloadConfirm → Logout\
'''

MIG_SOAP_NODEJS = '''\
// Node.js 18+ — SOAP parcel download workflow (before migration)
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

async function soapCall(action, body) {
  const env = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>${body}</soap:Body>
</soap:Envelope>`;
  const r = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}${action}"` },
    body: env
  });
  return r.text();
}

// Login — extract sessionId from XML
const loginXml = await soapCall('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>pass</ecg:Password></ecg:Login>');
const sessionId = '...extracted from loginXml...';

// ParcelInBox — extract parcel IDs from XML
const inboxXml = await soapCall('ParcelInBox',
  `<ecg:ParcelInBox><ecg:SessionID>${sessionId}</ecg:SessionID></ecg:ParcelInBox>`);

// For each parcel: ParcelDownload → save → ParcelDownloadConfirm → Logout\
'''

MIG_SOAP_PYTHON = '''\
# Python — SOAP parcel download workflow (before migration)
import requests, base64

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

def soap_call(action, body):
    env = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:ecg="' + ns + '">'
        '<soap:Body>' + body + '</soap:Body></soap:Envelope>'
    )
    return requests.post(endpoint, data=env.encode(), headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f\'"{ns}{action}"\'
    })

# Login — extract session_id from XML
login = soap_call("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>pass</ecg:Password></ecg:Login>")
session_id = "...extracted from login.text..."

# ParcelInBox, ParcelDownload, ParcelDownloadConfirm, Logout follow the same pattern\
'''

MIG_REST_CURL = '''\
# Step 1 — get inbox list
curl -s -X POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  -d \'{"mailboxId":0,"pageNo":1,"recordsPerPage":25}\' | jq .

# Step 2 — download a parcel (replace PARCEL_ID)
curl -s -X POST https://rest.ecgrid.io/v2/parcels/download \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  -d "{\\"parcelID\\":$PARCEL_ID}" -o "parcel-$PARCEL_ID.edi"

# Step 3 — confirm receipt
curl -s -X POST https://rest.ecgrid.io/v2/parcels/confirm \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  -d "{\\"parcelID\\":$PARCEL_ID}"\
'''

MIG_REST_JAVA = '''\
// Java 11+ — REST parcel download workflow (after migration)
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.Files;
import java.nio.file.Path;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String base = "https://rest.ecgrid.io";

// Step 1 — get inbox list
var inboxResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/pending-inbox-list"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"mailboxId\\":0,\\"pageNo\\":1,\\"recordsPerPage\\":25}"))
    .build(), BodyHandlers.ofString());
// Parse parcel list from inboxResp.body() and iterate...

// Step 2 — download (for each parcelId)
long parcelId = 12345L;
var downloadResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/download"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"parcelID\\":" + parcelId + "}"))
    .build(), BodyHandlers.ofByteArray());
Files.write(Path.of("parcel-" + parcelId + ".edi"), downloadResp.body());

// Step 3 — confirm receipt
http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/confirm"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"parcelID\\":" + parcelId + "}"))
    .build(), BodyHandlers.discarding());\
'''

MIG_REST_NODEJS = '''\
// Node.js 18+ — REST parcel download workflow (after migration)
const apiKey = process.env.ECGRID_API_KEY;
const base = 'https://rest.ecgrid.io';
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — get inbox list
const inboxResp = await fetch(`${base}/v2/parcels/pending-inbox-list`, {
  method: 'POST', headers,
  body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
});
const inbox = await inboxResp.json();

for (const parcel of inbox.data ?? []) {
  // Step 2 — download
  const downloadResp = await fetch(`${base}/v2/parcels/download`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
  const bytes = Buffer.from(await downloadResp.arrayBuffer());
  require('fs').writeFileSync(`parcel-${parcel.parcelId}.edi`, bytes);

  // Step 3 — confirm receipt
  await fetch(`${base}/v2/parcels/confirm`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
}\
'''

MIG_REST_PYTHON = '''\
# Python — REST parcel download workflow (after migration)
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})
base = "https://rest.ecgrid.io"

# Step 1 — get inbox list
inbox = session.post(f"{base}/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25}).json()

for parcel in inbox.get("data", []):
    parcel_id = parcel["parcelId"]

    # Step 2 — download
    data = session.post(f"{base}/v2/parcels/download",
        json={"parcelID": parcel_id}).content
    with open(f"parcel-{parcel_id}.edi", "wb") as f:
        f.write(data)

    # Step 3 — confirm receipt
    session.post(f"{base}/v2/parcels/confirm", json={"parcelID": parcel_id})\
'''

# ─── rest-console.md ─────────────────────────────────────────────────────────

CONSOLE_SETUP_CURL = '''\
# cURL passes the API key as a header on every request — no setup phase needed
# Export the key once in your shell session
export ECGRID_API_KEY="your-api-key-here"

# Every request uses it like this:
curl -s \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  https://rest.ecgrid.io/v2/auth/version | jq .\
'''

CONSOLE_SETUP_JAVA = '''\
// Java 11+ — reusable HttpClient with API key applied to every request
// Use a request factory helper since Java's HttpClient doesn't support default headers
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;

class EcGridClient {
    private final HttpClient http = HttpClient.newHttpClient();
    private final String apiKey;
    private final String baseUrl;

    EcGridClient(String apiKey, String baseUrl) {
        this.apiKey   = apiKey;
        this.baseUrl  = baseUrl;
    }

    HttpRequest.Builder request(String path) {
        return HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + path))
            .header("Content-Type", "application/json")
            .header("X-API-Key", apiKey);
    }

    // Usage: http.send(client.request("/v2/auth/version").GET().build(), BodyHandlers.ofString())
}\
'''

CONSOLE_SETUP_NODEJS = '''\
// Node.js 18+ — reusable fetch wrapper with API key header
const BASE_URL = 'https://rest.ecgrid.io';
const API_KEY  = process.env.ECGRID_API_KEY;

function ecgridFetch(path, options = {}) {
  return fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY,
      ...options.headers
    }
  });
}

// Usage: const resp = await ecgridFetch('/v2/auth/version');\
'''

CONSOLE_SETUP_PYTHON = '''\
# Python — requests.Session with API key applied to every request
import os, requests

api_key = os.environ["ECGRID_API_KEY"]

session = requests.Session()
session.headers.update({
    "X-API-Key": api_key,
    "Content-Type": "application/json"
})
session.base_url = "https://rest.ecgrid.io"

# Usage: resp = session.get(session.base_url + "/v2/auth/version")\
'''

CONSOLE_INBOX_CURL = '''\
# Check inbox and print parcel IDs
curl -s -X POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  -d \'{"mailboxId":0,"pageNo":1,"recordsPerPage":25}\' | jq \'.data[].parcelId\'

# Download a specific parcel (replace 12345)
curl -s -X POST https://rest.ecgrid.io/v2/parcels/download \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  -d \'{"parcelID":12345}\' -o parcel-12345.edi

# Confirm receipt
curl -s -X POST https://rest.ecgrid.io/v2/parcels/confirm \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  -d \'{"parcelID":12345}\'\
'''

CONSOLE_INBOX_JAVA = '''\
// Java 11+ — inbox check and download loop
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String base = "https://rest.ecgrid.io";

// Get inbox list
var inboxResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/pending-inbox-list"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"mailboxId\\":0,\\"pageNo\\":1,\\"recordsPerPage\\":25}"))
    .build(), BodyHandlers.ofString());
// Parse parcel list from inboxResp.body() and iterate...

// For each parcel — download
long parcelId = 12345L;
var downloadResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/download"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"parcelID\\":" + parcelId + "}"))
    .build(), BodyHandlers.ofByteArray());
Files.write(Path.of("parcel-" + parcelId + ".edi"), downloadResp.body());

// Confirm receipt
http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/confirm"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"parcelID\\":" + parcelId + "}"))
    .build(), BodyHandlers.discarding());\
'''

CONSOLE_INBOX_NODEJS = '''\
// Node.js 18+ — inbox check and download loop
import fs from 'node:fs/promises';

const apiKey = process.env.ECGRID_API_KEY;
const base = 'https://rest.ecgrid.io';
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Get inbox list
const inboxResp = await fetch(`${base}/v2/parcels/pending-inbox-list`, {
  method: 'POST', headers,
  body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
});
const inbox = await inboxResp.json();

for (const parcel of inbox.data ?? []) {
  // Download parcel
  const dlResp = await fetch(`${base}/v2/parcels/download`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
  const bytes = Buffer.from(await dlResp.arrayBuffer());
  await fs.writeFile(`parcel-${parcel.parcelId}.edi`, bytes);

  // Confirm receipt
  await fetch(`${base}/v2/parcels/confirm`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
  console.log(`Parcel ${parcel.parcelId} saved and confirmed.`);
}\
'''

CONSOLE_INBOX_PYTHON = '''\
# Python — inbox check and download loop
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})
base = "https://rest.ecgrid.io"

inbox = session.post(f"{base}/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25}).json()

for parcel in inbox.get("data", []):
    parcel_id = parcel["parcelId"]

    # Download
    data = session.post(f"{base}/v2/parcels/download",
        json={"parcelID": parcel_id}).content
    with open(f"parcel-{parcel_id}.edi", "wb") as f:
        f.write(data)

    # Confirm receipt
    session.post(f"{base}/v2/parcels/confirm", json={"parcelID": parcel_id})
    print(f"Parcel {parcel_id} saved and confirmed.")\
'''

CONSOLE_UPLOAD_CURL = '''\
# Upload an outbound EDI file
curl -s -X POST https://rest.ecgrid.io/v2/parcels/upload \\
  -H "X-API-Key: $ECGRID_API_KEY" \\
  -H "Content-Type: application/octet-stream" \\
  --data-binary @outbound.edi | jq .\
'''

CONSOLE_UPLOAD_JAVA = '''\
// Java 11+ — upload an outbound EDI file
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

byte[] fileBytes = Files.readAllBytes(Path.of("outbound.edi"));

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/upload"))
    .header("Content-Type", "application/octet-stream")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofByteArray(fileBytes))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // parse JSON for parcel ID\
'''

CONSOLE_UPLOAD_NODEJS = '''\
// Node.js 18+ — upload an outbound EDI file
import fs from 'node:fs/promises';

const apiKey = process.env.ECGRID_API_KEY;
const fileBytes = await fs.readFile('outbound.edi');

const response = await fetch('https://rest.ecgrid.io/v2/parcels/upload', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/octet-stream',
    'X-API-Key': apiKey
  },
  body: fileBytes
});

const result = await response.json();
console.log('Uploaded parcel ID:', result.data?.parcelId);\
'''

CONSOLE_UPLOAD_PYTHON = '''\
# Python — upload an outbound EDI file
import os, requests

api_key = os.environ["ECGRID_API_KEY"]

with open("outbound.edi", "rb") as f:
    file_bytes = f.read()

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/upload",
    data=file_bytes,
    headers={
        "Content-Type": "application/octet-stream",
        "X-API-Key": api_key
    }
)
resp.raise_for_status()
print("Uploaded parcel ID:", resp.json()["data"]["parcelId"])\
'''

# ─── soap-httpclient.md ───────────────────────────────────────────────────────

SOAP_ENV_BUILD_JAVA = '''\
// Java 11+ — build a SOAP 1.1 envelope for any ECGridOS method
String buildEnvelope(String methodName, String ns, java.util.Map<String, String> params) {
    var sb = new StringBuilder();
    sb.append("<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>");
    sb.append("<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" ");
    sb.append("xmlns:ecg=\\"").append(ns).append("\\">");
    sb.append("<soap:Body><ecg:").append(methodName).append(">");
    for (var entry : params.entrySet()) {
        sb.append("<ecg:").append(entry.getKey()).append(">");
        sb.append(entry.getValue());
        sb.append("</ecg:").append(entry.getKey()).append(">");
    }
    sb.append("</ecg:").append(methodName).append(">");
    sb.append("</soap:Body></soap:Envelope>");
    return sb.toString();
}

// Example: build a Login envelope
var loginEnv = buildEnvelope("Login", "http://www.ecgridos.net/",
    java.util.Map.of("Email", "user@example.com", "Password", "YourPassword1!"));\
'''

SOAP_ENV_BUILD_NODEJS = '''\
// Node.js 18+ — build a SOAP 1.1 envelope for any ECGridOS method
function buildEnvelope(methodName, ns, params) {
  const paramXml = Object.entries(params)
    .map(([k, v]) => `<ecg:${k}>${v}</ecg:${k}>`)
    .join('');

  return `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>
    <ecg:${methodName}>
      ${paramXml}
    </ecg:${methodName}>
  </soap:Body>
</soap:Envelope>`;
}

// Example: build a Login envelope
const loginEnv = buildEnvelope('Login', 'http://www.ecgridos.net/', {
  Email: 'user@example.com',
  Password: 'YourPassword1!'
});\
'''

SOAP_ENV_BUILD_PYTHON = '''\
# Python — build a SOAP 1.1 envelope for any ECGridOS method
def build_envelope(method_name, ns, **params):
    param_xml = "".join(
        f"<ecg:{k}>{v}</ecg:{k}>" for k, v in params.items()
    )
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        f'xmlns:ecg="{ns}">'
        f'<soap:Body><ecg:{method_name}>{param_xml}</ecg:{method_name}></soap:Body>'
        '</soap:Envelope>'
    )

# Example: build a Login envelope
ns = "http://www.ecgridos.net/"
login_env = build_envelope("Login", ns,
    Email="user@example.com",
    Password="YourPassword1!")\
'''

SOAP_SEND_JAVA = '''\
// Java 11+ — send a SOAP request and return the response body
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

static final String ECG_NS       = "http://www.ecgridos.net/";
static final String ENDPOINT_URL = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";

String postSoap(HttpClient http, String methodName, String envelope) throws Exception {
    var request = HttpRequest.newBuilder()
        .uri(URI.create(ENDPOINT_URL))
        .header("Content-Type", "text/xml; charset=utf-8")
        .header("SOAPAction", "\\"" + ECG_NS + methodName + "\\"")
        .POST(BodyPublishers.ofString(envelope))
        .build();

    var response = http.send(request, BodyHandlers.ofString());
    if (response.statusCode() >= 400)
        throw new RuntimeException("SOAP HTTP error: " + response.statusCode());

    return response.body(); // parse XML for the result element
}\
'''

SOAP_SEND_NODEJS = '''\
// Node.js 18+ — send a SOAP request and return the response XML
const ECG_NS       = 'http://www.ecgridos.net/';
const ENDPOINT_URL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';

async function postSoap(methodName, envelope) {
  const response = await fetch(ENDPOINT_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/xml; charset=utf-8',
      SOAPAction: `"${ECG_NS}${methodName}"`
    },
    body: envelope
  });

  if (!response.ok)
    throw new Error(`SOAP HTTP error: ${response.status}`);

  return response.text(); // parse XML for the result element
}\
'''

SOAP_SEND_PYTHON = '''\
# Python — send a SOAP request and return the response XML
import requests

ECG_NS       = "http://www.ecgridos.net/"
ENDPOINT_URL = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"

def post_soap(method_name, envelope):
    resp = requests.post(ENDPOINT_URL,
        data=envelope.encode("utf-8"),
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f\'"{ECG_NS}{method_name}"\'
        })
    resp.raise_for_status()
    return resp.text  # parse XML for the result element\
'''

SOAP_SESSION_JAVA = '''\
// Java 11+ — full SOAP session lifecycle: Login → ParcelInBox → Download → Confirm → Logout
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login
String loginEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email><ecg:Password>pass</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";
var loginResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + "Login\\"")
    .POST(BodyPublishers.ofString(loginEnv)).build(), BodyHandlers.ofString());
// Extract sessionId from loginResp.body() using an XML parser (e.g. javax.xml)
String sessionId = "...";

// ParcelInBox — iterate results and download/confirm each
// ... build envelopes for ParcelInBox, ParcelDownload, ParcelDownloadConfirm

// Logout
String logoutEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\" xmlns:ecg=\\""
    + ns + "\\">"
    + "<soap:Body><ecg:Logout><ecg:SessionID>" + sessionId + "</ecg:SessionID></ecg:Logout>"
    + "</soap:Body></soap:Envelope>";
http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"" + ns + "Logout\\"")
    .POST(BodyPublishers.ofString(logoutEnv)).build(), BodyHandlers.discarding());\
'''

SOAP_SESSION_NODEJS = '''\
// Node.js 18+ — full SOAP session lifecycle: Login → ParcelInBox → Download → Confirm → Logout
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

async function soapCall(action, body) {
  const env = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>${body}</soap:Body>
</soap:Envelope>`;
  const r = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}${action}"` },
    body: env
  });
  if (!r.ok) throw new Error(`SOAP HTTP ${r.status}`);
  return r.text();
}

// Login — extract sessionId from XML
const loginXml = await soapCall('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>pass</ecg:Password></ecg:Login>');
const sessionId = '...extracted from loginXml...';

// ParcelInBox → ParcelDownload → ParcelDownloadConfirm for each parcel
// (build body strings and call soapCall for each)

// Logout
await soapCall('Logout',
  `<ecg:Logout><ecg:SessionID>${sessionId}</ecg:SessionID></ecg:Logout>`);\
'''

SOAP_SESSION_PYTHON = '''\
# Python — full SOAP session lifecycle: Login → ParcelInBox → Download → Confirm → Logout
import requests

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

def soap_call(action, body):
    env = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:ecg="' + ns + '">'
        '<soap:Body>' + body + '</soap:Body></soap:Envelope>'
    )
    resp = requests.post(endpoint, data=env.encode(), headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f\'"{ns}{action}"\'
    })
    resp.raise_for_status()
    return resp.text

# Login — extract session_id from XML
login_xml = soap_call("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>pass</ecg:Password></ecg:Login>")
session_id = "...extracted from login_xml..."

# ParcelInBox → ParcelDownload → ParcelDownloadConfirm for each parcel
# (build body strings and call soap_call for each)

# Logout
soap_call("Logout",
    f"<ecg:Logout><ecg:SessionID>{session_id}</ecg:SessionID></ecg:Logout>")\
'''

# ─── Main ─────────────────────────────────────────────────────────────────────

FILES = [
    (
        "guides/authentication-session-management.md",
        [
            ("### REST C# Example — API Key",
             rest_block(AUTH_API_KEY_CURL, AUTH_API_KEY_JAVA, AUTH_API_KEY_NODEJS, AUTH_API_KEY_PYTHON)),
            ("### REST C# Example — Bearer JWT",
             rest_block(AUTH_JWT_CURL, AUTH_JWT_JAVA, AUTH_JWT_NODEJS, AUTH_JWT_PYTHON)),
            ("### SOAP C# Example — Full Session Lifecycle",
             soap_block(AUTH_SOAP_JAVA, AUTH_SOAP_NODEJS, AUTH_SOAP_PYTHON)),
        ],
        "Add multi-language code tabs to REST and SOAP auth examples"
    ),
    (
        "guides/error-handling-troubleshooting.md",
        [
            ("### REST C# Exception Handling",
             rest_block(ERR_REST_CURL, ERR_REST_JAVA, ERR_REST_NODEJS, ERR_REST_PYTHON)),
            ("### SOAP C# Exception Handling",
             soap_block(ERR_SOAP_JAVA, ERR_SOAP_NODEJS, ERR_SOAP_PYTHON)),
            ("### C# Retry with Exponential Backoff",
             rest_block(ERR_RETRY_CURL, ERR_RETRY_JAVA, ERR_RETRY_NODEJS, ERR_RETRY_PYTHON)),
        ],
        "Add multi-language code tabs to error handling and retry examples"
    ),
    (
        "guides/connecting-via-soap.md",
        [
            ("### Complete C# example",
             soap_block(SOAP_CONNECT_JAVA, SOAP_CONNECT_NODEJS, SOAP_CONNECT_PYTHON)),
            ("### Use the generated proxy",
             soap_block(SOAP_SVCUTIL_JAVA, SOAP_SVCUTIL_NODEJS, SOAP_SVCUTIL_PYTHON)),
            ("### Configure the channel",
             soap_block(SOAP_COREWCF_JAVA, SOAP_COREWCF_NODEJS, SOAP_COREWCF_PYTHON)),
        ],
        "Add multi-language code tabs to SOAP connection options"
    ),
    (
        "guides/migrating-soap-to-rest.md",
        [
            ("### SOAP — before",
             soap_block(MIG_SOAP_JAVA, MIG_SOAP_NODEJS, MIG_SOAP_PYTHON)),
            ("### REST — after",
             rest_block(MIG_REST_CURL, MIG_REST_JAVA, MIG_REST_NODEJS, MIG_REST_PYTHON)),
        ],
        "Add multi-language code tabs to SOAP-to-REST migration examples"
    ),
    (
        "code-samples/rest-console.md",
        [
            ("### HttpClient Setup",
             rest_block(CONSOLE_SETUP_CURL, CONSOLE_SETUP_JAVA, CONSOLE_SETUP_NODEJS, CONSOLE_SETUP_PYTHON)),
            ("### Inbox Check and Download Loop",
             rest_block(CONSOLE_INBOX_CURL, CONSOLE_INBOX_JAVA, CONSOLE_INBOX_NODEJS, CONSOLE_INBOX_PYTHON)),
            ("### Upload",
             rest_block(CONSOLE_UPLOAD_CURL, CONSOLE_UPLOAD_JAVA, CONSOLE_UPLOAD_NODEJS, CONSOLE_UPLOAD_PYTHON)),
        ],
        "Add multi-language code tabs to REST console sample key patterns"
    ),
    (
        "code-samples/soap-httpclient.md",
        [
            ("### SOAP Envelope Construction",
             soap_block(SOAP_ENV_BUILD_JAVA, SOAP_ENV_BUILD_NODEJS, SOAP_ENV_BUILD_PYTHON)),
            ("### Sending a SOAP Request",
             soap_block(SOAP_SEND_JAVA, SOAP_SEND_NODEJS, SOAP_SEND_PYTHON)),
            ("### Session Lifecycle",
             soap_block(SOAP_SESSION_JAVA, SOAP_SESSION_NODEJS, SOAP_SESSION_PYTHON)),
        ],
        "Add multi-language code tabs to SOAP HttpClient sample key patterns"
    ),
]

if __name__ == '__main__':
    ok = 0
    for rel, sections, desc in FILES:
        process_file(rel, sections, desc)
        ok += 1
    print(f'\nDone: {ok}/{len(FILES)} files processed.')
