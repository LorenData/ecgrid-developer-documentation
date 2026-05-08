#!/usr/bin/env python3
"""
Append a dated entry to the AI Attribution comment in all files modified
by add_tabs.py (files that contain <Tabs in docs/rest-api and docs/soap-api).
"""

import re
from pathlib import Path

DOCS_DIR = Path(r"E:\LD_Code\ECGrid Developer Documentation Portal\website\docs")
REST_DIR = DOCS_DIR / "rest-api"
SOAP_DIR = DOCS_DIR / "soap-api"

DATE = "2026-05-07"
DEVELOPER = "Greg Kolinski"
ENTRY = f"{DATE}: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - {DEVELOPER}"

SKIP_FILES = {"overview.md"}


def update_attribution(filepath: Path) -> None:
    content = filepath.read_text(encoding="utf-8")

    # Only update files that have tabs (i.e., were modified by add_tabs.py)
    if "<Tabs" not in content:
        return

    # Match the single-line attribution comment: {/* ... */}
    # Pattern ends with | or newline before */}
    m = re.search(r"(\{/\* AI Attribution[^\n]*?)(\s*\*/\})", content)
    if not m:
        return

    existing_text = m.group(1)
    closing = m.group(2)

    # Skip if this entry was already added
    if ENTRY in existing_text:
        print(f"  already updated : {filepath.name}")
        return

    # Append the new entry before the closing */}
    new_comment = existing_text + "\n    " + ENTRY + closing
    new_content = content[:m.start()] + new_comment + content[m.end():]

    filepath.write_text(new_content, encoding="utf-8")
    print(f"  ok              : {filepath.name}")


def main():
    print("=== Updating attribution in REST API pages ===")
    for f in sorted(REST_DIR.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        update_attribution(f)

    print("\n=== Updating attribution in SOAP API pages ===")
    for f in sorted(SOAP_DIR.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        update_attribution(f)

    print("\nDone.")


if __name__ == "__main__":
    main()
