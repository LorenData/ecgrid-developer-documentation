#!/usr/bin/env python3
"""
Add multi-language code tabs to REST and SOAP endpoint documentation pages.

Processes:
  docs/rest-api/**/*.md  — adds cURL, C#, Java, Node.js, Python tabs
  docs/soap-api/**/*.md  — adds C#, Java, Node.js, Python tabs

Skips files that already contain <Tabs or have no ## C# Example section.
"""

import re
from pathlib import Path

DOCS_DIR = Path(r"E:\LD_Code\ECGrid Developer Documentation Portal\website\docs")
REST_DIR = DOCS_DIR / "rest-api"
SOAP_DIR = DOCS_DIR / "soap-api"

TABS_IMPORT = "import Tabs from '@theme/Tabs';\nimport TabItem from '@theme/TabItem';"
SKIP_FILES = {"overview.md"}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def has_tabs(content):
    return "<Tabs" in content

def has_tabs_import(content):
    return "import Tabs from" in content

def insert_tabs_import(content):
    """Insert Tabs import after the AI Attribution comment line."""
    m = re.search(r'(\{/\* AI Attribution[^\n]*\*/\})\n', content)
    if m:
        pos = m.end()
        return content[:pos] + "\n" + TABS_IMPORT + "\n" + content[pos:]
    # Fallback: after closing frontmatter ---
    m2 = re.search(r'^---\n', content[4:])
    if m2:
        pos = 4 + m2.end()
        return content[:pos] + "\n" + TABS_IMPORT + "\n" + content[pos:]
    return content

def extract_endpoint(content):
    """Return (METHOD, /path) or (None, None)."""
    m = re.search(r"## Endpoint\s*```http\s*(\w+)\s+(/[^\s`]*)\s*```", content, re.DOTALL)
    if m:
        return m.group(1).upper(), m.group(2).strip()
    return None, None

