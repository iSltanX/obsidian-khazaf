<p align="center">
  <img src="docs/images/banner.png" alt="Khazaf — an Arabic-first Obsidian theme" width="100%">
</p>

<p align="center">
  <a href="#english">English</a> ·
  <a href="https://github.com/iSltanX/obsidian-khazaf/releases">Releases</a> ·
  <a href="CHANGELOG.md">Changelog</a>
</p>

<div dir="rtl">

# خَزَف · Khazaf

ثيم Obsidian مصمَّم للكتابة العربية الطويلة. الاسم من الخزف: طينٌ مشويّ وطلاءٌ بلون المريمية. سطح ضبابي هادئ، وحبر أردوازي مريح للقراءة، ولمسة طينية واحدة تُعلِّم ما يهمّ: الرابط، والعنصر المحدد، ومرجع الحاشية.

## لماذا خزف؟

- **عربي أولًا.** الواجهة معكوسة كاملة، والمتن بخط Vazirmatn بحجم 17 وتباعد أسطر 1.75 حتى لا تتصادم الحركات بين الأسطر.
- **حواشٍ تليق بالعربية.** المرجع رقم صغير بلا أقواس، والقائمة أسفل الملاحظة بخط أصغر، ورابط العودة ↩ بعد النص.
- **بيت الشعر.** صدر وعجز متقابلان بخط نسخي، ويتراصّان تلقائيًا على الشاشات الضيقة.
- **كود لا ينقلب.** كتل الكود من اليسار دائمًا داخل الملاحظة العربية، وتتمرّر أفقيًا على الهاتف بدل أن تنكسر.
- **لا يحتاج شيئًا آخر.** الخطوط الثلاثة مضمّنة داخل الثيم، فيعمل كما هو على الحاسب والهاتف، بلا إضافات.

## الصور

لقطات حقيقية من Obsidian 1.14.4 بواجهة عربية.

| المعاينة الحية · داكن | وضع المصدر · فاتح |
|---|---|
| ![المعاينة الحية بالوضع الداكن](docs/screenshots/live-preview-dark.png) | ![وضع المصدر بالوضع الفاتح](docs/screenshots/source-mode-light.png) |
| **القراءة · داكن** | **المبدّل السريع · فاتح** |
| ![القراءة بالوضع الداكن مع كود وبيت شعر وجدول](docs/screenshots/reading-dark.png) | ![المبدّل السريع](docs/screenshots/quick-switcher-light.png) |

<p align="center">
  <img src="docs/screenshots/mobile-reading-light.png" alt="الهاتف: قراءة فاتح" width="24%">
  <img src="docs/screenshots/mobile-reading-dark.png" alt="الهاتف: قراءة داكن" width="24%">
  <img src="docs/screenshots/mobile-drawer-light.png" alt="الهاتف: درج الملفات" width="24%">
</p>

## اللوحة والخطوط

![لوحة مريمية وطين بالوضعين](docs/images/palette.png)

![الخطوط الثلاث: Markazi Text وVazirmatn وJetBrains Mono](docs/images/typography.png)

## التثبيت

**من داخل Obsidian:** بعد قبول الثيم في دليل الثيمات، افتح الإعدادات ← المظهر ← الثيمات ← إدارة، وابحث عن **Khazaf**.

