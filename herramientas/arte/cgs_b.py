"""Escenas especiales (CG), portada y menús de EL BRAMADOR."""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from lib import *
import fondos_b as F

CG = OUT + "/cg"
GUI = "/home/claude/bramador/game/gui"
TMP = "/home/claude/bramador/arte/tmp"
os.makedirs(TMP, exist_ok=True)
os.makedirs(CG, exist_ok=True)
os.makedirs(GUI, exist_ok=True)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SERIF_C = "/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Italic.ttf"


def fnt(p, s):
    return ImageFont.truetype(p, s)


def guardar(im, path, grain=6, vignette=0.5, seed=1, tint=None):
    im.convert("RGB").save(path)
    post(path, grain=grain, vignette=vignette, seed=seed, tint=tint)


def papel_viejo(w, h, seed, base=(214, 196, 158)):
    rng = np.random.default_rng(seed)
    a = np.ones((h, w, 3), np.float32) * np.array(base, np.float32)
    n = rng.normal(0, 1, (h // 8 + 1, w // 8 + 1)).astype(np.float32)
    n = np.array(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    a *= (0.86 + 0.18 * n)[..., None]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a *= (1 - 0.35 * np.clip(d - 0.6, 0, 1) ** 1.2)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(capa)
    rnd = random.Random(seed)
    for _ in range(9):
        x, y, r = rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(30, 120)
        dr.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(110, 80, 40, 30))
    for _ in range(3):
        x = rnd.uniform(0.2, 0.8) * w
        dr.line([(x, 0), (x + rnd.uniform(-20, 20), h)], fill=(120, 96, 60, 70), width=3)
    y = rnd.uniform(0.3, 0.7) * h
    dr.line([(0, y), (w, y + rnd.uniform(-10, 10))], fill=(120, 96, 60, 70), width=3)
    capa = capa.filter(ImageFilter.GaussianBlur(6))
    im.alpha_composite(capa)
    # bordes irregulares
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    pts = []
    for i in range(60):
        t = i / 60
        pts.append((t * w, rnd.uniform(0, 14)))
    for i in range(40):
        t = i / 40
        pts.append((w - rnd.uniform(0, 14), t * h))
    for i in range(60):
        t = i / 60
        pts.append(((1 - t) * w, h - rnd.uniform(0, 14)))
    for i in range(40):
        t = i / 40
        pts.append((rnd.uniform(0, 14), (1 - t) * h))
    md.polygon(pts, fill=255)
    im.putalpha(mask)
    return im


def mesa_oscura(seed=3, base=(24, 16, 11)):
    a = np.ones((1080, 1920, 3), np.float32) * np.array(base, np.float32)
    rng = np.random.default_rng(seed)
    vetas = np.cumsum(rng.normal(0, 1, (1080, 1)), 0) * 0.5 + np.sin(np.linspace(0, 50, 1920))[None, :] * 3
    a += vetas[..., None] * np.array([1.0, 0.7, 0.5])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def con_sombra(base, im, pos, blur=18, op=0.65):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.split()[3].point(lambda v: int(v * op)))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (pos[0] + 18, pos[1] + 24))
    base.alpha_composite(im, pos)


def luz_central(base, caja, fuerza=200, color=(255, 214, 150), calido=0.10):
    W_, H_ = base.size
    luz = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(luz).ellipse(caja, fill=255)
    luz = luz.filter(ImageFilter.GaussianBlur(120))
    osc = Image.new("RGBA", (W_, H_), (0, 0, 0, 255))
    osc.putalpha(luz.point(lambda v: int(fuerza - v * fuerza / 255 * 0.95)))
    base.alpha_composite(osc)
    c = Image.new("RGBA", (W_, H_), color + (0,))
    c.putalpha(luz.point(lambda v: int(v * calido)))
    base.alpha_composite(c)


# ---------------------------------------------------------------------------

