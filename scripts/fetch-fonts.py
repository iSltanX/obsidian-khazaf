#!/usr/bin/env python3
"""يجلب ملفات woff2 (متغيّرة الوزن) من Google Fonts للخطوط الثلاثة، ويحتفظ بمجموعتي arabic وlatin فقط.
يكتب fonts/*.woff2 و fonts/fonts.json (الوصف الذي يستخدمه build.py)."""
import json, re, sys, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
FONTS.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
URL = ("https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300..700"
       "&family=Markazi+Text:wght@400..700&family=JetBrains+Mono:wght@400..600&display=swap")
KEEP = {"arabic", "latin"}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

css = get(URL).decode()
blocks = re.findall(r"/\* (\w[\w-]*) \*/\s*@font-face\s*\{(.*?)\}", css, re.S)
out = []
for subset, body in blocks:
    if subset not in KEEP:
        continue
    fam = re.search(r"font-family:\s*'([^']+)'", body).group(1)
    weight = re.search(r"font-weight:\s*([\d ]+);", body).group(1).strip()
    src = re.search(r"url\(([^)]+\.woff2)\)", body).group(1)
    urange = re.search(r"unicode-range:\s*([^;]+);", body).group(1).strip()
    slug = fam.lower().replace(" ", "-") + "-" + subset + ".woff2"
    data = get(src)
    (FONTS / slug).write_bytes(data)
    out.append({"family": fam, "subset": subset, "weight": weight, "file": slug, "unicodeRange": urange, "bytes": len(data)})
    print(f"{slug:36} {len(data)/1024:7.1f} KB  weight {weight}")

(FONTS / "fonts.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print("total", sum(o["bytes"] for o in out) // 1024, "KB")

# تقليص الخطوط إلى الحروف المستخدمة (يحتاج fonttools وbrotli)
import subprocess, sys
subprocess.run([sys.executable, str(ROOT / "scripts" / "subset-fonts.py")], check=True)
