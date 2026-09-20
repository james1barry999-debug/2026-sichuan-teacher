# -*- coding: utf-8 -*-
"""知识点清单式审计：每条知识点的每个关键词组至少命中一个同义词才算覆盖。"""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from points import P, Q
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = open(os.path.join(ROOT,'out','心理学12_学习小镇.html'), encoding='utf-8').read()
h = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', '', h)
txt = re.sub(r'<[^>]+>', '', h)
def N(s): return re.sub(r'[\s\u3000]+', '', s)
T = N(txt)
miss=[]
for pid, name, groups, src in P:
    for g in groups:
        if not any(N(k) in T for k in g):
            miss.append((pid, name, g, src))
print('知识点总数', len(P), '｜ 未覆盖组', len(miss))
for m in miss: print('  MISS', m)
covered = len(P) - len(set(m[0] for m in miss))
print(f'知识点覆盖：{covered}/{len(P)}')
qm=[]
for qid, stem, ans in Q:
    if N(stem) not in T: qm.append((qid,'stem',stem))
    if N(ans) not in T: qm.append((qid,'ans',ans))
print('真题总数', len(Q), '｜ 缺', qm)
