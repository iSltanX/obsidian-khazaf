// عميل CDP بسيط لفحص الثيم داخل Obsidian المفتوح بـ --remote-debugging-port=9222
// الاستخدام:
//   node scripts/cdp.mjs eval "<js expression>"
//   node scripts/cdp.mjs shot out.png [width height]
//   node scripts/cdp.mjs size <width> <height>     (محاكاة حجم نافذة؛ 0 0 لإلغائها)
const PORT = process.env.CDP_PORT || 9222;
const [cmd, ...args] = process.argv.slice(2);

const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
// CDP_TITLE يختار نافذة بجزء من عنوانها (مثل نافذة الإعدادات المستقلة في Obsidian 1.14)
const byTitle = process.env.CDP_TITLE && targets.find(t => t.type === "page" && (t.title || "").includes(process.env.CDP_TITLE));
const page = byTitle || targets.find(t => t.type === "page" && /app:\/\/obsidian\.md\/index\.html/.test(t.url)) || targets.find(t => t.type === "page");
if (!page) { console.error("no page target", targets.map(t => t.url)); process.exit(1); }

const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let id = 0; const pending = new Map();
ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } };
const send = (method, params = {}) => new Promise(res => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });

if (cmd === "eval") {
  const r = await send("Runtime.evaluate", { expression: args[0], awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) console.error(JSON.stringify(r.result.exceptionDetails, null, 1));
  console.log(JSON.stringify(r.result?.result?.value ?? r.result?.result, null, 1));
} else if (cmd === "winsize") {
  // يغيّر حجم نافذة Obsidian الفعلية (يبقى بعد إغلاق الاتصال)
  const [w, h] = args.map(Number);
  const win = await send("Browser.getWindowForTarget");
  const r = await send("Browser.setWindowBounds", { windowId: win.result.windowId, bounds: { width: w, height: h, windowState: "normal" } });
  console.log(r.error ? JSON.stringify(r.error) : "ok");
} else if (cmd === "size") {
  const [w, h] = args.map(Number);
  if (!w) await send("Emulation.clearDeviceMetricsOverride");
  else await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  console.log("ok");
} else if (cmd === "shot") {
  // الحجم يُطبَّق داخل الجلسة نفسها لأن المحاكاة تُلغى عند إغلاق الاتصال
  const [w, h] = args.slice(1).map(Number);
  if (w) {
    await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
    await new Promise(r => setTimeout(r, 900));
  }
  const r = await send("Page.captureScreenshot", { format: "png" });
  const fs = await import("node:fs");
  fs.writeFileSync(args[0], Buffer.from(r.result.data, "base64"));
  console.log("saved", args[0]);
} else if (cmd === "shotel") {
  // node scripts/cdp.mjs shotel "<css selector>" out.png [pad]
  const pad = Number(args[2] || 12);
  const r0 = await send("Runtime.evaluate", { expression: `(()=>{const e=document.querySelector(${JSON.stringify(args[0])}); if(!e) return null; e.scrollIntoView({block:'center'}); const b=e.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height}})()`, returnByValue: true });
  const b = r0.result?.result?.value;
  if (!b) { console.error("selector not found", args[0]); process.exit(1); }
  await new Promise(r => setTimeout(r, 300));
  const r1 = await send("Runtime.evaluate", { expression: `(()=>{const b=document.querySelector(${JSON.stringify(args[0])}).getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height}})()`, returnByValue: true });
  const c = r1.result.result.value;
  const r = await send("Page.captureScreenshot", { format: "png", clip: { x: Math.max(0, c.x - pad), y: Math.max(0, c.y - pad), width: c.w + pad * 2, height: c.h + pad * 2, scale: 1 } });
  const fs = await import("node:fs");
  fs.writeFileSync(args[1], Buffer.from(r.result.data, "base64"));
  console.log("saved", args[1], c);
} else {
  console.error("unknown command", cmd);
}
ws.close();