**يدويًا:** نزّل `theme.css` و`manifest.json` من [آخر إصدار](https://github.com/iSltanX/obsidian-khazaf/releases/latest)، وضعهما في المجلد:

```
<قبوك>/.obsidian/themes/Khazaf/
```

ثم اختر Khazaf من الإعدادات ← المظهر.

### إعدادات تكمّل الثيم

هذه إعدادات في Obsidian نفسه، والثيم لا يفرضها:

| الإعداد | المكان | لماذا |
|---|---|---|
| لغة الواجهة: العربية | عام ← اللغة | تعكس الأشرطة والقوائم (يحتاج إعادة تشغيل) |
| من اليمين إلى اليسار | المحرر | يجعل الاتجاه الافتراضي للمحرر عربيًا |
| حجم الخط 17 | المظهر ← حجم الخط | الحجم الذي صُمّم عليه الثيم |
| طول السطر المقروء | المحرر | سطر بعرض 700px، نحو 70 إلى 85 حرفًا |

## بيت الشعر

اكتب البيت جدولًا بعمودين داخل تنبيه من نوع `verse`:

```markdown
> [!verse]
> | | |
> |---|---|
> | وما نَيْلُ المطالبِ بالتمنّي | ولكنْ تُؤخَذُ الدنيا غِلابا |
> | وما استعصى على قومٍ منالٌ | إذا الإقدامُ كان لهم رِكابا |
```

![بيت الشعر في وضع القراءة](docs/screenshots/verse-light.png)

الملاحظة نفسها تبقى Markdown عاديًا، ويظهر الجدول عاديًا إن غيّرت الثيم.

## قيود معروفة

هذه من Obsidian نفسه، وتظهر مع الثيم الافتراضي أيضًا:

- حقل التاريخ في الخصائص يظهر فارغًا وبحروف معكوسة في الواجهة العربية.
- السطر الذي يبدأ بحرف لاتيني، مثل `> [!tip] نصيحة`، يُعرض في المحرر من اليسار، لأن Obsidian يحدد اتجاه كل سطر من أول حرف فيه.

## التطوير

```
src/            مصدر الثيم مقسّمًا (المتغيرات، المتن، الواجهة، RTL، الهاتف، وضع المصدر)
fonts/          ملفات الخطوط ورخصتها
scripts/        جلب الخطوط، البناء، وأداة فحص داخل Obsidian
test-vault/     قبو تجريبي بملاحظات عربية حقيقية
docs/           الصور ولقطات التصميم
theme.css       ناتج البناء (لا تحرّره يدويًا)
```

```bash
python3 scripts/fetch-fonts.py   # مرة واحدة
python3 scripts/build.py         # بعد كل تعديل في src/
```

البناء ينسخ الثيم إلى `test-vault`، فافتح هذا المجلد في Obsidian كقبو لتجربة التعديلات.

للإصدار: ارفع رقم `version` في `manifest.json`، ثم ادفع وسمًا بالرقم نفسه (مثل `0.1.1`)، فينشئ GitHub Actions مسودة إصدار فيها `theme.css` و`manifest.json`.

التصميم الكامل (الأسس، المكونات، الشاشات، ملاحظات التنفيذ) في ملف Figma خاص بالمشروع، ولقطاته في [docs/design](docs/design).

## الرخصة

كود الثيم برخصة [MIT](LICENSE). الخطوط المضمّنة (Vazirmatn، Markazi Text، JetBrains Mono) برخصة [SIL OFL 1.1](fonts/OFL.txt)، وحقوقها في [fonts/NOTICE.md](fonts/NOTICE.md).

</div>

---

<a id="english"></a>

## English

**Khazaf** (Arabic for *ceramic*: fired clay with a sage glaze) is an Arabic-first theme for Obsidian. Misty surfaces, slate ink and a single terracotta accent for links, selection and footnote references.

- Fully mirrored RTL interface; body text in Vazirmatn at 17px with 1.75 line height so diacritics never collide.
- Footnotes rendered as bracket-less superscript numbers, a smaller footnote list and a ↩ back-link.
- A `> [!verse]` callout that lays out classical Arabic poetry in two hemistichs and stacks them on narrow screens.
- Code blocks always LTR, scrolling horizontally on mobile.
- Light and dark modes; Obsidian's pure-black mobile dark surfaces are replaced with slate.
- Fonts (Vazirmatn, Markazi Text, JetBrains Mono) are embedded as WOFF2, so the theme works offline and on mobile with no plugins.

Tested on Obsidian 1.14.4 (desktop, and mobile emulation) with the Arabic interface. Theme code is MIT; bundled fonts are SIL OFL 1.1.
