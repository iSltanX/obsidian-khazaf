#!/usr/bin/env bash
# يثبّت إضافتي Style Settings وDataview في test-vault لتجربة دعم الثيم لهما.
# الإضافات لا تُرفع للمستودع (انظر .gitignore). يحتاج gh مسجّل الدخول.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUG="$ROOT/test-vault/.obsidian/plugins"
install() { # repo id
  local repo="$1" id="$2"
  mkdir -p "$PLUG/$id"
  gh release download --repo "$repo" --pattern 'main.js' --pattern 'manifest.json' --pattern 'styles.css' --dir "$PLUG/$id" --clobber 2>/dev/null \
    || gh release download --repo "$repo" --pattern 'main.js' --pattern 'manifest.json' --dir "$PLUG/$id" --clobber
  echo "installed $id $(python3 -c "import json;print(json.load(open('$PLUG/$id/manifest.json'))['version'])")"
}
install obsidian-community/obsidian-style-settings obsidian-style-settings
install blacksmithgu/obsidian-dataview dataview
printf '[\n  "obsidian-style-settings",\n  "dataview"\n]\n' > "$ROOT/test-vault/.obsidian/community-plugins.json"
