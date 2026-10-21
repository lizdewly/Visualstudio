const { chromium } = require('C:/Users/김세원/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { pathToFileURL } = require('node:url');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const source = 'C:/Users/김세원/김세원2/001_AI4_1019/05.FastAPI-uvicorn/assets/FastAPI_이론실습교안.html';
  const output = path.resolve('output/pdf/FastAPI_이론실습교안.pdf');
  fs.mkdirSync(path.dirname(output), { recursive: true });
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(source).href, { waitUntil: 'load' });
    await page.evaluate(async () => {
      await document.fonts.ready;
      document.querySelectorAll('details').forEach(el => el.open = true);
      for (const img of document.images) {
        if (!img.complete) await new Promise(resolve => { img.onload = resolve; img.onerror = resolve; });
        if (!img.naturalWidth) {
          const note = document.createElement('p');
          note.textContent = `[원본 이미지 파일 누락: ${img.getAttribute('src')}]`;
          note.style.cssText = 'font-size:9pt;color:#52677c;border:1px solid #d6e1ea;padding:10px';
          img.replaceWith(note);
        }
      }
    });
    await page.addStyleTag({ content: `@media print {
      @page { size: A4; }
      h2,h3,h4 { break-after:avoid; }
      pre { overflow:visible; }
      thead { display:table-header-group; }
      a { text-decoration:none; }
      body { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
    }` });
    await page.pdf({ path: output, format:'A4', printBackground:true,
      margin: { top:'16mm', bottom:'18mm', left:'16mm', right:'16mm' },
      displayHeaderFooter:true, headerTemplate:'<div></div>',
      footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#52677c;font-family:Arial"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
    console.log(output);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
