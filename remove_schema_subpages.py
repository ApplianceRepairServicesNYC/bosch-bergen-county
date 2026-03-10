#!/usr/bin/env python3
import re
from pathlib import Path
import sys

BASE_DIR = Path(sys.argv[0]).parent.resolve()

def remove_schema(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    pattern = r'\s*<script type="application/ld\+json">[\s\S]*?</script>\s*'
    new_content = re.sub(pattern, '\n', content)
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

html_files = list(BASE_DIR.rglob('index.html'))
homepage = BASE_DIR / 'index.html'
removed = 0
for f in html_files:
    if f == homepage or 'assets' in str(f):
        continue
    if remove_schema(f):
        removed += 1
print(f"Removed Schema from {removed} subpages, kept homepage only")
