import { chromium } from '/tmp/pwtest/node_modules/playwright/index.mjs';
const file = 'file://' + process.cwd() + '/out/心理学12_学习小镇.html';
const browser = await chromium.launch();
const page = await (await browser.newContext({viewport:{width:1280,height:900}})).newPage();
await page.goto(file); await page.addStyleTag({content:'html{scroll-behavior:auto!important}'});
for (const id of ['k15','k43','k55','k58','k61']) {
  const el = await page.$('#'+id+' .kc-fig svg');
  await el.screenshot({path:`build/shots/fig_${id}.png`});
}
const map = await page.$('#map svg'); await map.screenshot({path:'build/shots/fig_map.png'});
await browser.close(); console.log('done');
