import { chromium } from '/tmp/pwtest/node_modules/playwright/index.mjs';
const file = 'file://' + process.cwd() + '/out/心理学12_学习小镇.html';
const browser = await chromium.launch();
async function shot(name, opts, actions){
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type()==='error') errors.push(m.text()); });
  await page.goto(file); await page.addStyleTag({content:'html{scroll-behavior:auto!important}'}); await page.waitForTimeout(400);
  if (actions) await actions(page);
  await page.screenshot({ path: `build/shots/${name}.png`, fullPage: false });
  console.log(name, 'errors:', errors);
  await ctx.close();
}
await shot('01_hero_map', { viewport:{width:1280,height:1100} });
await shot('02_card_light', { viewport:{width:1280,height:1000} }, async p => { await p.evaluate(()=>document.getElementById('k12').scrollIntoView({behavior:'instant',block:'start'})); await p.waitForTimeout(700); });
await shot('03_card_dark', { viewport:{width:1280,height:1000}, colorScheme:'dark' }, async p => { await p.evaluate(()=>document.getElementById('k53').scrollIntoView({behavior:'instant',block:'start'})); await p.waitForTimeout(700); });
await shot('04_quiz_interact', { viewport:{width:1280,height:900} }, async p => {
  await p.evaluate(()=>document.getElementById('q-s1').scrollIntoView({behavior:'instant',block:'start'}));
  await p.click('[data-id="Q04"] .q-opts li:nth-child(3)'); // wrong answer C
  await p.click('[data-id="Q02"] .q-opts li:nth-child(2)'); // right
  await p.waitForTimeout(700);
  const res = await p.evaluate(()=>({
    q4: document.querySelector('[data-id="Q04"]').className,
    q2: document.querySelector('[data-id="Q02"]').className,
    wrong: document.querySelectorAll('#wrong-box .quiz').length,
    stats: [document.getElementById('st-answered').textContent, document.getElementById('st-right').textContent]
  }));
  console.log('quiz state', JSON.stringify(res));
});
await shot('05_mobile', { viewport:{width:390,height:844}, deviceScaleFactor:2, isMobile:true, hasTouch:true }, async p => { await p.evaluate(()=>document.getElementById('k44').scrollIntoView({behavior:'instant',block:'start'})); await p.waitForTimeout(700); });
await shot('06_recite_arena', { viewport:{width:1280,height:1000} }, async p => {
  await p.evaluate(()=>document.getElementById('recite').scrollIntoView({behavior:'instant',block:'start'}));
  await p.click('#cz-all');
  await p.waitForTimeout(700);
});
await shot('07_arena', { viewport:{width:1280,height:1000} }, async p => {
  await p.click('[data-pass="s1"]'); await p.click('[data-pass="s2"]');
  await p.evaluate(()=>document.getElementById('arena').scrollIntoView({behavior:'instant',block:'start'}));
  await p.click('#arena-start'); await p.waitForTimeout(700);
  const n = await p.evaluate(()=>document.querySelectorAll('#arena-box .quiz').length);
  const pb = await p.evaluate(()=>document.getElementById('pbar').style.width);
  console.log('arena quizzes', n, 'progress', pb);
});
await browser.close();