def escena_titulo(path, con_texto=True, para_menu=False):
    d1 = F.grad("cieloTT", [(0, "#01030a"), (0.6, "#0a1430"), (1, "#22203a")])
    b = [f'<rect width="{W}" height="820" fill="url(#cieloTT)"/>', via_lactea(1400, 160, 900, 170, -20, 601),
         estrellas(800, 602, y_max=640)]
    b.append(cerro(720, 140, 603, "#0b0f17", rim="#2c3e57"))
    b.append(F.cerro_bramador(1180, 820, 1500, 560, "noche", seed=7, detalle=1.3))
    b.append(F.pampa(810, "#0d0b09", "#1b1713", 604, n=140))
    # rendija dorada al pie del manto de arena
    b.append('<path d="M1000,800 L1020,700 L1036,700 L1040,800 Z" fill="#fff0b0"/>')
    b.append('<circle cx="1022" cy="760" r="260" fill="url(#glowOro)" opacity="0.9"/>')
    b.append('<ellipse cx="1022" cy="810" rx="300" ry="40" fill="#f0b93c" opacity="0.25" filter="url(#b16)"/>')
    # silueta del Caballero sobre la arena
    b.append('<g transform="translate(1180,812) scale(0.55)" fill="#050305">'
             '<ellipse cx="0" cy="-330" rx="70" ry="12"/><rect x="-30" y="-380" width="60" height="50" rx="6"/>'
             '<ellipse cx="0" cy="-300" rx="26" ry="32"/>'
             '<path d="M-60,-270 L60,-270 L80,-100 L50,0 L20,0 L10,-110 L-10,-110 L-20,0 L-50,0 L-80,-100 Z"/>'
             '</g>')
    b.append('<path d="M1180,812 L1500,840" stroke="#000" stroke-width="10" opacity="0.4" filter="url(#b4)"/>')
    if para_menu:
        b.append('<rect width="640" height="1080" fill="#000" opacity="0.4"/>')
    if con_texto:
        b.append('<rect x="0" y="330" width="1920" height="300" fill="#000" opacity="0.25" filter="url(#b60)"/>')
        b.append(texto(620, 470, "EL BRAMADOR", 112, fill="#f0e2c0", weight="bold", spacing=12))
        b.append(texto(620, 545, "Una leyenda de Copiapó", 44, fill="#e0b060", style="italic", spacing=3))
        b.append('<rect x="320" y="575" width="600" height="3" fill="#d4a24a"/>')
    render(doc("".join(b), d1 + F.DEFS_FUEGO), path)
    post(path, grain=7, vignette=0.6, tint=((6, 8, 24), (255, 200, 130)), seed=61)


def titulo():
    escena_titulo(f"{CG}/titulo.png")


def menus():
    escena_titulo(f"{GUI}/main_menu.png", con_texto=False, para_menu=True)
    im = Image.open(f"{GUI}/main_menu.png").filter(ImageFilter.GaussianBlur(14))
    ImageEnhance.Brightness(im).enhance(0.42).save(f"{GUI}/game_menu.png")


