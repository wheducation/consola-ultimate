#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retoques: logos del carrusel sin fondo + optimización de fotos pesadas."""
import os, glob, subprocess
from PIL import Image, ImageFilter
from collections import deque

def quitar_fondo(path, thr=205):
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    px = im.load()
    def lum(p): return 0.299*p[0]+0.587*p[1]+0.114*p[2]
    bg = [[False]*w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h-1):
            if lum(px[x, y]) > thr and not bg[y][x]: bg[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w-1):
            if lum(px[x, y]) > thr and not bg[y][x]: bg[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and not bg[ny][nx] and lum(px[nx, ny]) > thr:
                bg[ny][nx] = True; q.append((nx, ny))
    mask = Image.new('L', (w, h), 255)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            if bg[y][x]: mp[x, y] = 0
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(mask)
    return im

# 1) logos del carrusel (300x151) → fondo transparente
for f in sorted(glob.glob('assets/*300x151*.webp')):
    im = quitar_fondo(f)
    im.save(f, 'WEBP', quality=95)
    print('logo sin fondo:', os.path.basename(f))

# 2) fotos PNG gigantes → máx 1500px + cuantizar
PESADAS = [
    'hf_20260409_144831_3b1e2a92-9d05-476c-9547-430d3d0be464.png',
    'hf_20260422_135711_1842b168-0f74-4444-bd8a-afee06263b4f.png',
    'hf_20260422_134211_f1962cae-60d8-4f25-b6b0-9a97cf5986c3.png',
    'hf_20260422_130608_988292ad-ae42-45a9-a941-9041eb8c3d43.png',
    'hf_20260422_131342_cfb557df-febe-4b7d-93ed-6f76e8e1ba2f.png',
]
for name in PESADAS:
    p = os.path.join('assets', name)
    if not os.path.exists(p): continue
    im = Image.open(p)
    if max(im.size) > 1500:
        im.thumbnail((1500, 1500), Image.LANCZOS)
    im.save(p, optimize=True)
    r = subprocess.run(['pngquant', '256', '--speed', '1', '--force', '--output', p + '.tmp', p])
    if r.returncode == 0:
        os.replace(p + '.tmp', p)
    print('optimizada:', name, os.path.getsize(p)//1024, 'KB')
