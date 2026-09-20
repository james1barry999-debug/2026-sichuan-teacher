# -*- coding: utf-8 -*-
"""拼装 build/parts/*.html → out/心理学12_学习小镇.html，并把 3 张原板书图嵌入。"""
import base64, glob, io, os, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parts = sorted(glob.glob(os.path.join(ROOT, 'build', 'parts', '*.html')))
html = ''.join(open(p, encoding='utf-8').read() for p in parts)

def b64(sid, width=1000, q=78):
    p = os.path.join(ROOT, 'sl', 'slides', sid + '.jpg')
    im = Image.open(p).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True)
    return base64.b64encode(buf.getvalue()).decode('ascii')

for sid in re.findall(r'__(S\d{3})__', html):
    html = html.replace('__%s__' % sid, b64(sid))
out = os.path.join(ROOT, 'out', '心理学12_学习小镇.html')
open(out, 'w', encoding='utf-8').write(html)
print(out, len(html)//1024, 'KB', '| parts:', len(parts))
