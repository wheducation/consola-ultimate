#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Descarga los assets del CDN según assets-manifest.txt → assets/"""
import os, sys, requests

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}
os.makedirs('assets', exist_ok=True)
fallos = []
for line in open('assets-manifest.txt', encoding='utf-8'):
    line = line.strip()
    if not line: continue
    name, url = line.split('\t')
    dest = os.path.join('assets', name)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        continue
    try:
        r = requests.get(url, headers=UA, timeout=60)
        r.raise_for_status()
        open(dest, 'wb').write(r.content)
        print('ok ', name)
    except Exception as e:
        print('FALLO', name, e)
        fallos.append(name)

# parchear url() relativos en los CSS del tema
for f in os.listdir('assets'):
    if f.endswith('.css'):
        p = os.path.join('assets', f)
        css = open(p, encoding='utf-8', errors='ignore').read()
        c2 = css.replace('url(./sparkle.gif)', 'url(sparkle.gif)')
        c2 = c2.replace('url(./', 'url(https://consolaultimate.shop/cdn/shop/t/17/assets/')
        if c2 != css:
            open(p, 'w', encoding='utf-8').write(c2)

if fallos:
    print('ADVERTENCIA: fallaron', len(fallos), 'archivos:', fallos)
    if len(fallos) > 5: sys.exit(1)