def derrotero():
    base = mesa_oscura(5)
    w, h = 1300, 900
    pap = papel_viejo(w, h, 71)
    svg = ('<g stroke="#3a2412" fill="none" stroke-linecap="round">'
           # cerro dibujado a pluma
           '<path d="M380,560 C440,420 520,330 600,300 C680,320 760,420 860,560" stroke-width="5"/>'
           '<path d="M420,560 C470,470 540,380 600,330 C590,420 560,500 520,560" stroke-width="3" stroke-dasharray="8 6"/>'
           + "".join(f'<path d="M{450 + k*12},{540 - k*20} l-10,22" stroke-width="2"/>' for k in range(9))
           + '<path d="M150,700 C350,650 700,690 1150,640" stroke-width="4"/>'
           '<path d="M150,720 C350,670 700,710 1150,660" stroke-width="2"/>'
           # quebrada y camino punteado
           '<path d="M1150,320 C1000,380 900,460 860,560" stroke-width="3"/>'
           '<path d="M1100,760 C900,740 700,700 520,600" stroke-width="4" stroke-dasharray="4 14"/>'
           # cruz donde la arena no canta
           '<path d="M500,555 l30,30 M530,555 l-30,30" stroke="#8a1414" stroke-width="7"/>'
           '<circle cx="515" cy="570" r="34" stroke="#8a1414" stroke-width="3"/>'
           # rosa de los vientos
           '<path d="M1110,180 L1110,300 M1050,240 L1170,240" stroke-width="3"/>'
           '<path d="M1110,170 l-12,24 l24,0 Z" fill="#3a2412"/>'
           '</g>'
           + texto(600, 260, "Bramador", 44, fill="#3a2412", style="italic")
           + texto(1110, 160, "N", 26, fill="#3a2412", weight="bold")
           + texto(1000, 250, "P.", 24, fill="#3a2412", style="italic")
           + texto(820, 760, "Río de Copiapó", 30, fill="#3a2412", style="italic")
           + texto(1180, 800, "Toledo", 28, fill="#3a2412", style="italic", anchor="end")
           + texto(330, 520, "aquí no canta", 26, fill="#8a1414", style="italic")
           + garabatos(140, 120, 360, 4, 34, 72, color="#3a2412", sw=2.2, op=0.75)
           + garabatos(140, 790, 520, 2, 34, 73, color="#3a2412", sw=2.2, op=0.7))
    render(doc(svg, w=w, h=h), f"{TMP}/derrotero_tinta.png")
    tinta = Image.open(f"{TMP}/derrotero_tinta.png").convert("RGBA")
    pap.alpha_composite(tinta)
    pap = pap.rotate(-2.5, expand=True, resample=Image.BICUBIC)
    con_sombra(base, pap, (960 - pap.width // 2, 540 - pap.height // 2))
    luz_central(base, [300, 60, 1620, 1020], fuerza=180)
    guardar(base, f"{CG}/derrotero.png", grain=6, vignette=0.55, seed=62, tint=((14, 8, 4), (255, 220, 170)))


def contrato():
    base = mesa_oscura(9, base=(30, 20, 14))
    w, h = 980, 1040
    pap = papel_viejo(w, h, 81, base=(226, 214, 186))
    d = ImageDraw.Draw(pap)
    tinta = (40, 30, 26, 255)
    d.text((w / 2, 90), "COMPAÑÍA MINERA", font=fnt(SERIF_B, 40), fill=tinta, anchor="mm")
    d.text((w / 2, 145), "«La Fortuna del Poniente»", font=fnt(SERIF_I, 38), fill=tinta, anchor="mm")
    d.line([(200, 185), (w - 200, 185)], fill=tinta, width=2)
    d.text((80, 230), "En Copiapó, a 20 días de junio de 1839, ante mí, escribano,", font=fnt(SERIF_C, 25), fill=tinta)
    d.text((80, 266), "comparecen los socios D. Fermín Cisternas, Matías Ardiles", font=fnt(SERIF_C, 25), fill=tinta)
    d.text((80, 302), "y Celestino Aracena, y convienen lo siguiente:", font=fnt(SERIF_C, 25), fill=tinta)
    svg = garabatos(80, 370, 820, 6, 36, 82, color="#2a2420", sw=2.2, op=0.75)
    render(doc(svg, w=w, h=h), f"{TMP}/contrato_g.png")
    pap.alpha_composite(Image.open(f"{TMP}/contrato_g.png").convert("RGBA"))
    d = ImageDraw.Draw(pap)
    # cláusula cuarta, legible y subrayada a lápiz
    y0 = 600
    d.text((80, y0), "Cuarta. Cada socio responde ante las deudas", font=fnt(SERIF_I, 30), fill=tinta)
    d.text((80, y0 + 42), "de la compañía con lo suyo y con los suyos.", font=fnt(SERIF_I, 30), fill=tinta)
    capa = Image.new("RGBA", pap.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).line([(470, y0 + 82), (720, y0 + 84)], fill=(140, 30, 30, 200), width=4)
    pap.alpha_composite(capa)
    svg2 = garabatos(80, 730, 820, 3, 36, 83, color="#2a2420", sw=2.2, op=0.75)
    render(doc(svg2, w=w, h=h), f"{TMP}/contrato_g2.png")
    pap.alpha_composite(Image.open(f"{TMP}/contrato_g2.png").convert("RGBA"))
    d = ImageDraw.Draw(pap)
    d.text((150, 920), "Fermín Cisternas", font=fnt(SERIF_I, 34), fill=(30, 30, 60, 255))
    d.line([(140, 960), (420, 956)], fill=(30, 30, 60, 255), width=2)
    d.text((480, 912), "+", font=fnt(SERIF_B, 54), fill=(30, 30, 60, 255))
    d.text((560, 920), "Matías Ardiles", font=fnt(SERIF_I, 32), fill=(30, 30, 60, 255))
    d.ellipse([w - 150, 800, w - 60, 890], fill=(140, 24, 30, 255))
    d.ellipse([w - 132, 818, w - 78, 872], outline=(90, 10, 14, 255), width=4)
    pap = pap.rotate(1.5, expand=True, resample=Image.BICUBIC)
    con_sombra(base, pap, (960 - pap.width // 2, 540 - pap.height // 2 + 10))
    # pluma y tintero
    svg3 = ('<rect x="1560" y="720" width="120" height="100" rx="14" fill="#c9ccd6" stroke="#5a5e68" stroke-width="4"/>'
            '<ellipse cx="1620" cy="720" rx="40" ry="12" fill="#1a1a22"/>'
            '<path d="M1620,716 L1760,420 C1790,400 1800,430 1780,450 Z" fill="#efe8dc" stroke="#8a8478" stroke-width="3"/>')
    render(doc(svg3), f"{TMP}/pluma.png")
    base.alpha_composite(Image.open(f"{TMP}/pluma.png").convert("RGBA"))
    luz_central(base, [260, 0, 1660, 1080], fuerza=170)
    guardar(base, f"{CG}/contrato.png", grain=6, vignette=0.55, seed=63, tint=((14, 10, 8), (255, 230, 190)))


def avalancha():
    rnd = random.Random(651)
    d1 = F.grad("cieloAv", [(0, "#2e2546"), (1, "#d07a56")])
    d2 = F.grad("arenaAv", [(0, "#f6d6a2"), (0.6, "#dcae72"), (1, "#a9784a")], vertical=False)
    b = ['<rect width="1920" height="1080" fill="url(#cieloAv)"/>']
    lad = "M0,180 C600,120 1300,60 1920,0 L1920,1080 L0,1080 Z"
    b.append(f'<path d="{lad}" fill="url(#arenaAv)"/>')
    defs = d1 + d2 + f'<clipPath id="avC"><path d="{lad}"/></clipPath>'
    g = []
    for k in range(160):
        y = rnd.uniform(100, 1080)
        x = rnd.uniform(-100, 1900)
        L = rnd.uniform(100, 360)
        g.append(f'<path d="M{x:.0f},{y:.0f} q{L/2:.0f},{rnd.uniform(-10,4):.0f} {L:.0f},{rnd.uniform(-22,-4):.0f}" stroke="#b98a52" stroke-width="2" fill="none" opacity="0.45"/>')
    # lenguas de arena en movimiento (diagonales, con estela)
    for k in range(26):
        x0 = rnd.uniform(200, 1800)
        y0 = rnd.uniform(60, 400)
        L = rnd.uniform(500, 900)
        dx = -rnd.uniform(150, 400)
        g.append(f'<path d="M{x0:.0f},{y0:.0f} q{dx*0.3:.0f},{L*0.5:.0f} {dx:.0f},{L:.0f}" stroke="#fff2d0" stroke-width="{rnd.uniform(16,40):.0f}" opacity="0.28" fill="none" filter="url(#b8)" stroke-linecap="round"/>')
        for j in range(5):
            ox = rnd.uniform(-20, 20)
            g.append(f'<path d="M{x0 + ox:.0f},{y0:.0f} q{dx*0.3:.0f},{L*0.5:.0f} {dx + ox*3:.0f},{L:.0f}" stroke="#fff6dc" stroke-width="1.6" opacity="0.6" fill="none"/>')
    b.append('<g clip-path="url(#avC)">' + "".join(g) + '</g>')
    # ondas del bramido saliendo del cerro
    for k in range(9):
        r = 180 + k * 150
        b.append(f'<path d="M{960 - r},{1080} A{r},{r*0.6} 0 0 1 {960 + r},{1080}" stroke="#ffe0a0" stroke-width="{6 - k*0.5:.1f}" fill="none" opacity="{0.42 - k*0.04:.2f}" filter="url(#b2)"/>')
    # Celestino deslizándose (silueta con chupalla)
    b.append('<g transform="translate(900,780) rotate(14)" stroke="#2a1a10" stroke-linecap="round" fill="#2a1a10">'
             '<path d="M-20,-60 C-30,-20 -20,20 0,40" stroke-width="64" fill="none"/>'
             '<path d="M-30,-40 L-110,-110" stroke-width="20" fill="none"/><path d="M10,-40 L90,-120" stroke-width="20" fill="none"/>'
             '<path d="M0,40 L-150,70" stroke-width="26" fill="none"/><path d="M10,40 L-120,100" stroke-width="26" fill="none"/>'
             '<circle cx="-14" cy="-118" r="26" stroke="none"/>'
             '<ellipse cx="-14" cy="-138" rx="62" ry="12" stroke="none"/><ellipse cx="-14" cy="-152" rx="30" ry="18" stroke="none"/>'
             '</g>')
    b.append('<path d="M700,860 C760,820 900,800 1040,840" stroke="#fff2d0" stroke-width="40" opacity="0.35" fill="none" filter="url(#b16)"/>')
    for k in range(60):
        b.append(f'<circle cx="{rnd.uniform(500,1400):.0f}" cy="{rnd.uniform(600,1000):.0f}" r="{rnd.uniform(1,3):.1f}" fill="#fff0cc" opacity="{rnd.uniform(0.3,0.8):.2f}"/>')
    svg = doc("".join(b), defs)
    p = f"{CG}/avalancha.png"
    render(svg, p)
    post(p, grain=6, vignette=0.55, tint=((40, 20, 20), (255, 215, 165)), seed=64)


def caballero_cg():
    F.campamento()
    base = Image.open(f"{OUT}/bg/campamento.png").convert("RGB")
    base = base.crop((360, 200, 1560, 875)).resize((1920, 1080), Image.LANCZOS).filter(ImageFilter.GaussianBlur(10))
    base = ImageEnhance.Brightness(base, ).enhance(0.55).convert("RGBA")
    cab = Image.open(f"{OUT}/sprites/caballero_sonrisa.png").convert("RGBA")
    s = 1.75
    cab = cab.resize((int(820 * s), int(1080 * s)), Image.LANCZOS)
    base.alpha_composite(cab, (560 - int(410 * s) + 300, -60))
    # luz del fuego desde abajo
    luz = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse([300, 640, 1600, 1500], fill=(255, 140, 50, 90))
    base.alpha_composite(luz.filter(ImageFilter.GaussianBlur(120)))
    # mano enguantada con la petaca de plata
    svg = ('<g transform="translate(1320,820) rotate(-14)">'
           '<rect x="-90" y="-210" width="180" height="250" rx="40" fill="#c9ccd6" stroke="#4a4e58" stroke-width="6"/>'
           '<rect x="-60" y="-180" width="120" height="190" rx="24" fill="none" stroke="#8a8e98" stroke-width="4"/>'
           '<path d="M-40,-140 q40,-30 80,0 q-40,30 -80,0 Z" fill="none" stroke="#8a8e98" stroke-width="3"/>'
           '<rect x="-26" y="-260" width="52" height="54" rx="8" fill="#a8acb6" stroke="#4a4e58" stroke-width="5"/>'
           '<path d="M-100,-80 C-160,-60 -180,40 -150,140 L80,140 C90,80 80,20 60,0 Z" fill="#0c0b10"/>'
           '<path d="M-110,-110 C-60,-130 40,-120 70,-90 C60,-40 20,-10 -40,-10 C-90,-10 -120,-50 -110,-110 Z" fill="#141218" stroke="#2a2830" stroke-width="4"/>'
           '<path d="M70,-90 L60,-20" stroke="#2a2830" stroke-width="4"/>'
           '</g>'
           '<circle cx="1300" cy="640" r="40" fill="#ffffff" opacity="0.18" filter="url(#b16)"/>')
    render(doc(svg), f"{TMP}/petaca.png")
    base.alpha_composite(Image.open(f"{TMP}/petaca.png").convert("RGBA"))
    rnd = random.Random(5)
    chispas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    dd = ImageDraw.Draw(chispas)
    for _ in range(60):
        x, y, r = rnd.uniform(0, 1920), rnd.uniform(500, 1080), rnd.uniform(1.5, 4)
        dd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 200, 100, rnd.randint(120, 230)))
    base.alpha_composite(chispas)
    guardar(base, f"{CG}/caballero.png", grain=7, vignette=0.7, seed=65, tint=((10, 4, 10), (255, 180, 110)))


TODOS = ["titulo", "menus", "derrotero", "contrato", "avalancha", "caballero_cg"]

if __name__ == "__main__":
    for n in sys.argv[1:] or TODOS:
        globals()[n]()
        print("ok", n)
