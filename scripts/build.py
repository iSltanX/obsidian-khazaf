#!/usr/bin/env python3
"""يبني theme.css من src/*.css (بالترتيب الأبجدي) ويضمّن الخطوط base64 من fonts/fonts.json،
ثم ينسخ الثيم إلى test-vault/.obsidian/themes/Khazaf/ ليُفتح في Obsidian مباشرة."""
import base64, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, FONTS = ROOT / "src", ROOT / "fonts"
manifest = json.loads((ROOT / "manifest.json").read_text())

header = f"""/* ============================================================
   Khazaf — خَزَف · Arabic-first Obsidian theme   v{manifest['version']}
   مريمية وطين: أسطح ضبابية باردة، حبر أردوازي، لمسة طينية للتحديد.
   مبني من src/*.css بواسطة scripts/build.py — لا تحرّر هذا الملف يدويًا.
   الخطوط المضمّنة: Vazirmatn، Markazi Text، JetBrains Mono (SIL OFL 1.1، انظر fonts/OFL.txt)
   ============================================================ */
"""

faces = []
meta = json.loads((FONTS / "fonts.json").read_text()) if (FONTS / "fonts.json").exists() else []
for f in meta:
    b64 = base64.b64encode((FONTS / f["file"]).read_bytes()).decode()
    faces.append(
        "@font-face {\n"
        f"  font-family: '{f['family']}';\n  font-style: normal;\n  font-weight: {f['weight']};\n  font-display: swap;\n"
        f"  src: url(data:font/woff2;base64,{b64}) format('woff2');\n"
        f"  unicode-range: {f['unicodeRange']};\n}}\n")
fonts_css = "/* ---------- 00 الخطوط المضمّنة ---------- */\n" + "".join(faces) if faces else "/* (no embedded fonts — run scripts/fetch-fonts.py) */\n"

parts = [header, fonts_css]
for p in sorted(SRC.glob("*.css")):
    parts.append(f"\n/* ---------- {p.stem} ---------- */\n" + p.read_text())
out = "\n".join(parts)
(ROOT / "theme.css").write_text(out)
print(f"theme.css: {len(out)/1024:.0f} KB ({len(meta)} font files embedded)")

dest = ROOT / "test-vault" / ".obsidian" / "themes" / manifest["name"]
dest.mkdir(parents=True, exist_ok=True)
shutil.copy(ROOT / "theme.css", dest / "theme.css")
shutil.copy(ROOT / "manifest.json", dest / "manifest.json")
print("installed into", dest.relative_to(ROOT))