def extract_request_json(content):
    """Return first JSON block in ## Request Body section, or None."""
    m = re.search(r"## Request Body.*?```json\s*(.*?)```", content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return None

def extract_csharp_block(content):
    """Return code inside ## C# Example code fence, or None."""
    m = re.search(r"## C# Example\s*```csharp\s*(.*?)```", content, re.DOTALL)
    if m:
        return m.group(1).rstrip()
    return None

def compact_json(s):
    return " ".join(s.split())

def path_params(path):
    return re.findall(r"\{(\w+)\}", path)

def to_upper_snake(name):
    """camelCase to UPPER_SNAKE_CASE."""
    s = re.sub(r"([A-Z])", r"_\1", name).upper()
    return s.lstrip("_")

def to_snake(name):
    """camelCase to snake_case."""
    s = re.sub(r"([A-Z])", r"_\1", name).lower()
    return s.lstrip("_")

# ─── REST code generators ─────────────────────────────────────────────────────

def gen_curl(method, path, json_body):
    params = path_params(path)
    curl_path = path
    for p in params:
        curl_path = curl_path.replace("{" + p + "}", "$" + to_upper_snake(p))

    url = "https://rest.ecgrid.io" + curl_path
    lines = [f'curl -X {method} "{url}" \\']
    lines.append('  -H "X-API-Key: $ECGRID_API_KEY"')

    if method in ("POST", "PUT", "PATCH") and json_body:
        cj = compact_json(json_body).replace("'", "'\"'\"'")
        lines[-1] += " \\"
        lines.append('  -H "Content-Type: application/json" \\')
        lines.append(f"  -d '{cj}'")
    return "\n".join(lines)

def gen_java_rest(method, path, json_body):
    params = path_params(path)

    if params:
        fmt_path = re.sub(r"\{\w+\}", "%s", path)
        decls = [f'String {p} = "0"; // replace with actual {p}' for p in params]
        url_expr = 'String.format("https://rest.ecgrid.io' + fmt_path + '", ' + ", ".join(params) + ")"
        decl_lines = "\n".join(decls)
    else:
        decl_lines = ""
        url_expr = '"https://rest.ecgrid.io' + path + '"'

    lines = [
        "import java.net.URI;",
        "import java.net.http.*;",
        "",
        'String apiKey = System.getenv("ECGRID_API_KEY");',
    ]
    if decl_lines:
        lines.append(decl_lines)
    lines.append("")

    if method in ("POST", "PUT", "PATCH") and json_body:
        cj = compact_json(json_body).replace('"', '\\"')
        lines.append(f'String body = "{cj}";')
        lines.append("")
        lines += [
            "HttpRequest request = HttpRequest.newBuilder()",
            f"    .uri(URI.create({url_expr}))",
            '    .header("X-API-Key", apiKey)',
            '    .header("Content-Type", "application/json")',
        ]
        if method == "PATCH":
            lines.append(f'    .method("PATCH", HttpRequest.BodyPublishers.ofString(body))')
        else:
            lines.append(f"    .{method}(HttpRequest.BodyPublishers.ofString(body))")
        lines.append("    .build();")
    elif method == "DELETE":
        lines += [
            "HttpRequest request = HttpRequest.newBuilder()",
            f"    .uri(URI.create({url_expr}))",
            '    .header("X-API-Key", apiKey)',
            "    .DELETE()",
            "    .build();",
        ]
    else:
        lines += [
            "HttpRequest request = HttpRequest.newBuilder()",
            f"    .uri(URI.create({url_expr}))",
            '    .header("X-API-Key", apiKey)',
            "    .GET()",
            "    .build();",
        ]

    lines += [
        "",
        "HttpClient client = HttpClient.newHttpClient();",
        "HttpResponse<String> response = client.send(",
        "    request, HttpResponse.BodyHandlers.ofString());",
        "",
        "System.out.println(response.body());",
    ]
    return "\n".join(lines)

def gen_nodejs_rest(method, path, json_body):
    params = path_params(path)

    if params:
        node_path = path
        for p in params:
            node_path = node_path.replace("{" + p + "}", "${" + p + "}")
        url_line = f"const url = `https://rest.ecgrid.io{node_path}`;"
    else:
        url_line = f"const url = 'https://rest.ecgrid.io{path}';"

    lines = [
        "const apiKey = process.env.ECGRID_API_KEY;",
        url_line,
        "",
    ]

    if method in ("POST", "PUT", "PATCH") and json_body:
        cj = compact_json(json_body)
        lines += [
            "const response = await fetch(url, {",
            f"  method: '{method}',",
            "  headers: {",
            "    'X-API-Key': apiKey,",
            "    'Content-Type': 'application/json',",
            "  },",
            f"  body: JSON.stringify({cj}),",
            "});",
        ]
    else:
        lines += [
            "const response = await fetch(url, {",
            f"  method: '{method}',",
            "  headers: { 'X-API-Key': apiKey },",
            "});",
        ]

    lines += ["", "const data = await response.json();", "console.log(data);"]
    return "\n".join(lines)

def gen_python_rest(method, path, json_body):
    params = path_params(path)

    if params:
        py_path = path
        for p in params:
            py_path = py_path.replace("{" + p + "}", "{" + to_snake(p) + "}")
        snake_decls = [f'{to_snake(p)} = 0  # replace with actual {to_snake(p)}' for p in params]
        decl_block = "\n".join(snake_decls) + "\n"
        url_line = f'url = f"https://rest.ecgrid.io{py_path}"'
    else:
        decl_block = ""
        url_line = f'url = "https://rest.ecgrid.io{path}"'

    lines = [
        "import os, requests",
        "",
        'api_key = os.environ["ECGRID_API_KEY"]',
        'headers = {"X-API-Key": api_key}',
    ]
    if decl_block:
        lines.append(decl_block.rstrip())
    lines += [url_line, ""]

    m = method.lower()
    if method in ("POST", "PUT", "PATCH") and json_body:
        cj = compact_json(json_body)
        lines += [
            f"response = requests.{m}(",
            "    url,",
            f"    json={cj},",
            "    headers=headers,",
            ")",
        ]
    else:
        lines.append(f"response = requests.{m}(url, headers=headers)")

    lines += ["", "response.raise_for_status()", "print(response.json())"]
    return "\n".join(lines)

def build_rest_tabs(method, path, json_body, csharp_code):
    curl = gen_curl(method, path, json_body)
    java = gen_java_rest(method, path, json_body)
    node = gen_nodejs_rest(method, path, json_body)
    py   = gen_python_rest(method, path, json_body)
    return (
        "## Code Examples\n\n"
        "<Tabs groupId=\"lang\">\n"
        "<TabItem value=\"curl\" label=\"cURL\">\n\n"
        "```bash\n" + curl + "\n```\n\n"
        "</TabItem>\n"
        "<TabItem value=\"csharp\" label=\"C#\">\n\n"
        "```csharp\n" + csharp_code + "\n```\n\n"
        "</TabItem>\n"
        "<TabItem value=\"java\" label=\"Java\">\n\n"
        "```java\n" + java + "\n```\n\n"
        "</TabItem>\n"
        "<TabItem value=\"nodejs\" label=\"Node.js\">\n\n"
        "```javascript\n" + node + "\n```\n\n"
        "</TabItem>\n"
        "<TabItem value=\"python\" label=\"Python\">\n\n"
        "```python\n" + py + "\n```\n\n"
        "</TabItem>\n"
        "</Tabs>"
    )

# ─── SOAP code generators ─────────────────────────────────────────────────────

def extract_soap_method(content):
    m = re.search(r"## Method Signature\s*```[^\n]*\n\s*[\w<>\[\]]+\s+(\w+)\s*\(", content, re.DOTALL)
    if m:
        return m.group(1)
    return None

def gen_java_soap(method_name):
    return (
        "// JAX-WS generated client\n"
        "// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL\n\n"
        "ECGridOS service = new ECGridOS();\n"
        "ECGridOSPortType port = service.getECGridOSPort();\n\n"
        f"var result = port.{method_name}(sessionID /*, additional params */);\n"
        "System.out.println(result);"
    )

def gen_nodejs_soap(method_name):
    return (
        "// npm install soap\n"
        "import soap from 'soap';\n\n"
        "const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';\n"
        "const client = await soap.createClientAsync(WSDL);\n\n"
        f"const [result] = await client.{method_name}Async({{\n"
        "  SessionID: sessionId,\n"
        "  // additional params\n"
        "});\n"
        "console.log(result);"
    )

def gen_python_soap(method_name):
    return (
        "# pip install zeep\n"
        "from zeep import Client\n\n"
        "WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL'\n"
        "client = Client(WSDL)\n\n"
        f"result = client.service.{method_name}(\n"
        "    SessionID=session_id,\n"
        "    # additional params\n"
        ")\n"
        "print(result)"
    )

def build_soap_tabs(method_name, csharp_code):
    java = gen_java_soap(method_name)
    node = gen_nodejs_soap(method_name)
    py   = gen_python_soap(method_name)
    return (
        "## Code Examples\n\n"
        "<Tabs groupId=\"lang\">\n"
        "<TabItem value=\"csharp\" label=\"C#\">\n\n"
        "```csharp\n" + csharp_code + "\n```\n\n"
        "</TabItem>\n"
        "<TabItem value=\"java\" label=\"Java\">\n\n"
        "```java\n" + java + "\n```\n\n"
        "</TabItem>\n"
        "<TabItem value=\"nodejs\" label=\"Node.js\">\n\n"
        "```javascript\n" + node + "\n```\n\n"
        "</TabItem>\n"
        "<TabItem value=\"python\" label=\"Python\">\n\n"
        "```python\n" + py + "\n```\n\n"
        "</TabItem>\n"
        "</Tabs>"
    )

# ─── File processors ──────────────────────────────────────────────────────────

def process_rest_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    if has_tabs(content):
        print(f"  skip (tabs exist)  : {filepath.name}")
        return
    csharp = extract_csharp_block(content)
    if not csharp:
        print(f"  skip (no C# block) : {filepath.name}")
        return
    method, path = extract_endpoint(content)
    if not method:
        print(f"  skip (no endpoint) : {filepath.name}")
        return
    json_body = extract_request_json(content)

    if not has_tabs_import(content):
        content = insert_tabs_import(content)

    tabs_block = build_rest_tabs(method, path, json_body, csharp)
    new_content = re.sub(
        r"## C# Example\s*```csharp.*?```",
        lambda _m: tabs_block,
        content,
        flags=re.DOTALL,
        count=1,
    )
    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  ok                 : {filepath.name}")
    else:
        print(f"  no change          : {filepath.name}")

def process_soap_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    if has_tabs(content):
        print(f"  skip (tabs exist)  : {filepath.name}")
        return
    csharp = extract_csharp_block(content)
    if not csharp:
        print(f"  skip (no C# block) : {filepath.name}")
        return
    method_name = extract_soap_method(content)
    if not method_name:
        print(f"  skip (no method)   : {filepath.name}")
        return

    if not has_tabs_import(content):
        content = insert_tabs_import(content)

    tabs_block = build_soap_tabs(method_name, csharp)
    new_content = re.sub(
        r"## C# Example\s*```csharp.*?```",
        lambda _m: tabs_block,
        content,
        flags=re.DOTALL,
        count=1,
    )
    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  ok                 : {filepath.name}")
    else:
        print(f"  no change          : {filepath.name}")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=== REST API pages ===")
    for f in sorted(REST_DIR.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        process_rest_file(f)

    print("\n=== SOAP API pages ===")
    for f in sorted(SOAP_DIR.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        process_soap_file(f)

    print("\nDone.")

if __name__ == "__main__":
    main()
