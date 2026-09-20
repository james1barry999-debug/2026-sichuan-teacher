# -*- coding: utf-8 -*-
import re, sys, subprocess, os, json
from html.parser import HTMLParser
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = open(os.path.join(ROOT,'out','心理学12_学习小镇.html'), encoding='utf-8').read()
h_noimg = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', 'IMG', h)

VOID = {'meta','link','img','br','hr','input','source','wbr','path','rect','circle','line','ellipse','polygon','polyline','use','stop'}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack=[]; self.errs=[]; self.ids=[]
    def handle_starttag(self, tag, attrs):
        for k,v in attrs:
            if k=='id': self.ids.append(v)
        if tag in VOID: return
        self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs):
        for k,v in attrs:
            if k=='id': self.ids.append(v)
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack: self.errs.append(('extra close', tag, self.getpos())); return
        t,pos = self.stack.pop()
        if t != tag:
            self.errs.append(('mismatch', t, pos, 'closed by', tag, self.getpos()))
            # try to recover
            while self.stack and self.stack[-1][0]!=tag: self.stack.pop()
            if self.stack: self.stack.pop()
p = P(); p.feed(h_noimg)
print('tag errors:', p.errs[:10], '| unclosed:', p.stack[:10])
dup = [i for i in set(p.ids) if p.ids.count(i)>1]
print('duplicate ids:', dup)
hrefs = set(re.findall(r'href="#([^"]+)"', h_noimg))
missing = sorted(x for x in hrefs if x not in set(p.ids))
print('hrefs without id:', missing)

# quiz checks
quizzes = re.findall(r'<div class="quiz glass" data-a="(\d+)" data-id="(Q\d+)">(.*?)<button class="q-again">', h_noimg, re.S)
ids=[q[1] for q in quizzes]
print('quizzes:', len(quizzes), 'unique ids:', len(set(ids)))
bad=[]
for a,qid,body in quizzes:
    opts = re.findall(r'<li>(.*?)</li>', re.search(r'<ul class="q-opts[^"]*">(.*?)</ul>', body, re.S).group(1), re.S)
    if int(a) >= len(opts): bad.append((qid,a,len(opts)))
    if len(set(opts))!=len(opts): bad.append((qid,'dup opts'))
    if '<div class="q-exp">' not in body: bad.append((qid,'no exp'))
print('quiz problems:', bad)
seq = sorted(int(x[1:]) for x in ids)
print('quiz ids continuous 1..41:', seq == list(range(1,42)))

# JS syntax
js = re.search(r'<script>(.*?)</script>', h_noimg, re.S).group(1)
open('/tmp/town.js','w').write(js)
r = subprocess.run(['node','--check','/tmp/town.js'], capture_output=True, text=True)
print('node --check:', 'OK' if r.returncode==0 else r.stderr[:500])

# fullwidth punctuation in JS code (outside strings) quick check
for m in re.finditer(r'[（）：，；]', js):
    ctx = js[max(0,m.start()-20):m.end()+20]
    if not re.search(r"['\"]", ctx): print('fullwidth in js?', repr(ctx))

# cards count
print('cards:', len(re.findall(r'<article class="kc glass"', h_noimg)))
print('svg figures:', len(re.findall(r'<svg', h_noimg)))
print('size KB:', len(h)//1024)
