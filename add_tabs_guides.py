#!/usr/bin/env python3
"""
add_tabs_guides.py
Add multi-language code tabs to common-operations/*.md files.
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

def rest_tabs(curl, csharp, java, nodejs, python):
    items = '\n'.join([
        _tab('curl', 'cURL', 'bash', curl),
        _tab('csharp', 'C#', 'csharp', csharp, True),
        _tab('java', 'Java', 'java', java),
        _tab('nodejs', 'Node.js', 'javascript', nodejs),
        _tab('python', 'Python', 'python', python),
    ])
    return '### Code Examples\n\n<Tabs groupId="lang">\n' + items + '\n</Tabs>'

def soap_tabs(csharp, java, nodejs, python):
    items = '\n'.join([
        _tab('csharp', 'C#', 'csharp', csharp, True),
        _tab('java', 'Java', 'java', java),
        _tab('nodejs', 'Node.js', 'javascript', nodejs),
        _tab('python', 'Python', 'python', python),
    ])
    return '### Code Examples\n\n<Tabs groupId="lang">\n' + items + '\n</Tabs>'

def replace_section(text, heading, builder):
    pat = re.escape(heading) + r'\n\n```csharp\n(.*?)```'
    m = re.search(pat, text, re.DOTALL)
    if not m:
        print(f'  WARN: not found: {heading!r}')
        return text, None
    csharp = m.group(1).rstrip()
    return text[:m.start()] + builder(csharp) + text[m.end():], csharp

def process(rel, rest_h, rest_x, soap_h, soap_x, desc):
    path = os.path.join(BASE, rel.replace('/', os.sep))
    print(f'Processing {rel}...')
    with open(path, encoding='utf-8') as f:
        text = f.read()
    text = ensure_tabs_import(text)
    soap_pos = text.find('\n## SOAP\n')
    if soap_pos == -1:
        soap_pos = len(text)
    rest_text = text[:soap_pos]
    soap_text = text[soap_pos:]
    rest_text, _ = replace_section(rest_text, rest_h,
        lambda cs: rest_tabs(rest_x['curl'], cs, rest_x['java'], rest_x['nodejs'], rest_x['python']))
    if soap_h and soap_x:
        soap_text, _ = replace_section(soap_text, soap_h,
            lambda cs: soap_tabs(cs, soap_x['java'], soap_x['nodejs'], soap_x['python']))
    text = update_attribution(rest_text + soap_text, desc)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('  Done.')

# ─── poll-inbound-files.md ────────────────────────────────────────────────────

POLL_REST = {
'curl': r'''curl -s -X POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"mailboxId":0,"pageNo":1,"recordsPerPage":25}' | jq .''',

'java': '''// Java 11+ — poll inbox for ready parcels
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var client = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String body = "{\\"mailboxId\\":0,\\"pageNo\\":1,\\"recordsPerPage\\":25}";

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/pending-inbox-list"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = client.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // parse JSON to get parcel list''',

'nodejs': '''// Node.js 18+ — poll inbox for ready parcels
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/parcels/pending-inbox-list', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
});

const result = await response.json();
for (const parcel of result.data ?? []) {
  console.log(`ParcelID: ${parcel.parcelId} — ${parcel.fileName}`);
}''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

resp = session.post(
    "https://rest.ecgrid.io/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25}
)
resp.raise_for_status()

for parcel in resp.json().get("data", []):
    print(f"ParcelID: {parcel[\'parcelId\']} — {parcel[\'fileName\']}")''',
}

POLL_SOAP = {
'java': '''// Java 11+ — SOAP ParcelInBox via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID"; // obtain from Login

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:ParcelInBox>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>"
    + "<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>"
    + "<ecg:Status>InBoxReady</ecg:Status>"
    + "<ecg:BeginDate>0001-01-01T00:00:00</ecg:BeginDate>"
    + "<ecg:EndDate>9999-12-31T00:00:00</ecg:EndDate>"
    + "<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>25</ecg:RecordsPerPage>"
    + "</ecg:ParcelInBox></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/ParcelInBox\\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, BodyHandlers.ofString());
System.out.println(response.body()); // parse ParcelIDInfo elements from XML''',

'nodejs': r'''// Node.js 18+ — SOAP ParcelInBox via raw HTTP
const sessionId = 'YOUR_SESSION_ID'; // obtain from Login

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelInBox>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>
    <ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>
    <ecg:Status>InBoxReady</ecg:Status>
    <ecg:BeginDate>0001-01-01T00:00:00</ecg:BeginDate>
    <ecg:EndDate>9999-12-31T00:00:00</ecg:EndDate>
    <ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>25</ecg:RecordsPerPage>
  </ecg:ParcelInBox></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelInBox"'
  },
  body: envelope
});
const xml = await response.text();
console.log(xml); // parse ParcelIDInfo elements from XML''',

'python': r'''import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelInBox>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>'
    '<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>'
    '<ecg:Status>InBoxReady</ecg:Status>'
    '<ecg:BeginDate>0001-01-01T00:00:00</ecg:BeginDate>'
    '<ecg:EndDate>9999-12-31T00:00:00</ecg:EndDate>'
    '<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>25</ecg:RecordsPerPage>'
    '</ecg:ParcelInBox></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelInBox"'}
)
resp.raise_for_status()
print(resp.text)  # parse ParcelIDInfo elements from XML''',
}

# ─── download-a-file.md ───────────────────────────────────────────────────────

DOWNLOAD_REST = {
'curl': r'''curl -s -X POST https://rest.ecgrid.io/v2/parcels/download \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"parcelId":98765}' \
  | jq -r '.data.content' | base64 -d > parcel-98765.edi''',

'java': '''// Java 11+ — download a parcel and decode Base64 content
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
long parcelId = 98765L;

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/download"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"parcelId\\":" + parcelId + "}"))
    .build();

var response = http.send(request, HttpResponse.BodyHandlers.ofString());
JsonNode root = new ObjectMapper().readTree(response.body());
String base64 = root.path("data").path("content").asText();
String fileName = root.path("data").path("fileName").asText("parcel.edi");

byte[] bytes = Base64.getDecoder().decode(base64);
Files.write(Path.of(fileName), bytes);
System.out.println("Saved " + fileName + " (" + bytes.length + " bytes)");''',

'nodejs': '''// Node.js 18+ — download a parcel and save to disk
import { writeFile } from 'fs/promises';

const apiKey = process.env.ECGRID_API_KEY;
const parcelId = 98765;

const response = await fetch('https://rest.ecgrid.io/v2/parcels/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ parcelId })
});

const { data } = await response.json();
const bytes = Buffer.from(data.content, 'base64');
await writeFile(data.fileName, bytes);
console.log(`Saved ${data.fileName} (${bytes.length} bytes)`);''',

'python': '''import os, base64, requests
from pathlib import Path

api_key = os.environ["ECGRID_API_KEY"]
parcel_id = 98765

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/download",
    headers={"X-API-Key": api_key},
    json={"parcelId": parcel_id}
)
resp.raise_for_status()

data = resp.json()["data"]
file_bytes = base64.b64decode(data["content"])
out_path = Path(data["fileName"])
out_path.write_bytes(file_bytes)
print(f"Saved {out_path} ({len(file_bytes)} bytes)")''',
}

DOWNLOAD_SOAP = {
'java': '''// Java 11+ — SOAP ParcelDownload via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
String parcelId  = "98765";

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:ParcelDownload>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:ParcelID>" + parcelId + "</ecg:ParcelID>"
    + "</ecg:ParcelDownload></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/ParcelDownload\\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Extract Base64 ParcelDownloadResult from XML, then decode
// var bytes = Base64.getDecoder().decode(extractedBase64);
// Files.write(Path.of("parcel-" + parcelId + ".edi"), bytes);
System.out.println(response.body());''',

'nodejs': r'''// Node.js 18+ — SOAP ParcelDownload via raw HTTP
import { writeFile } from 'fs/promises';

const sessionId = 'YOUR_SESSION_ID';
const parcelId  = '98765';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelDownload>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:ParcelID>${parcelId}</ecg:ParcelID>
  </ecg:ParcelDownload></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelDownload"'
  },
  body: envelope
});
const xml = await response.text();
// Parse ParcelDownloadResult from XML, decode Base64, write to file
console.log(xml);''',

'python': r'''import requests
from pathlib import Path
import base64

session_id = "YOUR_SESSION_ID"  # obtain from Login
parcel_id  = "98765"

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelDownload>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:ParcelID>' + parcel_id + '</ecg:ParcelID>'
    '</ecg:ParcelDownload></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelDownload"'}
)
resp.raise_for_status()
# Parse ParcelDownloadResult from resp.text, decode Base64, write to file
print(resp.text)''',
}

# ─── confirm-download.md ──────────────────────────────────────────────────────

CONFIRM_REST = {
'curl': r'''curl -s -X POST https://rest.ecgrid.io/v2/parcels/confirm \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"parcelId":98765}' | jq .''',

'java': '''// Java 11+ — confirm a downloaded parcel
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
long parcelId = 98765L;

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/confirm"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\\"parcelId\\":" + parcelId + "}"))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.statusCode()); // 200 = confirmed
System.out.println(response.body());''',

'nodejs': '''// Node.js 18+ — confirm a downloaded parcel
const apiKey = process.env.ECGRID_API_KEY;
const parcelId = 98765;

const response = await fetch('https://rest.ecgrid.io/v2/parcels/confirm', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ parcelId })
});

const result = await response.json();
console.log(result.data.status); // "InBoxTransferred"''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]
parcel_id = 98765

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/confirm",
    headers={"X-API-Key": api_key},
    json={"parcelId": parcel_id}
)
resp.raise_for_status()
print(resp.json()["data"]["status"])  # "InBoxTransferred"''',
}

CONFIRM_SOAP = {
'java': '''// Java 11+ — SOAP ParcelDownloadConfirm via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
String parcelId  = "98765";

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:ParcelDownloadConfirm>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:ParcelID>" + parcelId + "</ecg:ParcelID>"
    + "</ecg:ParcelDownloadConfirm></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/ParcelDownloadConfirm\\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // true = confirmed''',

'nodejs': r'''// Node.js 18+ — SOAP ParcelDownloadConfirm via raw HTTP
const sessionId = 'YOUR_SESSION_ID';
const parcelId  = '98765';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelDownloadConfirm>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:ParcelID>${parcelId}</ecg:ParcelID>
  </ecg:ParcelDownloadConfirm></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelDownloadConfirm"'
  },
  body: envelope
});
console.log(await response.text()); // true = confirmed''',

'python': r'''import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login
parcel_id  = "98765"

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelDownloadConfirm>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:ParcelID>' + parcel_id + '</ecg:ParcelID>'
    '</ecg:ParcelDownloadConfirm></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelDownloadConfirm"'}
)
resp.raise_for_status()
print(resp.text)  # true = confirmed''',
}

# ─── upload-a-file.md ─────────────────────────────────────────────────────────

UPLOAD_REST = {
'curl': r'''# Encode the file to Base64 first, then upload
B64=$(base64 -w 0 /path/to/850_order.edi)

curl -s -X POST https://rest.ecgrid.io/v2/parcels/upload \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"fileName\":\"850_order.edi\",\"content\":\"$B64\",\"fromECGridId\":123456,\"toECGridId\":789012}" | jq .''',

'java': '''// Java 11+ — read, Base64-encode, and upload an EDI file
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

Path filePath   = Path.of("/data/edi/outbound/850_order.edi");
byte[] bytes    = Files.readAllBytes(filePath);
String base64   = Base64.getEncoder().encodeToString(bytes);
String fileName = filePath.getFileName().toString();

String body = String.format(
    "{\\"fileName\\":\\"%s\\",\\"content\\":\\"%s\\",\\"fromECGridId\\":123456,\\"toECGridId\\":789012}",
    fileName, base64);

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/upload"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = http.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // contains parcelId''',

'nodejs': '''// Node.js 18+ — read, Base64-encode, and upload an EDI file
import { readFile } from 'fs/promises';
import { basename } from 'path';

const apiKey   = process.env.ECGRID_API_KEY;
const filePath = '/data/edi/outbound/850_order.edi';

const bytes   = await readFile(filePath);
const content = bytes.toString('base64');
const fileName = basename(filePath);

const response = await fetch('https://rest.ecgrid.io/v2/parcels/upload', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ fileName, content, fromECGridId: 123456, toECGridId: 789012 })
});

const { data } = await response.json();
console.log(`Uploaded as parcelId=${data.parcelId}`);''',

'python': '''import os, base64, requests
from pathlib import Path

api_key   = os.environ["ECGRID_API_KEY"]
file_path = Path("/data/edi/outbound/850_order.edi")

file_bytes = file_path.read_bytes()
content    = base64.b64encode(file_bytes).decode()

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/upload",
    headers={"X-API-Key": api_key},
    json={
        "fileName":     file_path.name,
        "content":      content,
        "fromECGridId": 123456,
        "toECGridId":   789012,
    }
)
resp.raise_for_status()
print(f"Uploaded as parcelId={resp.json()[\'data\'][\'parcelId\']}")''',
}

UPLOAD_SOAP = {
'java': '''// Java 11+ — SOAP ParcelUpload via raw HTTP (Base64 content in envelope)
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
Path filePath    = Path.of("/data/edi/outbound/850_order.edi");
byte[] bytes     = Files.readAllBytes(filePath);
String base64    = Base64.getEncoder().encodeToString(bytes);
String fileName  = filePath.getFileName().toString();

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:ParcelUpload>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:FileName>" + fileName + "</ecg:FileName>"
    + "<ecg:Bytes>" + base64 + "</ecg:Bytes>"
    + "<ecg:Content>application/edi-x12</ecg:Content>"
    + "</ecg:ParcelUpload></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/ParcelUpload\\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // extract ParcelUploadResult (parcelId)''',

'nodejs': r'''// Node.js 18+ — SOAP ParcelUpload via raw HTTP
import { readFile } from 'fs/promises';
import { basename } from 'path';

const sessionId = 'YOUR_SESSION_ID';
const filePath  = '/data/edi/outbound/850_order.edi';
const bytes     = await readFile(filePath);
const base64    = bytes.toString('base64');
const fileName  = basename(filePath);

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelUpload>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:FileName>${fileName}</ecg:FileName>
    <ecg:Bytes>${base64}</ecg:Bytes>
    <ecg:Content>application/edi-x12</ecg:Content>
  </ecg:ParcelUpload></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelUpload"'
  },
  body: envelope
});
console.log(await response.text()); // extract ParcelUploadResult (parcelId)''',

'python': r'''import base64, requests
from pathlib import Path

session_id = "YOUR_SESSION_ID"  # obtain from Login
file_path  = Path("/data/edi/outbound/850_order.edi")
file_bytes = file_path.read_bytes()
b64        = base64.b64encode(file_bytes).decode()

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelUpload>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:FileName>' + file_path.name + '</ecg:FileName>'
    '<ecg:Bytes>' + b64 + '</ecg:Bytes>'
    '<ecg:Content>application/edi-x12</ecg:Content>'
    '</ecg:ParcelUpload></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelUpload"'}
)
resp.raise_for_status()
print(resp.text)  # extract ParcelUploadResult (parcelId)''',
}

# ─── send-edi-to-trading-partner.md ──────────────────────────────────────────

SEND_REST = {
'curl': r'''# Step 1 — find the trading partner's ECGrid ID
curl -s "https://rest.ecgrid.io/v2/ids/find?qualifier=01&id=PARTNERCO" \
  -H "X-API-Key: $ECGRID_API_KEY" | jq '.data[0].ecGridId'

# Step 2 — upload the EDI file (replace TO_ECGRID_ID with value from step 1)
B64=$(base64 -w 0 /path/to/856_asn.edi)
curl -s -X POST https://rest.ecgrid.io/v2/parcels/upload \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"fileName\":\"856_asn.edi\",\"content\":\"$B64\",\"fromECGridId\":123456,\"toECGridId\":$TO_ECGRID_ID}" | jq .''',

'java': '''// Java 11+ — find trading partner by ISA ID, then upload EDI file
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;
import com.fasterxml.jackson.databind.*;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — find partner's ECGrid ID
var findReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/find?qualifier=01&id=PARTNERCO"))
    .header("X-API-Key", key)
    .GET().build();
var findResp = http.send(findReq, HttpResponse.BodyHandlers.ofString());
JsonNode idNode = mapper.readTree(findResp.body()).path("data").get(0);
int toId = idNode.path("ecGridId").asInt();

// Step 2 — encode and upload
byte[] bytes  = Files.readAllBytes(Path.of("/data/edi/outbound/856_asn.edi"));
String base64 = Base64.getEncoder().encodeToString(bytes);
String body   = String.format(
    "{\\"fileName\\":\\"856_asn.edi\\",\\"content\\":\\"%s\\",\\"fromECGridId\\":123456,\\"toECGridId\\":%d}",
    base64, toId);

var upReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/upload"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(body)).build();

var upResp = http.send(upReq, HttpResponse.BodyHandlers.ofString());
System.out.println(upResp.body()); // parcelId''',

'nodejs': '''// Node.js 18+ — find trading partner then upload EDI file
import { readFile } from 'fs/promises';
import { basename } from 'path';

const apiKey   = process.env.ECGRID_API_KEY;
const headers  = { 'X-API-Key': apiKey };
const filePath = '/data/edi/outbound/856_asn.edi';

// Step 1 — find partner ECGrid ID
const findResp = await fetch(
  'https://rest.ecgrid.io/v2/ids/find?qualifier=01&id=PARTNERCO',
  { headers });
const { data: [partner] } = await findResp.json();
const toECGridId = partner.ecGridId;

// Step 2 — upload
const bytes   = await readFile(filePath);
const content = bytes.toString('base64');
const response = await fetch('https://rest.ecgrid.io/v2/parcels/upload', {
  method: 'POST',
  headers: { ...headers, 'Content-Type': 'application/json' },
  body: JSON.stringify({ fileName: basename(filePath), content, fromECGridId: 123456, toECGridId })
});
const { data } = await response.json();
console.log(`Sent as parcelId=${data.parcelId}`);''',

'python': '''import os, base64, requests
from pathlib import Path

api_key  = os.environ["ECGRID_API_KEY"]
session  = requests.Session()
session.headers.update({"X-API-Key": api_key})
file_path = Path("/data/edi/outbound/856_asn.edi")

# Step 1 — find trading partner ECGrid ID
find = session.get("https://rest.ecgrid.io/v2/ids/find",
                   params={"qualifier": "01", "id": "PARTNERCO"})
find.raise_for_status()
to_ecgrid_id = find.json()["data"][0]["ecGridId"]

# Step 2 — encode and upload
content = base64.b64encode(file_path.read_bytes()).decode()
resp = session.post(
    "https://rest.ecgrid.io/v2/parcels/upload",
    json={"fileName": file_path.name, "content": content,
          "fromECGridId": 123456, "toECGridId": to_ecgrid_id}
)
resp.raise_for_status()
print(f"Sent as parcelId={resp.json()[\'data\'][\'parcelId\']}")''',
}

SEND_SOAP = {
'java': '''// Java 11+ — SOAP TPSearch + ParcelUpload via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

// Step 1 — TPSearch for the partner's ECGrid ID (parse result from XML)
String searchEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:TPSearch>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>"
    + "</ecg:TPSearch></soap:Body></soap:Envelope>";

var searchReq = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/TPSearch\\"")
    .POST(BodyPublishers.ofString(searchEnv)).build();
var searchResp = http.send(searchReq, HttpResponse.BodyHandlers.ofString());
// Extract ECGridID from searchResp.body() XML, then call ParcelUpload
System.out.println(searchResp.body());''',

'nodejs': r'''// Node.js 18+ — SOAP TPSearch + ParcelUpload via raw HTTP
import { readFile } from 'fs/promises';
import { basename } from 'path';

const sessionId = 'YOUR_SESSION_ID';

// Step 1 — find partner ECGrid ID via TPSearch
const searchEnv = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:TPSearch>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:Qualifier>01</ecg:Qualifier>
    <ecg:ID>PARTNERCO</ecg:ID>
  </ecg:TPSearch></soap:Body>
</soap:Envelope>`;

const searchResp = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/TPSearch"' },
  body: searchEnv
});
// Parse ECGridID from XML, then call ParcelUpload
console.log(await searchResp.text());''',

'python': r'''import base64, requests
from pathlib import Path

session_id = "YOUR_SESSION_ID"  # obtain from Login
file_path  = Path("/data/edi/outbound/856_asn.edi")

# Step 1 — find partner ECGrid ID via TPSearch
search_env = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:TPSearch>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>'
    '</ecg:TPSearch></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=search_env.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/TPSearch"'}
)
resp.raise_for_status()
# Parse ECGridID from resp.text, then call ParcelUpload
print(resp.text)''',
}

# ─── create-a-mailbox.md ──────────────────────────────────────────────────────

CREATE_MAILBOX_REST = {
'curl': r'''curl -s -X POST https://rest.ecgrid.io/v2/mailboxes/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"uniqueId":"ACME-EDI-01","companyName":"Acme Corporation"}' | jq .''',

'java': '''// Java 11+ — create an ECGrid mailbox
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String body = "{\\"networkId\\":0,\\"uniqueId\\":\\"ACME-EDI-01\\",\\"companyName\\":\\"Acme Corporation\\"}";

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/create"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // contains mailboxId''',

'nodejs': '''// Node.js 18+ — create an ECGrid mailbox
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/mailboxes/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ networkId: 0, uniqueId: 'ACME-EDI-01', companyName: 'Acme Corporation' })
});

const { data } = await response.json();
console.log(`Mailbox created: ID=${data.mailboxId}`);''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]

resp = requests.post(
    "https://rest.ecgrid.io/v2/mailboxes/create",
    headers={"X-API-Key": api_key},
    json={"networkId": 0, "uniqueId": "ACME-EDI-01", "companyName": "Acme Corporation"}
)
resp.raise_for_status()
mailbox_id = resp.json()["data"]["mailboxId"]
print(f"Mailbox created: ID={mailbox_id}")''',
}

CREATE_MAILBOX_SOAP = {
'java': '''// Java 11+ — SOAP MailboxAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:MailboxAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID>"
    + "<ecg:UniqueID>ACME-EDI-01</ecg:UniqueID>"
    + "<ecg:CompanyName>Acme Corporation</ecg:CompanyName>"
    + "</ecg:MailboxAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/MailboxAdd\\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // extract MailboxAddResult (mailboxId)''',

'nodejs': r'''// Node.js 18+ — SOAP MailboxAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:MailboxAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID>
    <ecg:UniqueID>ACME-EDI-01</ecg:UniqueID>
    <ecg:CompanyName>Acme Corporation</ecg:CompanyName>
  </ecg:MailboxAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/MailboxAdd"' },
  body: envelope
});
console.log(await response.text()); // extract MailboxAddResult (mailboxId)''',

'python': r'''import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:MailboxAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID>'
    '<ecg:UniqueID>ACME-EDI-01</ecg:UniqueID>'
    '<ecg:CompanyName>Acme Corporation</ecg:CompanyName>'
    '</ecg:MailboxAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/MailboxAdd"'}
)
resp.raise_for_status()
print(resp.text)  # extract MailboxAddResult (mailboxId)''',
}

# ─── onboard-trading-partner.md ───────────────────────────────────────────────

ONBOARD_REST = {
'curl': r'''# Step 1 — create the trading partner's ECGrid ID
curl -s -X POST https://rest.ecgrid.io/v2/ids \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":54321,"isaQualifier":"01","isaId":"ACMECORP      ","description":"Acme Corporation"}' | jq .

# Step 2 — create the interconnect (replace PARTNER_ECGRID_ID with step 1 ecGridId)
curl -s -X POST https://rest.ecgrid.io/v2/partners \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"ecGridIdFrom\":111111,\"ecGridIdTo\":$PARTNER_ECGRID_ID,\"status\":\"Active\"}" | jq .''',

'java': '''// Java 11+ — create ECGrid ID then interconnect
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — create trading partner ECGrid ID
String idBody = "{\\"networkId\\":0,\\"mailboxId\\":54321,\\"isaQualifier\\":\\"01\\"," +
    "\\"isaId\\":\\"ACMECORP      \\",\\"description\\":\\"Acme Corporation\\",\\"useType\\":\\"Production\\"}";

var idReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(idBody)).build();
var idResp = http.send(idReq, BodyHandlers.ofString());
int partnerECGridId = mapper.readTree(idResp.body()).path("data").path("ecGridId").asInt();
System.out.println("ECGrid ID created: " + partnerECGridId);

// Step 2 — create interconnect
String partnerBody = String.format(
    "{\\"ecGridIdFrom\\":111111,\\"ecGridIdTo\\":%d,\\"status\\":\\"Active\\"}", partnerECGridId);
var pReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(partnerBody)).build();
var pResp = http.send(pReq, BodyHandlers.ofString());
System.out.println(pResp.body()); // interconnectId''',

'nodejs': '''// Node.js 18+ — create ECGrid ID then interconnect
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — create trading partner ECGrid ID
const idResp = await fetch('https://rest.ecgrid.io/v2/ids', {
  method: 'POST', headers,
  body: JSON.stringify({ networkId: 0, mailboxId: 54321, isaQualifier: '01',
                         isaId: 'ACMECORP      ', description: 'Acme Corporation' })
});
const { data: idData } = await idResp.json();
console.log(`ECGrid ID created: ${idData.ecGridId}`);

// Step 2 — create interconnect
const pResp = await fetch('https://rest.ecgrid.io/v2/partners', {
  method: 'POST', headers,
  body: JSON.stringify({ ecGridIdFrom: 111111, ecGridIdTo: idData.ecGridId, status: 'Active' })
});
const { data: partner } = await pResp.json();
console.log(`Interconnect created: ID=${partner.interconnectId}`);''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})

# Step 1 — create trading partner ECGrid ID
id_resp = session.post("https://rest.ecgrid.io/v2/ids", json={
    "networkId": 0, "mailboxId": 54321, "isaQualifier": "01",
    "isaId": "ACMECORP      ", "description": "Acme Corporation"
})
id_resp.raise_for_status()
partner_ecgrid_id = id_resp.json()["data"]["ecGridId"]
print(f"ECGrid ID created: {partner_ecgrid_id}")

# Step 2 — create interconnect
p_resp = session.post("https://rest.ecgrid.io/v2/partners", json={
    "ecGridIdFrom": 111111, "ecGridIdTo": partner_ecgrid_id, "status": "Active"
})
p_resp.raise_for_status()
print(f"Interconnect: {p_resp.json()[\'data\'][\'interconnectId\']}")''',
}

ONBOARD_SOAP = {
'java': '''// Java 11+ — SOAP TPAdd + InterconnectAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String tpEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:TPAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>"
    + "<ecg:ISAQualifier>01</ecg:ISAQualifier>"
    + "<ecg:ISAID>ACMECORP      </ecg:ISAID>"
    + "<ecg:Description>Acme Corporation</ecg:Description>"
    + "</ecg:TPAdd></soap:Body></soap:Envelope>";

var tpReq = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/TPAdd\\"")
    .POST(BodyPublishers.ofString(tpEnv)).build();

var tpResp = http.send(tpReq, HttpResponse.BodyHandlers.ofString());
// Extract ECGridID from tpResp XML, then call InterconnectAdd
System.out.println(tpResp.body());''',

'nodejs': r'''// Node.js 18+ — SOAP TPAdd + InterconnectAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const tpEnvelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:TPAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>
    <ecg:ISAQualifier>01</ecg:ISAQualifier>
    <ecg:ISAID>ACMECORP      </ecg:ISAID>
    <ecg:Description>Acme Corporation</ecg:Description>
  </ecg:TPAdd></soap:Body>
</soap:Envelope>`;

const tpResp = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/TPAdd"' },
  body: tpEnvelope
});
// Extract ECGridID from XML, then call InterconnectAdd
console.log(await tpResp.text());''',

'python': r'''import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

tp_env = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:TPAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>'
    '<ecg:ISAQualifier>01</ecg:ISAQualifier>'
    '<ecg:ISAID>ACMECORP      </ecg:ISAID>'
    '<ecg:Description>Acme Corporation</ecg:Description>'
    '</ecg:TPAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=tp_env.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/TPAdd"'}
)
resp.raise_for_status()
# Extract ECGridID from resp.text, then call InterconnectAdd
print(resp.text)''',
}

# ─── setup-interconnect.md ────────────────────────────────────────────────────

SETUP_IC_REST = {
'curl': r'''# Step 1 — find the trading partner's ECGrid ID
curl -s "https://rest.ecgrid.io/v2/ids/find?isaQualifier=01&isaId=PARTNERCO" \
  -H "X-API-Key: $ECGRID_API_KEY" | jq '.data[0].ecGridId'

# Step 2 — create the interconnect (replace PARTNER_ID with result above)
curl -s -X POST https://rest.ecgrid.io/v2/partners \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"ecGridIdFrom\":111111,\"ecGridIdTo\":$PARTNER_ID,\"status\":\"Active\"}" | jq .''',

'java': '''// Java 11+ — find partner ECGrid ID then create interconnect
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — search for partner ECGrid ID
var findReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/find?isaQualifier=01&isaId=PARTNERCO"))
    .header("X-API-Key", key).GET().build();
var findResp = http.send(findReq, BodyHandlers.ofString());
int partnerId = mapper.readTree(findResp.body()).path("data").get(0).path("ecGridId").asInt();

// Step 2 — create the interconnect
String body = String.format(
    "{\\"ecGridIdFrom\\":111111,\\"ecGridIdTo\\":%d,\\"status\\":\\"Active\\"}", partnerId);
var icReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(body)).build();
var icResp = http.send(icReq, BodyHandlers.ofString());
System.out.println(icResp.body()); // interconnectId''',

'nodejs': '''// Node.js 18+ — find partner ECGrid ID then create interconnect
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'X-API-Key': apiKey };

// Step 1 — find partner ECGrid ID
const findResp = await fetch(
  'https://rest.ecgrid.io/v2/ids/find?isaQualifier=01&isaId=PARTNERCO',
  { headers });
const { data: [partner] } = await findResp.json();

// Step 2 — create interconnect
const icResp = await fetch('https://rest.ecgrid.io/v2/partners', {
  method: 'POST',
  headers: { ...headers, 'Content-Type': 'application/json' },
  body: JSON.stringify({ ecGridIdFrom: 111111, ecGridIdTo: partner.ecGridId, status: 'Active' })
});
const { data: ic } = await icResp.json();
console.log(`Interconnect created: ID=${ic.interconnectId}`);''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

# Step 1 — find partner ECGrid ID
find = session.get("https://rest.ecgrid.io/v2/ids/find",
                   params={"isaQualifier": "01", "isaId": "PARTNERCO"})
find.raise_for_status()
partner_id = find.json()["data"][0]["ecGridId"]

# Step 2 — create interconnect
resp = session.post("https://rest.ecgrid.io/v2/partners",
    json={"ecGridIdFrom": 111111, "ecGridIdTo": partner_id, "status": "Active"})
resp.raise_for_status()
print(f"Interconnect: {resp.json()[\'data\'][\'interconnectId\']}")''',
}

SETUP_IC_SOAP = {
'java': '''// Java 11+ — SOAP TPSearch + InterconnectAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String searchEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:TPSearch>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>"
    + "<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>10</ecg:RecordsPerPage>"
    + "</ecg:TPSearch></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/TPSearch\\"")
    .POST(BodyPublishers.ofString(searchEnv)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Parse ECGridID from XML, then call InterconnectAdd
System.out.println(response.body());''',

'nodejs': r'''// Node.js 18+ — SOAP TPSearch + InterconnectAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const searchEnv = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:TPSearch>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:Qualifier>01</ecg:Qualifier>
    <ecg:ID>PARTNERCO</ecg:ID>
    <ecg:PageNo>1</ecg:PageNo>
    <ecg:RecordsPerPage>10</ecg:RecordsPerPage>
  </ecg:TPSearch></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/TPSearch"' },
  body: searchEnv
});
// Parse ECGridID from XML, then call InterconnectAdd
console.log(await response.text());''',

'python': r'''import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:TPSearch>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>'
    '<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>10</ecg:RecordsPerPage>'
    '</ecg:TPSearch></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/TPSearch"'}
)
resp.raise_for_status()
# Parse ECGridID from resp.text, then call InterconnectAdd
print(resp.text)''',
}

# ─── configure-callbacks.md ───────────────────────────────────────────────────

CALLBACKS_REST = {
'curl': r'''# Step 1 — register the callback
curl -s -X POST https://rest.ecgrid.io/v2/callbacks/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":0,"ecGridId":0,"callBackUrl":"https://your-app.example.com/webhooks/ecgrid","callBackEvent":"InBox","frequency":1,"retries":3,"status":"Active"}' | jq .

# Step 2 — send a test event (replace QUEUE_ID with callBackQueueId from step 1)
curl -s -X POST https://rest.ecgrid.io/v2/callbacks/test \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"callBackQueueId":7001}' | jq .''',

'java': '''// Java 11+ — register a callback and fire a test event
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — register callback
String createBody = "{\\"networkId\\":0,\\"mailboxId\\":0,\\"ecGridId\\":0,"
    + "\\"callBackUrl\\":\\"https://your-app.example.com/webhooks/ecgrid\\","
    + "\\"callBackEvent\\":\\"InBox\\",\\"frequency\\":1,\\"retries\\":3,\\"status\\":\\"Active\\"}";

var createReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/create"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(createBody)).build();
var createResp = http.send(createReq, BodyHandlers.ofString());
int queueId = mapper.readTree(createResp.body()).path("data").path("callBackQueueId").asInt();
System.out.println("Callback registered: ID=" + queueId);

// Step 2 — send test event
String testBody = "{\\"callBackQueueId\\":" + queueId + "}";
var testReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/test"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(testBody)).build();
http.send(testReq, BodyHandlers.ofString());
System.out.println("Test event sent — verify your endpoint.");''',

'nodejs': '''// Node.js 18+ — register a callback and fire a test event
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — register callback
const createResp = await fetch('https://rest.ecgrid.io/v2/callbacks/create', {
  method: 'POST', headers,
  body: JSON.stringify({
    networkId: 0, mailboxId: 0, ecGridId: 0,
    callBackUrl: 'https://your-app.example.com/webhooks/ecgrid',
    callBackEvent: 'InBox', frequency: 1, retries: 3, status: 'Active'
  })
});
const { data } = await createResp.json();
console.log(`Callback registered: ID=${data.callBackQueueId}`);

// Step 2 — test it
await fetch('https://rest.ecgrid.io/v2/callbacks/test', {
  method: 'POST', headers,
  body: JSON.stringify({ callBackQueueId: data.callBackQueueId })
});
console.log('Test event sent — verify your endpoint.');''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

# Step 1 — register callback
create = session.post("https://rest.ecgrid.io/v2/callbacks/create", json={
    "networkId": 0, "mailboxId": 0, "ecGridId": 0,
    "callBackUrl": "https://your-app.example.com/webhooks/ecgrid",
    "callBackEvent": "InBox", "frequency": 1, "retries": 3, "status": "Active"
})
create.raise_for_status()
queue_id = create.json()["data"]["callBackQueueId"]
print(f"Callback registered: ID={queue_id}")

# Step 2 — send test event
test = session.post("https://rest.ecgrid.io/v2/callbacks/test",
                    json={"callBackQueueId": queue_id})
test.raise_for_status()
print("Test event sent — verify your endpoint.")''',
}

CALLBACKS_SOAP = {
'java': '''// Java 11+ — SOAP CallBackAdd + CallBackTest via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String addEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:CallBackAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>"
    + "<ecg:ECGridID>0</ecg:ECGridID>"
    + "<ecg:CallBackURL>https://your-app.example.com/webhooks/ecgrid</ecg:CallBackURL>"
    + "<ecg:CallBackEvent>InBox</ecg:CallBackEvent>"
    + "<ecg:Frequency>1</ecg:Frequency><ecg:Retries>3</ecg:Retries>"
    + "</ecg:CallBackAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/CallBackAdd\\"")
    .POST(BodyPublishers.ofString(addEnv)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Extract CallBackQueueID from XML, then call CallBackTest
System.out.println(response.body());''',

'nodejs': r'''// Node.js 18+ — SOAP CallBackAdd + CallBackTest via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const addEnvelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:CallBackAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>
    <ecg:ECGridID>0</ecg:ECGridID>
    <ecg:CallBackURL>https://your-app.example.com/webhooks/ecgrid</ecg:CallBackURL>
    <ecg:CallBackEvent>InBox</ecg:CallBackEvent>
    <ecg:Frequency>1</ecg:Frequency><ecg:Retries>3</ecg:Retries>
  </ecg:CallBackAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/CallBackAdd"' },
  body: addEnvelope
});
// Extract CallBackQueueID from XML, then call CallBackTest
console.log(await response.text());''',

'python': r'''import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:CallBackAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>'
    '<ecg:ECGridID>0</ecg:ECGridID>'
    '<ecg:CallBackURL>https://your-app.example.com/webhooks/ecgrid</ecg:CallBackURL>'
    '<ecg:CallBackEvent>InBox</ecg:CallBackEvent>'
    '<ecg:Frequency>1</ecg:Frequency><ecg:Retries>3</ecg:Retries>'
    '</ecg:CallBackAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/CallBackAdd"'}
)
resp.raise_for_status()
# Extract CallBackQueueID from resp.text, then call CallBackTest
print(resp.text)''',
}

# ─── manage-users-permissions.md ──────────────────────────────────────────────

USERS_REST = {
'curl': r'''# Step 1 — create the user
curl -s -X POST https://rest.ecgrid.io/v2/users \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":54321,"loginName":"jsmith","password":"S3cur3P@ssword!","firstName":"Jane","lastName":"Smith","email":"jsmith@example.com","authLevel":"General"}' | jq .

# Step 2 — set the authorization level (replace USER_ID with userId from step 1)
curl -s -X POST https://rest.ecgrid.io/v2/users/role \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"userId\":$USER_ID,\"authLevel\":\"MailboxAdmin\"}" | jq .''',

'java': '''// Java 11+ — create user then set authorization level
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — create user
String createBody = "{\\"networkId\\":0,\\"mailboxId\\":54321,\\"loginName\\":\\"jsmith\\","
    + "\\"password\\":\\"S3cur3P@ssword!\\",\\"firstName\\":\\"Jane\\",\\"lastName\\":\\"Smith\\","
    + "\\"email\\":\\"jsmith@example.com\\",\\"authLevel\\":\\"General\\"}";

var createReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(createBody)).build();
var createResp = http.send(createReq, BodyHandlers.ofString());
int userId = mapper.readTree(createResp.body()).path("data").path("userId").asInt();
System.out.println("User created: ID=" + userId);

// Step 2 — set role
String roleBody = "{\\"userId\\":" + userId + ",\\"authLevel\\":\\"MailboxAdmin\\"}";
var roleReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/role"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(roleBody)).build();
http.send(roleReq, BodyHandlers.ofString());
System.out.println("AuthLevel set to MailboxAdmin");''',

'nodejs': '''// Node.js 18+ — create user then set authorization level
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — create user
const createResp = await fetch('https://rest.ecgrid.io/v2/users', {
  method: 'POST', headers,
  body: JSON.stringify({
    networkId: 0, mailboxId: 54321, loginName: 'jsmith',
    password: process.env.NEW_USER_PASSWORD,
    firstName: 'Jane', lastName: 'Smith',
    email: 'jsmith@example.com', authLevel: 'General'
  })
});
const { data: user } = await createResp.json();
console.log(`User created: ID=${user.userId}`);

// Step 2 — set role
await fetch('https://rest.ecgrid.io/v2/users/role', {
  method: 'POST', headers,
  body: JSON.stringify({ userId: user.userId, authLevel: 'MailboxAdmin' })
});
console.log('AuthLevel set to MailboxAdmin');''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

# Step 1 — create user
create = session.post("https://rest.ecgrid.io/v2/users", json={
    "networkId": 0, "mailboxId": 54321, "loginName": "jsmith",
    "password": os.environ["NEW_USER_PASSWORD"],
    "firstName": "Jane", "lastName": "Smith",
    "email": "jsmith@example.com", "authLevel": "General"
})
create.raise_for_status()
user_id = create.json()["data"]["userId"]
print(f"User created: ID={user_id}")

# Step 2 — set role
role = session.post("https://rest.ecgrid.io/v2/users/role",
                    json={"userId": user_id, "authLevel": "MailboxAdmin"})
role.raise_for_status()
print("AuthLevel set to MailboxAdmin")''',
}

USERS_SOAP = {
'java': '''// Java 11+ — SOAP UserAdd + UserSetAuthLevel via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
String password  = System.getenv("NEW_USER_PASSWORD");

String addEnv = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:UserAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>"
    + "<ecg:LoginName>jsmith</ecg:LoginName>"
    + "<ecg:Password>" + password + "</ecg:Password>"
    + "<ecg:FirstName>Jane</ecg:FirstName><ecg:LastName>Smith</ecg:LastName>"
    + "<ecg:EMail>jsmith@example.com</ecg:EMail>"
    + "</ecg:UserAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/UserAdd\\"")
    .POST(BodyPublishers.ofString(addEnv)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Extract UserID from XML, then call UserSetAuthLevel
System.out.println(response.body());''',

'nodejs': r'''// Node.js 18+ — SOAP UserAdd + UserSetAuthLevel via raw HTTP
const sessionId = 'YOUR_SESSION_ID';
const password  = process.env.NEW_USER_PASSWORD;

const addEnvelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:UserAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>
    <ecg:LoginName>jsmith</ecg:LoginName>
    <ecg:Password>${password}</ecg:Password>
    <ecg:FirstName>Jane</ecg:FirstName><ecg:LastName>Smith</ecg:LastName>
    <ecg:EMail>jsmith@example.com</ecg:EMail>
  </ecg:UserAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/UserAdd"' },
  body: addEnvelope
});
// Extract UserID from XML, then call UserSetAuthLevel
console.log(await response.text());''',

'python': r'''import os, requests

session_id = "YOUR_SESSION_ID"  # obtain from Login
password   = os.environ["NEW_USER_PASSWORD"]

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:UserAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>'
    '<ecg:LoginName>jsmith</ecg:LoginName>'
    '<ecg:Password>' + password + '</ecg:Password>'
    '<ecg:FirstName>Jane</ecg:FirstName><ecg:LastName>Smith</ecg:LastName>'
    '<ecg:EMail>jsmith@example.com</ecg:EMail>'
    '</ecg:UserAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/UserAdd"'}
)
resp.raise_for_status()
# Extract UserID from resp.text, then call UserSetAuthLevel
print(resp.text)''',
}

# ─── work-with-carbon-copies.md ───────────────────────────────────────────────

CARBONCOPY_REST = {
'curl': r'''curl -s -X POST https://rest.ecgrid.io/v2/carboncopies/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":54321,"ecGridIdFrom":0,"ecGridIdTo":0,"copyToMailboxId":99001,"direction":"InBox","status":"Active"}' | jq .''',

'java': '''// Java 11+ — create a carbon copy rule
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String body = "{\\"networkId\\":0,\\"mailboxId\\":54321,\\"ecGridIdFrom\\":0,\\"ecGridIdTo\\":0,"
    + "\\"copyToMailboxId\\":99001,\\"direction\\":\\"InBox\\",\\"status\\":\\"Active\\"}";

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/carboncopies/create"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // carbonCopyId''',

'nodejs': '''// Node.js 18+ — create a carbon copy rule
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/carboncopies/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({
    networkId: 0, mailboxId: 54321,
    ecGridIdFrom: 0, ecGridIdTo: 0,
    copyToMailboxId: 99001, direction: 'InBox', status: 'Active'
  })
});

const { data } = await response.json();
console.log(`Carbon copy created: ID=${data.carbonCopyId}`);''',

'python': '''import os, requests

api_key = os.environ["ECGRID_API_KEY"]

resp = requests.post(
    "https://rest.ecgrid.io/v2/carboncopies/create",
    headers={"X-API-Key": api_key},
    json={
        "networkId": 0, "mailboxId": 54321,
        "ecGridIdFrom": 0, "ecGridIdTo": 0,
        "copyToMailboxId": 99001, "direction": "InBox", "status": "Active"
    }
)
resp.raise_for_status()
print(f"Carbon copy created: ID={resp.json()[\'data\'][\'carbonCopyId\']}")''',
}

CARBONCOPY_SOAP = {
'java': '''// Java 11+ — SOAP CarbonCopyAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String envelope = "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>"
    + "<soap:Envelope xmlns:soap=\\"http://schemas.xmlsoap.org/soap/envelope/\\""
    + " xmlns:ecg=\\"http://www.ecgridos.net/\\"><soap:Body><ecg:CarbonCopyAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>"
    + "<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>"
    + "<ecg:CopyToMailboxID>99001</ecg:CopyToMailboxID>"
    + "<ecg:Direction>InBox</ecg:Direction>"
    + "</ecg:CarbonCopyAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\\"http://www.ecgridos.net/CarbonCopyAdd\\"")
    .POST(BodyPublishers.ofString(envelope)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // carbon copy ID''',

'nodejs': r'''// Node.js 18+ — SOAP CarbonCopyAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:CarbonCopyAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>
    <ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>
    <ecg:CopyToMailboxID>99001</ecg:CopyToMailboxID>
    <ecg:Direction>InBox</ecg:Direction>
  </ecg:CarbonCopyAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/CarbonCopyAdd"' },
  body: envelope
});
console.log(await response.text()); // carbon copy ID''',

'python': r'''import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:CarbonCopyAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>'
    '<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>'
    '<ecg:CopyToMailboxID>99001</ecg:CopyToMailboxID>'
    '<ecg:Direction>InBox</ecg:Direction>'
    '</ecg:CarbonCopyAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/CarbonCopyAdd"'}
)
resp.raise_for_status()
print(resp.text)  # carbon copy ID''',
}

# ─── File processing list ─────────────────────────────────────────────────────

ATTR = "Add multi-language code tabs (cURL, C#, Java, Node.js, Python)"

FILES = [
    ("common-operations/poll-inbound-files.md",
     "### Complete C# Example", POLL_REST,
     "### Complete C# Example", POLL_SOAP, ATTR),

    ("common-operations/download-a-file.md",
     "### Complete C# Example", DOWNLOAD_REST,
     "### Complete C# Example", DOWNLOAD_SOAP, ATTR),

    ("common-operations/confirm-download.md",
     "### Complete C# Example", CONFIRM_REST,
     "### Complete C# Example", CONFIRM_SOAP, ATTR),

    ("common-operations/upload-a-file.md",
     "### Complete C# Example", UPLOAD_REST,
     "### Complete C# Example", UPLOAD_SOAP, ATTR),

    ("common-operations/send-edi-to-trading-partner.md",
     "### Complete C# Example", SEND_REST,
     "### Complete C# Example", SEND_SOAP, ATTR),

    ("common-operations/create-a-mailbox.md",
     "### Complete C# Example", CREATE_MAILBOX_REST,
     "### Complete C# Example", CREATE_MAILBOX_SOAP, ATTR),

    ("common-operations/onboard-trading-partner.md",
     "### Complete C# Example", ONBOARD_REST,
     "### Complete C# Example", ONBOARD_SOAP, ATTR),

    ("common-operations/setup-interconnect.md",
     "### Complete C# Example", SETUP_IC_REST,
     "### Complete C# Example", SETUP_IC_SOAP, ATTR),

    ("common-operations/configure-callbacks.md",
     "### Complete C# Example — REST Client", CALLBACKS_REST,
     "### Complete C# Example", CALLBACKS_SOAP, ATTR),

    ("common-operations/manage-users-permissions.md",
     "### Complete C# Example", USERS_REST,
     "### Complete C# Example", USERS_SOAP, ATTR),

    ("common-operations/work-with-carbon-copies.md",
     "### Complete C# Example", CARBONCOPY_REST,
     "### Complete C# Example", CARBONCOPY_SOAP, ATTR),
]

if __name__ == "__main__":
    ok = 0
    for (rel, rest_h, rest_x, soap_h, soap_x, desc) in FILES:
        try:
            process(rel, rest_h, rest_x, soap_h, soap_x, desc)
            ok += 1
        except Exception as e:
            print(f"  ERROR: {e}")
    print(f"\nDone: {ok}/{len(FILES)} files processed.")
