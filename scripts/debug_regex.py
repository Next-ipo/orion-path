import os
import re

LOG_FILE = r"h:\2nd-Brain\05_日誌\2026-03-22.md"
with open(LOG_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Debug: Find lines with Artemis II
print("--- Debug Lines ---")
for line in content.splitlines():
    if "Artemis II" in line:
        print(f"[{line}]")

print("--- Regex Test ---")
patterns = [
    r"Artemis II.*?\u6700\u65b0\u72b6\u6cc1.*?[:：]\s*([^\n\*]+)",
    r"Artemis II.*?\u6700\u65b0\u72b6\u6cc1\*\*[:：]\s*(.*)",
    r"Artemis II.*?\uff1a\s*(.*)" # Using unicode for :
]

for p in patterns:
    m = re.search(p, content)
    if m:
        print(f"Pattern [{p}] matched: [{m.group(1).strip()}]")
    else:
        print(f"Pattern [{p}] failed.")
