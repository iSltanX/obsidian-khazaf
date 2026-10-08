#!/usr/bin/env python3
"""يقلّص ملفات الخطوط في fonts/ إلى الحروف التي يحتاجها الثيم، ويحدّث unicodeRange في fonts.json.
يُبقي خصائص التشكيل (GSUB/GPOS) ومحور الوزن المتغيّر كاملين. آمن للتشغيل أكثر من مرة.
يتطلب: pip install fonttools brotli"""
import json, pathlib
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"

# العربية: الحروف والحركات والأرقام وعلامات الترقيم، وأشكال العرض-ب الشائعة في النص المنسوخ من PDF،
# وﷲ ﷺ والبسملة. تُحذف حروف الفارسية والأردية وكتل الامتداد؛ إن ظهرت يرسمها خط النظام.
ARABIC = [
    (0x0020, 0x0020), (0x00A0, 0x00A0),
    (0x060C, 0x060C), (0x061B, 0x061B), (0x061F, 0x061F),
    (0x0621, 0x063A), (0x0640, 0x0655), (0x0660, 0x066D), (0x0670, 0x0671),
    (0x200C, 0x200F), (0x25CC, 0x25CC),
    (0xFDF2, 0xFDF2), (0xFDFA, 0xFDFA), (0xFDFD, 0xFDFD),
    (0xFE70, 0xFE74), (0xFE76, 0xFEFC),
]
# اللاتينية: الأساسية وLatin-1 وعلامات الترقيم العامة وبعض الرموز التي يستخدمها الثيم (↩ ← →).
LATIN = [
    (0x0020, 0x007E), (0x00A0, 0x00FF), (0x0131, 0x0131), (0x0152, 0x0153),
    (0x02C6, 0x02C6), (0x02DA, 0x02DA), (0x02DC, 0x02DC),
    (0x2000, 0x206F), (0x20AC, 0x20AC), (0x2122, 0x2122),
    (0x2190, 0x2193), (0x21A9, 0x21A9), (0x2212, 0x2212), (0xFEFF, 0xFEFF), (0xFFFD, 0xFFFD),
]
RANGES = {"arabic": ARABIC, "latin": LATIN}


def to_unicode_range(ranges):
    out = []
    for a, b in ranges:
        out.append(f"U+{a:04X}" if a == b else f"U+{a:04X}-{b:04X}")
    return ", ".join(out)


meta = json.loads((FONTS / "fonts.json").read_text())
total_before = total_after = 0
for f in meta:
    path = FONTS / f["file"]
    before = path.stat().st_size
    ranges = RANGES[f["subset"]]
    unicodes = [u for a, b in ranges for u in range(a, b + 1)]
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    opts.glyph_names = False
    opts.hinting = False
    font = TTFont(str(path))
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=unicodes)
    sub.subset(font)
    font.flavor = "woff2"
    font.save(str(path))
    after = path.stat().st_size
    f["bytes"] = after
    f["unicodeRange"] = to_unicode_range(ranges)
    total_before += before
    total_after += after
    print(f"{f['file']:32} {before/1024:6.1f} KB -> {after/1024:6.1f} KB")

(FONTS / "fonts.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
print(f"total {total_before/1024:.0f} KB -> {total_after/1024:.0f} KB")
