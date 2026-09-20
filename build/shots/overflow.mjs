import { chromium } from '/tmp/pwtest/node_modules/playwright/index.mjs';
const file = 'file://' + process.cwd() + '/out/心理学12_学习小镇.html';
const browser = await chromium.launch();
const page = await (await browser.newContext({viewport:{width:1280,height:900}})).newPage();
await page.goto(file);
const bad = await page.evaluate(()=>{
  const out=[];
  document.querySelectorAll('svg').forEach((svg,si)=>{
    const vb = svg.viewBox.baseVal; const W=vb.width, H=vb.height;
    const art = svg.closest('article, section'); const id = art ? art.id : 'svg'+si;
    svg.querySelectorAll('text').forEach(t=>{
      const b = t.getBBox();
      if (b.x < -2 || b.x + b.width > W + 2 || b.y < -2 || b.y + b.height > H + 2)
        out.push({id, text:t.textContent.slice(0,40), x:Math.round(b.x), r:Math.round(b.x+b.width), W});
    });
  });
  return out;
});
console.log(JSON.stringify(bad,null,1));
await browser.close();
