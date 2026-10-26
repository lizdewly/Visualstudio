const {chromium} = require('C:/Users/김세원/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({headless:true,channel:'chrome'});
  const page = await browser.newPage();
  const errors=[];
  page.on('pageerror', e=>errors.push(e.message));
  const checks=[];
  for (const width of [1440,768,375,320]) {
    await page.setViewportSize({width,height:1000});
    await page.goto('http://127.0.0.1:8011/',{waitUntil:'networkidle'});
    const result=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,imageLoaded:document.querySelector('.hero-image').naturalWidth>0,background:getComputedStyle(document.body).backgroundColor,columns:getComputedStyle(document.querySelector('.content-grid')).gridTemplateColumns}));
    if(result.overflow || !result.imageLoaded) throw Error(JSON.stringify({width,...result}));
    checks.push({width,...result});
    if(width===1440) await page.screenshot({path:__dirname+'/preview-dark-desktop.png',fullPage:true});
    if(width===375) await page.screenshot({path:__dirname+'/preview-dark-mobile.png',fullPage:true});
  }
  await page.locator('#name').fill('디자인 확인');
  await page.locator('#message').fill('새로운 디자인에서도 한글 방명록이 정상적으로 등록됩니다.');
  await Promise.all([page.waitForURL('**/?saved=true'),page.locator('button[type=submit]').click()]);
  if(!(await page.locator('.message').first().textContent()).includes('한글 방명록')) throw Error('registration failed');
  console.log(JSON.stringify({checks,registration:true,errors}));
  await browser.close();
})();
