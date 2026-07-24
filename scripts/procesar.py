#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logos del carrusel sin fondo blanco. Las demás imágenes quedan originales."""
import os, glob
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

for f in sorted(glob.glob('assets/*300x151*.webp')):
    im = quitar_fondo(f)
    im.save(f, 'WEBP', quality=95)
    print('logo sin fondo:', os.path.basename(f))
