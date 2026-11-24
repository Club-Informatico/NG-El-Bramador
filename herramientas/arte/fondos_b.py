"""Fondos de EL BRAMADOR (Copiapó, 1839)."""
import math
import random
import sys

from lib import *

BG = OUT + "/bg"


def grad(gid, stops, vertical=True):
    a = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" {a}>{s}</linearGradient>'


def suavizar(vals, k=5):
    return np.convolve(vals, np.ones(k) / k, mode="same")


def silueta(x0, x1, ybase, pico_x, pico_y, seed, rugosidad=18, pasos=60):
    """Puntos de una silueta de cerro con cima en (pico_x, pico_y)."""
    rnd = random.Random(seed)
    pts = []
    for i in range(pasos + 1):
        x = x0 + (x1 - x0) * i / pasos
        if x <= pico_x:
            t = (x - x0) / max(1, pico_x - x0)
            y = ybase - (ybase - pico_y) * (math.sin(t * math.pi / 2) ** 1.4)
        else:
            t = (x - pico_x) / max(1, x1 - pico_x)
            y = ybase - (ybase - pico_y) * (math.cos(t * math.pi / 2) ** 1.2)
        pts.append([x, y])
    ys = suavizar([p[1] + rnd.gauss(0, rugosidad) for p in pts], 3)
    for p, y in zip(pts, ys):
        p[1] = y
    pts[0][1] = ybase
    pts[-1][1] = ybase
    return pts


def poli(pts, cierre_y=None):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    if cierre_y is not None:
        d += f" L{pts[-1][0]:.1f},{cierre_y} L{pts[0][0]:.1f},{cierre_y}"
    return d + " Z"


def cerro_bramador(cx, ybase, ancho, alto, modo="noche", seed=3, detalle=1.0):
    """El Bramador: macizo rocoso con la falda poniente cubierta por un manto irregular de arena."""
    col = {
        "noche": dict(roca="#17130f", roca2="#221c16", luz_roca="#3a4658", arena="#5e5a53", arena_luz="#8b867b",
                      arena_sombra="#3f3c37", onda="#4a4740", lengua="#a39d90"),
        "tarde": dict(roca="#5a3a28", roca2="#7a4e32", luz_roca="#c27a44", arena="#e2b77c", arena_luz="#f7d9a2",
                      arena_sombra="#b5824c", onda="#c99a62", lengua="#fff0cc"),
        "alba": dict(roca="#3a2a32", roca2="#4e3640", luz_roca="#c98a84", arena="#c9a28e", arena_luz="#f0c9a8",
                     arena_sombra="#8e6c66", onda="#a8847a", lengua="#ffe2cc"),
    }[modo]
    rnd = random.Random(seed)
    x0, x1 = cx - ancho / 2, cx + ancho / 2
    p1 = cx - ancho * 0.05
    p2 = cx + ancho * 0.22
    xs = np.linspace(x0, x1, 120)
    forma = np.exp(-((xs - p1) / (ancho * 0.26)) ** 2) + 0.62 * np.exp(-((xs - p2) / (ancho * 0.16)) ** 2)
    forma += 0.18 * np.exp(-((xs - (cx - ancho * 0.32)) / (ancho * 0.12)) ** 2)
    forma = forma / forma.max()
    pie = np.minimum(1, np.minimum((xs - x0) / (ancho * 0.06), (x1 - xs) / (ancho * 0.06)))
    ruido = suavizar([rnd.gauss(0, 1) for _ in xs], 4)
    ys = ybase - alto * forma * pie - np.array(ruido) * alto * 0.012
    ys[0] = ys[-1] = ybase
    pts = list(zip(xs, ys))
    o = [f'<path d="{poli(pts)}" fill="{col["roca"]}"/>']
    # quebradas y estratos
    for k in range(int(34 * detalle)):
        i = rnd.randint(10, 110)
        xq, yq = pts[i]
        largo = rnd.uniform(40, 170) * alto / 450
        o.append(f'<path d="M{xq:.0f},{yq + 8:.0f} q{rnd.uniform(-25,25):.0f},{largo/2:.0f} {rnd.uniform(-15,25):.0f},{largo:.0f}" '
                 f'stroke="{col["roca2"]}" stroke-width="{rnd.uniform(3,9):.0f}" fill="none" opacity="0.8"/>')
    cresta = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts[8:112])
    o.append(f'<path d="{cresta}" stroke="{col["luz_roca"]}" stroke-width="3" fill="none" opacity="0.6"/>')
    # --- manto de arena: borde superior bajo la cresta, bordes laterales ondulados, abanicos al pie
    i_top = int(np.argmin(ys))
    izq = []
    for i in range(14, i_top + 1, 3):
        x, y = pts[i]
        izq.append((x, y + rnd.uniform(14, 40) * alto / 450))
    tx, ty = pts[i_top]
    der_base_x = cx + ancho * 0.10
    der = []
    n = 14
    for j in range(1, n + 1):
        t = j / n
        x = tx + (der_base_x - tx) * t + math.sin(t * 9 + seed) * ancho * 0.018 + rnd.uniform(-8, 8)
        y = ty + 20 + (ybase - ty - 20) * t ** 0.9
        der.append((x, y))
    base = []
    xl = izq[0][0] - ancho * 0.03
    m = 10
    for j in range(m + 1):
        t = j / m
        x = der_base_x + (xl - der_base_x) * t
        lob = abs(math.sin(t * math.pi * 3.5 + seed)) * rnd.uniform(8, 26)
        base.append((x, ybase + lob))
    arena_pts = izq + der + base
    arena_d = poli(arena_pts)
    gid = f"arenaG{seed}{modo}"
    gid2 = f"arenaV{seed}{modo}"
    defs = (grad(gid, [(0, col["arena_luz"]), (0.6, col["arena"]), (1, col["arena_sombra"])], vertical=False)
            + grad(gid2, [(0, "#ffffff"), (1, "#000000")]))
    o.append(f'<defs>{defs}<clipPath id="clipA{seed}{modo}"><path d="{arena_d}"/></clipPath></defs>')
    o.append(f'<path d="{arena_d}" fill="url(#{gid})"/>')
    o.append(f'<path d="{arena_d}" fill="url(#{gid2})" opacity="0.10"/>')
    interior = []
    # ondulaciones finas
    for k in range(int(70 * detalle)):
        t = rnd.uniform(0.03, 1.0)
        y = ty + (ybase - ty) * t
        xa = izq[0][0] + (tx - izq[0][0]) * (1 - t) * 0.6
        xb = tx + (der_base_x - tx) * t
        a_ = xa + (xb - xa) * rnd.uniform(0, 0.7)
        b_ = a_ + (xb - xa) * rnd.uniform(0.1, 0.35)
        interior.append(f'<path d="M{a_:.0f},{y:.0f} Q{(a_+b_)/2:.0f},{y + rnd.uniform(-5,5):.0f} {b_:.0f},{y + rnd.uniform(-3,7):.0f}" '
                        f'stroke="{col["onda"]}" stroke-width="{1 + 1.6*t:.1f}" fill="none" opacity="0.5"/>')
    # afloramientos de roca dentro del manto
    for k in range(0):
        t = rnd.uniform(0.25, 0.75)
        y = ty + (ybase - ty) * t
        x = tx + (der_base_x - tx) * t * rnd.uniform(0.2, 0.7) - ancho * 0.05
        r = rnd.uniform(6, 16) * alto / 450
        ptsr = " ".join(f"{x + math.cos(a)*r*rnd.uniform(0.6,1.3):.0f},{y + math.sin(a)*r*0.6*rnd.uniform(0.6,1.3):.0f}" for a in np.linspace(0, 2*math.pi, 9)[:-1])
        interior.append(f'<polygon points="{ptsr}" fill="{col["roca"]}" opacity="0.9"/>')
    # lenguas de arena que corren ladera abajo (finas y suaves)
    for k in range(int(16 * detalle)):
        t0 = rnd.uniform(0.0, 0.35)
        x_s = tx - (tx - izq[0][0]) * rnd.uniform(0.0, 0.5) * (1 - t0)
        y_s = ty + (ybase - ty) * t0
        largo = (ybase - y_s) * rnd.uniform(0.45, 0.95)
        der_x = rnd.uniform(-60, 10)
        anchoL = rnd.uniform(3, 9)
        interior.append(f'<path d="M{x_s:.0f},{y_s:.0f} q{der_x*0.3:.0f},{largo*0.5:.0f} {der_x:.0f},{largo:.0f}" stroke="{col["lengua"]}" '
                        f'stroke-width="{anchoL:.1f}" fill="none" opacity="0.30" filter="url(#b2)" stroke-linecap="round"/>')
        interior.append(f'<path d="M{x_s + anchoL:.0f},{y_s:.0f} q{der_x*0.3:.0f},{largo*0.5:.0f} {der_x:.0f},{largo:.0f}" stroke="{col["arena_sombra"]}" '
                        f'stroke-width="{anchoL*0.5:.1f}" fill="none" opacity="0.30" stroke-linecap="round"/>')
    o.append(f'<g clip-path="url(#clipA{seed}{modo})">' + "".join(interior) + '</g>')
    return "".join(o)


def pampa(y0, color, piedras_col, seed, n=120, matas=True, w=W):
    rnd = random.Random(seed)
    o = [f'<rect x="0" y="{y0}" width="{w}" height="{H - y0 + 5}" fill="{color}"/>']
    for k in range(n):
        y = y0 + (H - y0) * (rnd.random() ** 1.6)
        esc = 0.3 + 1.7 * (y - y0) / (H - y0)
        x = rnd.uniform(0, w)
        r = rnd.uniform(3, 9) * esc
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r*1.4:.1f}" ry="{r*0.7:.1f}" fill="{piedras_col}" opacity="0.9"/>')
    if matas:
        for k in range(int(n / 6)):
            y = y0 + (H - y0) * (rnd.random() ** 1.3)
            esc = 0.3 + 1.7 * (y - y0) / (H - y0)
            x = rnd.uniform(0, w)
            ramas = "".join(f'<path d="M{x:.0f},{y:.0f} q{rnd.uniform(-8,8)*esc:.0f},{-10*esc:.0f} {rnd.uniform(-16,16)*esc:.0f},{-rnd.uniform(12,24)*esc:.0f}" '
                            f'stroke="#0d0b08" stroke-width="{1.5*esc:.1f}" fill="none"/>' for _ in range(7))
            o.append(ramas)
    return "".join(o)


def fogata(x, y, esc=1.0):
    s = esc
    o = [f'<circle cx="{x}" cy="{y - 30*s}" r="{420*s}" fill="url(#glowFuego)" opacity="0.9"/>',
         f'<ellipse cx="{x}" cy="{y + 6*s}" rx="{90*s}" ry="{18*s}" fill="#120a06"/>']
    for k in range(7):
        a = k / 7 * math.pi
        o.append(f'<ellipse cx="{x + math.cos(a)*60*s:.0f}" cy="{y + 8*s:.0f}" rx="{20*s:.0f}" ry="{11*s:.0f}" fill="#2a2420"/>')
    o.append(f'<path d="M{x-60*s},{y} L{x+50*s},{y-24*s} M{x-40*s},{y-26*s} L{x+60*s},{y-2*s}" stroke="#2a1608" stroke-width="{12*s}" stroke-linecap="round"/>')
    o.append(f'<path d="M{x-40*s},{y-6*s} C{x-50*s},{y-60*s} {x-10*s},{y-80*s} {x},{y-140*s} C{x+14*s},{y-90*s} {x+50*s},{y-60*s} {x+40*s},{y-6*s} Z" fill="#ff8a24"/>')
    o.append(f'<path d="M{x-22*s},{y-6*s} C{x-26*s},{y-40*s} {x-4*s},{y-60*s} {x+4*s},{y-100*s} C{x+12*s},{y-60*s} {x+30*s},{y-40*s} {x+22*s},{y-6*s} Z" fill="#ffd25a"/>')
    o.append(f'<path d="M{x-10*s},{y-6*s} C{x-10*s},{y-26*s} {x},{y-40*s} {x+2*s},{y-60*s} C{x+8*s},{y-36*s} {x+14*s},{y-24*s} {x+10*s},{y-6*s} Z" fill="#fff4c4"/>')
    o.append(f'<circle cx="{x}" cy="{y - 60*s}" r="{120*s}" fill="#ffb347" opacity="0.25" filter="url(#b30)"/>')
    rnd = random.Random(int(x))
    for k in range(18):
        o.append(f'<circle cx="{x + rnd.uniform(-60,60)*s:.0f}" cy="{y - rnd.uniform(80,320)*s:.0f}" r="{rnd.uniform(1.5,3)*s:.1f}" fill="#ffcf6a" opacity="{rnd.uniform(0.4,0.9):.2f}"/>')
    return "".join(o)


DEFS_FUEGO = ('<radialGradient id="glowFuego"><stop offset="0" stop-color="#ffb04a" stop-opacity="0.65"/>'
              '<stop offset="0.35" stop-color="#e0661e" stop-opacity="0.22"/><stop offset="1" stop-color="#e0661e" stop-opacity="0"/></radialGradient>'
              '<radialGradient id="glowOro"><stop offset="0" stop-color="#fff2b0" stop-opacity="0.9"/>'
              '<stop offset="0.4" stop-color="#f0b93c" stop-opacity="0.35"/><stop offset="1" stop-color="#f0b93c" stop-opacity="0"/></radialGradient>'
              '<radialGradient id="glowVelaB"><stop offset="0" stop-color="#fff1c4" stop-opacity="1"/><stop offset="0.3" stop-color="#ffb85a" stop-opacity="0.45"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>')


def mula(x, y, esc=1.0, color="#0c0a09", flip=False):
    s = esc
    tr = f' transform="translate({x},{y}) scale({-s if flip else s},{s})"'
    return (f'<g{tr} fill="{color}">'
            '<ellipse cx="0" cy="-70" rx="70" ry="34"/>'
            '<path d="M50,-90 C80,-110 95,-140 110,-150 L130,-140 C122,-118 110,-95 80,-70 Z"/>'
            '<path d="M108,-152 L104,-182 L114,-158 Z M118,-150 L118,-182 L126,-154 Z"/>'
            '<ellipse cx="128" cy="-136" rx="22" ry="13" transform="rotate(30 128 -136)"/>'
            '<rect x="-55" y="-50" width="10" height="52"/><rect x="-35" y="-48" width="10" height="50"/>'
            '<rect x="35" y="-50" width="10" height="52"/><rect x="52" y="-48" width="10" height="50"/>'
            '<path d="M-68,-80 C-90,-70 -94,-40 -88,-20" stroke="' + color + '" stroke-width="7" fill="none"/>'
            '</g>')


# ---------------------------------------------------------------------------

def cerro_noche():
    d1 = grad("cieloN", [(0, "#01030a"), (0.6, "#08122a"), (1, "#1a2840")])
    b = [f'<rect width="{W}" height="800" fill="url(#cieloN)"/>', via_lactea(1250, 180, 900, 170, -24, 301),
         estrellas(900, 302, y_max=650)]
    b.append(cerro(700, 160, 303, "#0b0f17", rim="#2c3e57"))
    b.append(cerro_bramador(1000, 790, 1500, 470, "noche", seed=7))
    b.append(cerro(820, 70, 304, "#0a0b0d"))
    b.append(pampa(790, "#0f0d0b", "#1c1914", 305, n=160))
    b.append('<rect y="740" width="1920" height="80" fill="#8a96b0" opacity="0.05" filter="url(#b30)"/>')
    svg = doc("".join(b), d1 + DEFS_FUEGO)
    p = f"{BG}/cerro_noche.png"
    render(svg, p)
    post(p, grain=7, vignette=0.6, tint=((4, 8, 22), (200, 210, 230)), seed=40)


def cerro_tarde():
    d1 = grad("cieloT", [(0, "#251f3f"), (0.45, "#7a4766"), (0.75, "#e0855a"), (1, "#f6c27a")])
    b = [f'<rect width="{W}" height="820" fill="url(#cieloT)"/>']
    b.append('<ellipse cx="400" cy="200" rx="500" ry="60" fill="#f2b08a" opacity="0.25" filter="url(#b30)"/>')
    b.append('<ellipse cx="1500" cy="300" rx="380" ry="40" fill="#f0a07a" opacity="0.2" filter="url(#b30)"/>')
    b.append(cerro(700, 170, 311, "#5c3a4a", rim="#c88a7a"))
    b.append(cerro_bramador(1000, 800, 1500, 480, "tarde", seed=7))
    b.append(cerro(830, 60, 312, "#3a2620"))
    b.append(pampa(800, "#7a5236", "#5a3a26", 313, n=170))
    # sombras largas
    b.append('<path d="M0,880 L1920,830 L1920,1080 L0,1080 Z" fill="#2a1a12" opacity="0.25"/>')
    b.append('<rect y="760" width="1920" height="80" fill="#ffd9a0" opacity="0.10" filter="url(#b30)"/>')
    svg = doc("".join(b), d1 + DEFS_FUEGO)
    p = f"{BG}/cerro_tarde.png"
    render(svg, p)
    post(p, grain=6, vignette=0.45, tint=((40, 20, 30), (255, 210, 160)), seed=41)


def ladera():
    d1 = grad("cieloL", [(0, "#3a2f52"), (1, "#d88a62")])
    d2 = grad("arenaL", [(0, "#f2cf98"), (0.6, "#d7a96e"), (1, "#a77a48")], vertical=False)
    rnd = random.Random(321)
    b = [f'<rect width="{W}" height="500" fill="url(#cieloL)"/>']
    # roca de la cumbre arriba a la derecha
    b.append('<path d="M1200,0 L1920,0 L1920,420 L1700,380 L1560,300 L1420,220 L1300,120 Z" fill="#4e3226"/>')
    for k in range(14):
        x = rnd.uniform(1300, 1900)
        b.append(f'<path d="M{x:.0f},{rnd.uniform(40,300):.0f} l{rnd.uniform(-30,30):.0f},{rnd.uniform(60,140):.0f}" stroke="#6a4430" stroke-width="{rnd.uniform(3,8):.0f}"/>')
    # la gran ladera de arena
    lad = "M0,330 C500,300 1000,230 1300,120 L1560,300 L1920,420 L1920,1080 L0,1080 Z"
    b.append(f'<path d="{lad}" fill="url(#arenaL)"/>')
    defs = d1 + d2 + f'<clipPath id="ladC"><path d="{lad}"/></clipPath>'
    ondas = []
    for k in range(220):
        y = rnd.uniform(260, 1080)
        x = rnd.uniform(-100, 1900)
        L = rnd.uniform(80, 360) * (0.4 + y / 1080)
        ondas.append(f'<path d="M{x:.0f},{y:.0f} q{L/2:.0f},{rnd.uniform(-14,6):.0f} {L:.0f},{rnd.uniform(-30,-5):.0f}" stroke="#b98a52" stroke-width="{1+3*y/1080:.1f}" fill="none" opacity="0.5"/>')
    # lenguas de arena corriendo ladera abajo
    for k in range(14):
        x0 = rnd.uniform(500, 1400)
        y0 = rnd.uniform(200, 420)
        L = rnd.uniform(400, 800)
        ancho = rnd.uniform(30, 80)
        dx = -rnd.uniform(60, 220)
        ondas.append(f'<path d="M{x0:.0f},{y0:.0f} q{dx*0.3:.0f},{L*0.5:.0f} {dx:.0f},{L:.0f}" stroke="#fbe2b4" stroke-width="{ancho*0.35:.0f}" opacity="0.30" fill="none" filter="url(#b8)" stroke-linecap="round"/>')
        for j in range(4):
            ox = rnd.uniform(-14, 14)
            ondas.append(f'<path d="M{x0 + ox:.0f},{y0:.0f} q{dx*0.3:.0f},{L*0.5:.0f} {dx + ox*2:.0f},{L:.0f}" stroke="#fff0cc" stroke-width="1.6" opacity="0.45" fill="none"/>')
        ondas.append(f'<path d="M{x0 + ancho*0.25:.0f},{y0:.0f} q{dx*0.3:.0f},{L*0.5:.0f} {dx + ancho*0.2:.0f},{L:.0f}" stroke="#a87a48" stroke-width="3" opacity="0.45" fill="none"/>')
    b.append('<g clip-path="url(#ladC)">' + "".join(ondas) + '</g>')
    # polvo en suspensión
    for k in range(30):
        b.append(f'<ellipse cx="{rnd.uniform(0,1920):.0f}" cy="{rnd.uniform(200,900):.0f}" rx="{rnd.uniform(60,220):.0f}" ry="{rnd.uniform(6,18):.0f}" fill="#ffe6b8" opacity="{rnd.uniform(0.05,0.14):.2f}" filter="url(#b8)"/>')
    b.append('<rect width="1920" height="1080" fill="#3a1e10" opacity="0.12"/>')
    svg = doc("".join(b), defs)
    p = f"{BG}/ladera.png"
    render(svg, p)
    post(p, grain=6, vignette=0.5, tint=((40, 20, 20), (255, 215, 165)), seed=42)


def puerta():
    d1 = grad("cieloP", [(0, "#120f22"), (1, "#5a3550")])
    d2 = grad("arenaP", [(0, "#8a7462"), (1, "#5c4a3e")])
    rnd = random.Random(331)
    b = [f'<rect width="{W}" height="400" fill="url(#cieloP)"/>', estrellas(150, 332, y_max=300)]
    lad = "M0,260 C600,240 1200,180 1920,120 L1920,1080 L0,1080 Z"
    b.append(f'<path d="{lad}" fill="url(#arenaP)"/>')
    for k in range(120):
        y = rnd.uniform(220, 1080)
        x = rnd.uniform(-100, 1900)
        L = rnd.uniform(80, 300)
        b.append(f'<path d="M{x:.0f},{y:.0f} q{L/2:.0f},{rnd.uniform(-10,6):.0f} {L:.0f},{rnd.uniform(-20,-4):.0f}" stroke="#6e5a4a" stroke-width="2" fill="none" opacity="0.5"/>')
    # manchón de arena "muda": más liso y quieto
    b.append('<ellipse cx="980" cy="700" rx="760" ry="260" fill="#9a846e" opacity="0.5" filter="url(#b16)"/>')
    # entrada excavada en la ladera: jambas y dintel de piedra que asoman de la arena
    b.append('<path d="M560,980 C600,700 700,520 980,500 C1260,520 1360,700 1400,980 Z" fill="#3a2e26" opacity="0.85"/>')
    b.append('<path d="M640,980 C680,740 760,600 980,585 C1200,600 1280,740 1320,980 Z" fill="#241a14"/>')
    # jambas
    b.append('<path d="M770,600 L860,600 L850,960 L760,960 Z" fill="#6b6258"/><path d="M1100,600 L1190,600 L1200,960 L1110,960 Z" fill="#544c44"/>')
    b.append('<path d="M770,600 L860,600 L850,960 L760,960 Z" fill="none" stroke="#2e2924" stroke-width="4"/>')
    b.append('<path d="M1100,600 L1190,600 L1200,960 L1110,960 Z" fill="none" stroke="#2e2924" stroke-width="4"/>')
    # dintel con signos
    b.append('<rect x="740" y="545" width="480" height="64" fill="#7a7066"/><rect x="740" y="545" width="480" height="64" fill="none" stroke="#2e2924" stroke-width="4"/>')
    for k in range(9):
        x = 772 + k * 50
        b.append(f'<path d="M{x},{562} l12,0 l-6,14 l12,0 M{x+22},{560} q9,12 0,24" stroke="#3a342e" stroke-width="3" fill="none"/>')
    # arena derramándose sobre el dintel
    b.append('<path d="M700,560 C760,520 1200,515 1260,560 C1200,548 1100,552 980,548 C860,552 760,548 700,560 Z" fill="#9a846e"/>')
    b.append('<path d="M900,548 q6,30 0,60" stroke="#b49c84" stroke-width="5" opacity="0.7"/>')
    # vano oscuro con brillo dorado
    b.append('<path d="M860,610 L1100,610 L1110,960 L850,960 Z" fill="#070403"/>')
    b.append('<path d="M870,640 L1095,640 L1100,960 L862,960 Z" fill="#f0b93c" opacity="0.16"/>')
    b.append('<ellipse cx="980" cy="880" rx="200" ry="150" fill="url(#glowOro)" opacity="0.85"/>')
    # montones de arena sacada
    b.append('<path d="M0,1080 C120,900 340,860 560,980 L620,1080 Z" fill="#8a7462"/>')
    b.append('<path d="M1920,1080 C1800,900 1580,870 1380,990 L1340,1080 Z" fill="#7a6656"/>')
    # herramientas y chonchón
    b.append('<path d="M300,1040 L560,760" stroke="#2a2a2e" stroke-width="14" stroke-linecap="round"/>')
    b.append('<ellipse cx="1560" cy="1000" rx="70" ry="20" fill="#8a8a90"/>')
    b.append('<rect x="1600" y="880" width="44" height="76" rx="6" fill="#3a3028"/><circle cx="1622" cy="868" r="11" fill="#ffd27a"/>')
    b.append('<circle cx="1622" cy="868" r="160" fill="url(#glowVelaB)" opacity="0.6"/>')
    # luz de la tarde que se va
    b.append('<rect width="1920" height="1080" fill="#1a1028" opacity="0.25"/>')
    svg = doc("".join(b), d1 + d2 + DEFS_FUEGO)
    p = f"{BG}/puerta.png"
    render(svg, p)
    post(p, grain=7, vignette=0.6, tint=((14, 8, 26), (255, 200, 140)), seed=43)


def campamento():
    d1 = grad("cieloC", [(0, "#01030a"), (1, "#101c32")])
    b = [f'<rect width="{W}" height="760" fill="url(#cieloC)"/>', via_lactea(700, 140, 900, 150, 12, 341),
         estrellas(800, 342, y_max=560)]
    b.append(cerro_bramador(1250, 780, 1800, 560, "noche", seed=11, detalle=1.2))
    b.append(pampa(770, "#0d0b09", "#1b1713", 343, n=110))
    # mulas inquietas a la derecha
    b.append(mula(1650, 870, 0.9, "#080706", flip=True))
    b.append(mula(1790, 890, 0.85, "#070605", flip=True))
    # bultos y monturas
    b.append('<ellipse cx="1300" cy="930" rx="130" ry="40" fill="#2a1e16"/><ellipse cx="1240" cy="905" rx="60" ry="34" fill="#3a2a1e"/>')
    b.append('<path d="M560,960 C620,930 800,930 860,960 L860,990 L560,990 Z" fill="#3a2418"/>')
    b.append('<path d="M560,960 C620,930 800,930 860,960" stroke="#8a4a2a" stroke-width="5" fill="none"/>')
    b.append(fogata(960, 930, 1.1))
    # luz de fuego sobre el suelo
    b.append('<ellipse cx="960" cy="960" rx="700" ry="160" fill="#ff9a3a" opacity="0.12" filter="url(#b30)"/>')
    svg = doc("".join(b), d1 + DEFS_FUEGO)
    p = f"{BG}/campamento.png"
    render(svg, p)
    post(p, grain=7, vignette=0.65, tint=((6, 6, 20), (255, 190, 120)), seed=44)


def desierto_alba():
    d1 = grad("cieloA", [(0, "#24284a"), (0.5, "#a86a7a"), (0.8, "#f2a86a"), (1, "#ffd99a")])
    b = [f'<rect width="{W}" height="820" fill="url(#cieloA)"/>']
    b.append('<circle cx="1500" cy="700" r="90" fill="#fff0c0"/>')
    b.append('<circle cx="1500" cy="700" r="380" fill="#ffd28a" opacity="0.35" filter="url(#b60)"/>')
    b.append(cerro(690, 170, 351, "#6a4a5a", rim="#f0c0a0"))
    b.append(cerro_bramador(520, 760, 900, 300, "alba", seed=13, detalle=0.8))
    b.append(cerro(760, 60, 352, "#4a3038"))
    b.append(pampa(760, "#8a6050", "#6a4438", 353, n=150))
    # huella del camino
    b.append('<path d="M560,1080 C700,940 900,830 1030,768 L1046,768 C960,840 860,960 1000,1080 Z" fill="#b08068" opacity="0.55"/>')
    b.append('<path d="M700,1080 C800,960 920,850 1036,770" stroke="#d2a888" stroke-width="5" fill="none" opacity="0.5"/>')
    b.append('<rect y="700" width="1920" height="120" fill="#ffe0b0" opacity="0.15" filter="url(#b30)"/>')
    svg = doc("".join(b), d1 + DEFS_FUEGO)
    p = f"{BG}/desierto_alba.png"
    render(svg, p)
    post(p, grain=6, vignette=0.4, tint=((40, 24, 40), (255, 220, 180)), seed=45)


if __name__ == "__main__":
    for n in sys.argv[1:] or ["cerro_noche", "cerro_tarde", "ladera", "puerta", "campamento", "desierto_alba"]:
        globals()[n]()
        print("ok", n)


# ===========================================================================
#  Interiores y Copiapó de 1839
# ===========================================================================

def pared_adobe(x, y, w, h, base, seed, manchas=60, grietas=True):
    rnd = random.Random(seed)
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{base}"/>']
    for k in range(manchas):
        cx_, cy_ = x + rnd.uniform(0, w), y + rnd.uniform(0, h)
        o.append(f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="{rnd.uniform(20,90):.0f}" ry="{rnd.uniform(10,40):.0f}" '
                 f'fill="{rnd.choice(["#000000", "#ffffff"])}" opacity="{rnd.uniform(0.03,0.08):.2f}" filter="url(#b8)"/>')
    if grietas:
        for k in range(8):
            gx, gy = x + rnd.uniform(0, w), y + rnd.uniform(0, h)
            d = f"M{gx:.0f},{gy:.0f}"
            for j in range(5):
                gx += rnd.uniform(-20, 20)
                gy += rnd.uniform(8, 26)
                d += f" L{gx:.0f},{gy:.0f}"
            o.append(f'<path d="{d}" stroke="#000" stroke-width="1.5" opacity="0.25" fill="none"/>')
    return "".join(o)


def vela(x, y, esc=1.0, botella=True, glow=1.0):
    s = esc
    o = []
    if botella:
        o.append(f'<path d="M{x-14*s},{y} L{x-14*s},{y-40*s} Q{x-14*s},{y-56*s} {x-5*s},{y-64*s} L{x-5*s},{y-80*s} L{x+5*s},{y-80*s} L{x+5*s},{y-64*s} Q{x+14*s},{y-56*s} {x+14*s},{y-40*s} L{x+14*s},{y} Z" fill="#1d2a1e" opacity="0.9"/>')
        top = y - 80 * s
    else:
        top = y
    o.append(f'<rect x="{x-5*s}" y="{top-36*s}" width="{10*s}" height="{36*s}" fill="#efe4c8"/>')
    o.append(f'<ellipse cx="{x}" cy="{top-46*s}" rx="{5*s}" ry="{11*s}" fill="#fff0b0"/>')
    o.append(f'<circle cx="{x}" cy="{top-44*s}" r="{200*s*glow}" fill="url(#glowVelaB)" opacity="0.55"/>')
    return "".join(o)


def chingana():
    rnd = random.Random(401)
    b = [pared_adobe(0, 0, 1920, 1080, "#5a3c28", 402)]
    # vigas del techo
    b.append('<rect width="1920" height="150" fill="#1e140d"/>')
    for k in range(8):
        b.append(f'<rect x="{k*260 - 20}" y="0" width="60" height="170" fill="#2c1d12"/>')
    b.append('<rect y="140" width="1920" height="26" fill="#2c1d12"/>')
    # puerta abierta a la noche (derecha)
    b.append('<rect x="1540" y="250" width="260" height="560" fill="#0c1424"/>')
    b.append(estrellas(30, 403, y_max=200).replace('cy="', 'cy="2').replace('cx="', 'cx="1').replace("<circle", '<circle'))
    b.append('<rect x="1540" y="250" width="260" height="560" fill="none" stroke="#1e140d" stroke-width="22"/>')
    b.append('<path d="M1800,260 L1880,300 L1880,820 L1800,810 Z" fill="#3a2616"/>')
    # repisas con botellas y guitarra colgada
    b.append('<rect x="160" y="300" width="560" height="16" fill="#2a1a0e"/><rect x="160" y="420" width="560" height="16" fill="#2a1a0e"/>')
    for k in range(10):
        x = 190 + k * 52
        h = rnd.uniform(50, 80)
        col = rnd.choice(["#2a3a24", "#3a2410", "#4a3a1a", "#1e2a30"])
        b.append(f'<rect x="{x}" y="{300 - h}" width="26" height="{h}" rx="6" fill="{col}"/><rect x="{x+8}" y="{300 - h - 18}" width="10" height="20" fill="{col}"/>')
        h = rnd.uniform(40, 70)
        b.append(f'<ellipse cx="{x+13}" cy="{420 - h/2}" rx="18" ry="{h/2}" fill="#7a4a2a"/>')
    b.append('<g transform="translate(980,250) rotate(-12)"><ellipse cx="0" cy="170" rx="80" ry="95" fill="#8a5a2a"/>'
             '<ellipse cx="0" cy="80" rx="60" ry="70" fill="#8a5a2a"/><circle cx="0" cy="120" r="22" fill="#1e140d"/>'
             '<rect x="-12" y="-150" width="24" height="200" fill="#3a2410"/><rect x="-18" y="-190" width="36" height="46" fill="#2a1a0e"/>'
             + "".join(f'<line x1="{-8 + k*3.2}" y1="-150" x2="{-8 + k*3.2}" y2="230" stroke="#d8c8a0" stroke-width="1"/>' for k in range(6))
             + '</g>')
    # mesón y barril
    b.append('<rect x="80" y="640" width="760" height="300" fill="#2e1d10"/><rect x="60" y="620" width="800" height="34" fill="#4a2e18"/>')
    b.append('<ellipse cx="1100" cy="860" rx="110" ry="140" fill="#4a2c16"/><rect x="990" y="760" width="220" height="12" fill="#1e140d"/><rect x="990" y="940" width="220" height="12" fill="#1e140d"/>')
    for k in range(5):
        x = 150 + k * 140
        b.append(f'<path d="M{x},620 q-24,-50 0,-90 q24,40 0,90 Z" fill="#8a5232"/>')
    # mesa de primer plano con cachos y vela
    b.append('<rect x="300" y="900" width="1300" height="40" fill="#3a2414"/><rect x="340" y="940" width="30" height="140" fill="#2a1a0e"/><rect x="1530" y="940" width="30" height="140" fill="#2a1a0e"/>')
    for x in (520, 700, 1300):
        b.append(f'<path d="M{x-24},900 L{x-18},850 L{x+18},850 L{x+24},900 Z" fill="#c9b48a"/>')
    b.append(vela(960, 900, 1.2))
    b.append(vela(400, 620, 0.9))
    b.append(vela(1700, 900, 0.8, glow=0.7))
    b.append('<rect width="1920" height="1080" fill="#1a0c04" opacity="0.18"/>')
    svg = doc("".join(b), DEFS_FUEGO)
    p = f"{BG}/chingana.png"
    render(svg, p)
    post(p, grain=7, vignette=0.6, tint=((14, 8, 6), (255, 196, 130)), seed=46)


def oficina():
    rnd = random.Random(411)
    b = [pared_adobe(0, 0, 1920, 1080, "#c9bca6", 412, manchas=40)]
    b.append('<rect y="820" width="1920" height="260" fill="#3a2a1c"/>')
    for k in range(16):
        b.append(f'<line x1="{k*130}" y1="820" x2="{k*130 - 120}" y2="1080" stroke="#24180e" stroke-width="3"/>')
    b.append('<rect y="800" width="1920" height="24" fill="#5a4030"/>')
    # ventana con vidrios y luz diurna
    b.append('<rect x="140" y="180" width="420" height="520" fill="#f2efe4"/>')
    for i in range(3):
        for j in range(4):
            b.append(f'<rect x="{150 + i*137}" y="{190 + j*127}" width="127" height="117" fill="#dfe8ee"/>')
    b.append('<path d="M140,180 L560,180 L560,700 L140,700 Z" fill="none" stroke="#5a4030" stroke-width="16"/>')
    b.append('<path d="M560,700 L1300,1080 L700,1080 L140,700 Z" fill="#fff6dc" opacity="0.18"/>')
    # cuadro de un barco
    b.append('<rect x="760" y="200" width="300" height="210" fill="#5a4020"/><rect x="776" y="216" width="268" height="178" fill="#5a6a72"/>')
    b.append('<path d="M840,340 L980,340 L960,370 L860,370 Z" fill="#2a1a10"/><path d="M900,250 L900,340 M900,262 L950,320 L900,320 M900,262 L860,320 L900,320" stroke="#e8e0d0" stroke-width="3" fill="#e8e0d0"/>')
    # reloj de pared
    b.append('<rect x="1180" y="160" width="90" height="300" rx="10" fill="#4a2e18"/><circle cx="1225" cy="230" r="34" fill="#efe6d2"/>')
    b.append('<line x1="1225" y1="230" x2="1225" y2="206" stroke="#222" stroke-width="3"/><line x1="1225" y1="230" x2="1240" y2="236" stroke="#222" stroke-width="3"/>')
    # estante con libros
    b.append('<rect x="1400" y="160" width="400" height="560" fill="#3a2414"/>')
    for r_ in range(4):
        y = 190 + r_ * 130
        b.append(f'<rect x="1410" y="{y + 110}" width="380" height="10" fill="#24160c"/>')
        x = 1420
        while x < 1770:
            w_ = rnd.uniform(18, 34)
            h_ = rnd.uniform(80, 108)
            b.append(f'<rect x="{x:.0f}" y="{y + 110 - h_:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="{rnd.choice(["#6a2a1e","#2a3a4a","#4a3a20","#2e4a2a","#5a4a3a"])}"/>')
            x += w_ + 3
    # caja fuerte
    b.append('<rect x="1480" y="700" width="260" height="240" rx="8" fill="#2a2c30"/><circle cx="1610" cy="800" r="30" fill="#8a8a7a"/><circle cx="1610" cy="800" r="8" fill="#2a2c30"/>')
    # escritorio
    b.append('<rect x="560" y="700" width="820" height="40" fill="#4a2a16"/><rect x="590" y="740" width="760" height="230" fill="#3a2010"/>')
    b.append('<rect x="620" y="770" width="320" height="170" fill="none" stroke="#24120a" stroke-width="5"/><rect x="1000" y="770" width="320" height="170" fill="none" stroke="#24120a" stroke-width="5"/>')
    # balanza de cobre
    b.append('<rect x="700" y="560" width="10" height="140" fill="#b07040"/><rect x="620" y="560" width="170" height="8" fill="#b07040"/>')
    b.append('<path d="M620,568 L600,630 L640,630 Z M790,568 L770,630 L810,630 Z" stroke="#b07040" stroke-width="2" fill="none"/>')
    b.append('<ellipse cx="620" cy="632" rx="34" ry="8" fill="#c98a50"/><ellipse cx="790" cy="632" rx="34" ry="8" fill="#c98a50"/>')
    b.append('<rect x="660" y="690" width="90" height="12" fill="#8a5030"/>')
    # libro de cuentas, tintero, barras de plata
    b.append('<path d="M880,690 L1110,690 L1130,700 L860,700 Z" fill="#6a2a1e"/><rect x="880" y="672" width="230" height="20" fill="#efe6d2"/>')
    b.append('<rect x="1160" y="664" width="44" height="36" rx="4" fill="#c9ccd2"/><path d="M1190,664 L1230,600" stroke="#efe6d2" stroke-width="3"/>')
    for k in range(3):
        b.append(f'<path d="M{1240 + k*8},{700 - k*14} L{1340 + k*8},{700 - k*14} L{1330 + k*8},{686 - k*14} L{1250 + k*8},{686 - k*14} Z" fill="#c9ccd6" stroke="#8a8e98" stroke-width="2"/>')
    b.append('<rect width="1920" height="1080" fill="#20140a" opacity="0.10"/>')
    svg = doc("".join(b), DEFS_FUEGO)
    p = f"{BG}/oficina.png"
    render(svg, p)
    post(p, grain=6, vignette=0.5, tint=((20, 14, 12), (255, 236, 200)), seed=47)


def rancho():
    rnd = random.Random(421)
    b = [pared_adobe(0, 0, 1920, 1080, "#4a3222", 422)]
    # techo de caña con vigas
    b.append('<rect width="1920" height="170" fill="#2a1c10"/>')
    for k in range(120):
        x = k * 16
        b.append(f'<line x1="{x}" y1="0" x2="{x + 6}" y2="170" stroke="#3a2a18" stroke-width="7"/>')
    for k in range(5):
        b.append(f'<rect x="{k*420 + 60}" y="0" width="44" height="200" fill="#1a1008"/>')
    b.append('<rect y="160" width="1920" height="30" fill="#1a1008"/>')
    # piso de tierra
    b.append('<rect y="840" width="1920" height="240" fill="#2a1e14"/>')
    # catre con frazada
    b.append('<rect x="120" y="700" width="620" height="40" fill="#3a2414"/><rect x="140" y="740" width="20" height="150" fill="#2a1a0e"/><rect x="700" y="740" width="20" height="150" fill="#2a1a0e"/>')
    b.append('<path d="M120,700 C200,640 600,630 740,690 L740,760 L120,760 Z" fill="#6a2a24"/>')
    for k in range(6):
        b.append(f'<line x1="{140 + k*100}" y1="660" x2="{150 + k*100}" y2="760" stroke="#8a3a2a" stroke-width="10" opacity="0.6"/>')
    # cordel con ropa colgada
    b.append('<path d="M900,300 Q1300,360 1760,300" stroke="#c9b48a" stroke-width="3" fill="none"/>')
    for k, col in enumerate(["#d8d0c0", "#8a9aa8", "#c9b0a0", "#e8e0d0"]):
        x = 980 + k * 190
        y = 318 + 18 * math.sin(k)
        b.append(f'<path d="M{x},{y} L{x+130},{y + 4} L{x+120},{y + 170} L{x+10},{y + 166} Z" fill="{col}" opacity="0.9"/>')
    # artesa de lavar
    b.append('<path d="M1300,880 L1700,880 L1660,980 L1340,980 Z" fill="#5a4030"/><ellipse cx="1500" cy="880" rx="200" ry="22" fill="#2a3a4a"/>')
    # santito con vela
    b.append('<rect x="860" y="430" width="90" height="120" fill="#c9a86a"/><rect x="870" y="440" width="70" height="100" fill="#4a5a8a"/><circle cx="905" cy="470" r="18" fill="#f2d6b0"/>')
    b.append(vela(905, 600, 0.7, botella=False, glow=0.7))
    b.append('<rect x="850" y="600" width="110" height="10" fill="#2a1a0e"/>')
    # brasero
    b.append('<path d="M860,960 L1060,960 L1030,880 L890,880 Z" fill="#3a3a3e"/><ellipse cx="960" cy="880" rx="80" ry="18" fill="#1a1010"/>')
    for k in range(14):
        b.append(f'<circle cx="{900 + rnd.uniform(0,120):.0f}" cy="{874 + rnd.uniform(0,10):.0f}" r="{rnd.uniform(5,10):.0f}" fill="{rnd.choice(["#ff6a1a","#ffb04a","#c0300a"])}"/>')
    b.append('<circle cx="960" cy="860" r="460" fill="url(#glowFuego)" opacity="0.8"/>')
    b.append('<rect width="1920" height="1080" fill="#0a0604" opacity="0.2"/>')
    svg = doc("".join(b), DEFS_FUEGO)
    p = f"{BG}/rancho.png"
    render(svg, p)
    post(p, grain=7, vignette=0.65, tint=((12, 8, 10), (255, 190, 130)), seed=48)


def transito():
    rnd = random.Random(431)
    b = [pared_adobe(0, 0, 1920, 1080, "#3e2a1e", 432)]
    b.append('<rect width="1920" height="140" fill="#1a1008"/>')
    for k in range(4):
        b.append(f'<rect x="{k*520 + 100}" y="0" width="40" height="170" fill="#120a04"/>')
    b.append('<rect y="130" width="1920" height="24" fill="#120a04"/>')
    # atados de hierbas colgando
    for k in range(18):
        x = 80 + k * 100 + rnd.uniform(-20, 20)
        L = rnd.uniform(90, 170)
        col = rnd.choice(["#4a5a2a", "#5a6a3a", "#6a5a3a", "#3a4a28"])
        b.append(f'<line x1="{x:.0f}" y1="154" x2="{x:.0f}" y2="{170:.0f}" stroke="#8a7a5a" stroke-width="2"/>')
        b.append(f'<path d="M{x-6:.0f},170 L{x+6:.0f},170 L{x + rnd.uniform(18,34):.0f},{170 + L:.0f} L{x - rnd.uniform(18,34):.0f},{170 + L:.0f} Z" fill="{col}"/>')
        for j in range(6):
            b.append(f'<line x1="{x:.0f}" y1="176" x2="{x + rnd.uniform(-30,30):.0f}" y2="{170 + L*rnd.uniform(0.7,1.05):.0f}" stroke="#2a3418" stroke-width="2" opacity="0.6"/>')
    # santos y estampas en la pared
    for k in range(14):
        x = 200 + (k % 7) * 180 + rnd.uniform(-20, 20)
        y = 380 + (k // 7) * 170 + rnd.uniform(-20, 20)
        w_ = rnd.uniform(60, 90)
        b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w_:.0f}" height="{w_*1.35:.0f}" fill="#c9a86a" opacity="0.9"/>')
        b.append(f'<rect x="{x+6:.0f}" y="{y+6:.0f}" width="{w_-12:.0f}" height="{w_*1.35-12:.0f}" fill="{rnd.choice(["#4a3a6a","#6a2a2a","#2a4a5a","#5a4a2a"])}"/>')
        b.append(f'<circle cx="{x + w_/2:.0f}" cy="{y + w_*0.45:.0f}" r="{w_*0.18:.0f}" fill="#e8c8a0" opacity="0.8"/>')
        b.append(f'<circle cx="{x + w_/2:.0f}" cy="{y + w_*0.45:.0f}" r="{w_*0.28:.0f}" fill="none" stroke="#f2d27a" stroke-width="2" opacity="0.7"/>')
    # cruz
    b.append('<rect x="1520" y="300" width="16" height="200" fill="#2a1a0e"/><rect x="1470" y="350" width="116" height="16" fill="#2a1a0e"/>')
    # repisa con frascos
    b.append('<rect x="1360" y="600" width="480" height="14" fill="#24160c"/>')
    for k in range(9):
        x = 1380 + k * 50
        h = rnd.uniform(40, 80)
        b.append(f'<rect x="{x}" y="{600 - h:.0f}" width="34" height="{h:.0f}" rx="8" fill="{rnd.choice(["#3a5a4a","#5a3a2a","#7a6a4a","#2a3a5a"])}" opacity="0.85"/>')
    # fogón con humo que sube derecho
    b.append('<rect y="840" width="1920" height="240" fill="#1e140c"/>')
    b.append('<path d="M760,900 L1160,900 L1120,820 L800,820 Z" fill="#5a3a26"/>')
    b.append(fogata(960, 830, 0.6))
    b.append('<path d="M950,700 C940,500 980,320 960,150 L972,150 C990,320 952,500 966,700 Z" fill="#d8d0c8" opacity="0.25" filter="url(#b8)"/>')
    b.append('<path d="M956,680 L962,150" stroke="#e8e0d8" stroke-width="16" opacity="0.18" filter="url(#b16)"/>')
    b.append(vela(400, 820, 0.8, botella=False))
    b.append(vela(1600, 820, 0.8, botella=False))
    b.append('<rect width="1920" height="1080" fill="#0a0604" opacity="0.2"/>')
    svg = doc("".join(b), DEFS_FUEGO)
    p = f"{BG}/transito.png"
    render(svg, p)
    post(p, grain=7, vignette=0.65, tint=((10, 8, 6), (255, 190, 130)), seed=49)


def casa_adobe(x, ybase, w, h, pared, techo, seed, puerta=True, ventana=True, luz=False):
    rnd = random.Random(seed)
    o = [f'<rect x="{x}" y="{ybase - h}" width="{w}" height="{h}" fill="{pared}"/>']
    o.append(f'<path d="M{x - 14},{ybase - h} L{x + w + 14},{ybase - h} L{x + w},{ybase - h - h*0.22} L{x},{ybase - h - h*0.22} Z" fill="{techo}"/>')
    for k in range(int(w / 14)):
        o.append(f'<line x1="{x + k*14}" y1="{ybase - h - h*0.22}" x2="{x + k*14 - 4}" y2="{ybase - h}" stroke="#000" stroke-width="2" opacity="0.25"/>')
    if puerta:
        px = x + w * rnd.uniform(0.15, 0.6)
        o.append(f'<rect x="{px:.0f}" y="{ybase - h*0.7:.0f}" width="{w*0.16:.0f}" height="{h*0.7:.0f}" fill="#2a1a0e"/>')
    if ventana:
        vx = x + w * 0.72
        col = "#f2b766" if luz else "#14100c"
        o.append(f'<rect x="{vx:.0f}" y="{ybase - h*0.72:.0f}" width="{w*0.14:.0f}" height="{h*0.32:.0f}" fill="{col}"/>')
        for k in range(4):
            o.append(f'<line x1="{vx + k*w*0.14/3:.0f}" y1="{ybase - h*0.72:.0f}" x2="{vx + k*w*0.14/3:.0f}" y2="{ybase - h*0.40:.0f}" stroke="#0a0806" stroke-width="3"/>')
        if luz:
            o.append(f'<circle cx="{vx + w*0.07:.0f}" cy="{ybase - h*0.56:.0f}" r="{h*0.5:.0f}" fill="url(#glowVelaB)" opacity="0.35"/>')
    return "".join(o)


def campanario(x, ybase, esc, color):
    s = esc
    return (f'<rect x="{x - 70*s}" y="{ybase - 260*s}" width="{140*s}" height="{260*s}" fill="{color}"/>'
            f'<rect x="{x - 55*s}" y="{ybase - 360*s}" width="{110*s}" height="{100*s}" fill="{color}"/>'
            f'<path d="M{x - 40*s},{ybase - 330*s} L{x - 40*s},{ybase - 290*s} L{x + 40*s},{ybase - 290*s} L{x + 40*s},{ybase - 330*s} A{40*s},{30*s} 0 0 0 {x - 40*s},{ybase - 330*s} Z" fill="#0a0806" opacity="0.7"/>'
            f'<path d="M{x - 60*s},{ybase - 360*s} L{x},{ybase - 440*s} L{x + 60*s},{ybase - 360*s} Z" fill="{color}"/>'
            f'<rect x="{x - 3*s}" y="{ybase - 490*s}" width="{6*s}" height="{55*s}" fill="{color}"/><rect x="{x - 16*s}" y="{ybase - 478*s}" width="{32*s}" height="{6*s}" fill="{color}"/>')


def calle(modo="noche"):
    if modo == "noche":
        d1 = grad("cieloS", [(0, "#02040c"), (1, "#18263e")])
        pared, techo, suelo = "#3a3634", "#2a1c18", "#1c1814"
    else:
        d1 = grad("cieloS", [(0, "#3a3a6a"), (0.5, "#c98a8a"), (1, "#ffc98a")])
        pared, techo, suelo = "#c9a48a", "#8a4a36", "#a4826a"
    b = [f'<rect width="1920" height="760" fill="url(#cieloS)"/>']
    if modo == "noche":
        b.append(estrellas(500, 441, y_max=450))
        b.append(cerro(560, 200, 442, "#0b111c", rim="#2c3e57"))
    else:
        b.append('<circle cx="960" cy="560" r="400" fill="#ffd8a0" opacity="0.4" filter="url(#b60)"/>')
        b.append(cerro(560, 200, 442, "#6a4a5a", rim="#f0c0a0"))
    b.append(f'<rect y="700" width="1920" height="380" fill="{suelo}"/>')
    # campanario al fondo
    b.append(campanario(1240 if modo == "noche" else 1500, 700, 0.9, "#0e0c0c" if modo == "noche" else "#b08a70"))
    if modo == "noche":
        # casas a ambos lados en perspectiva simple
        for k, (x, w_, h_) in enumerate([(0, 380, 330), (380, 300, 260), (680, 220, 200), (900, 160, 160)]):
            b.append(casa_adobe(x, 760 - k * 20, w_, h_, pared, techo, 450 + k, luz=(k == 1)))
        for k, (x, w_, h_) in enumerate([(1540, 380, 330), (1300, 240, 250), (1130, 170, 190)]):
            b.append(casa_adobe(x, 760 - k * 20, w_, h_, pared, techo, 460 + k, luz=(k == 2)))
        # farol de aceite en la pared
        b.append('<rect x="560" y="380" width="8" height="40" fill="#111"/><path d="M548,420 L580,420 L574,460 L554,460 Z" fill="#ffd27a"/>')
        b.append('<circle cx="564" cy="440" r="260" fill="url(#glowVelaB)" opacity="0.5"/>')
        b.append('<ellipse cx="640" cy="900" rx="500" ry="80" fill="#ffb04a" opacity="0.08" filter="url(#b16)"/>')
    else:
        # plaza con pila y casas bajas
        for k, (x, w_, h_) in enumerate([(0, 420, 300), (420, 340, 250), (1700, 260, 280)]):
            b.append(casa_adobe(x, 740, w_, h_, pared, techo, 470 + k))
        b.append('<ellipse cx="760" cy="880" rx="260" ry="50" fill="#7a6a5a"/><ellipse cx="760" cy="868" rx="240" ry="40" fill="#8a9aa8"/>')
        b.append('<rect x="730" y="720" width="60" height="150" fill="#9a8a7a"/><ellipse cx="760" cy="720" rx="70" ry="18" fill="#a89a8a"/>')
        b.append('<path d="M760,700 q-30,-40 -60,10 M760,700 q30,-40 60,10" stroke="#cfe0ec" stroke-width="5" fill="none" opacity="0.7"/>')
        b.append('<path d="M0,1080 L1920,1080 L1920,940 L0,1000 Z" fill="#000" opacity="0.15"/>')
        b.append('<rect width="1920" height="1080" fill="#ffb07a" opacity="0.08"/>')
    svg = doc("".join(b), d1 + DEFS_FUEGO)
    p = f"{BG}/calle_{'noche' if modo == 'noche' else 'alba'}.png"
    render(svg, p)
    if modo == "noche":
        post(p, grain=7, vignette=0.6, tint=((6, 8, 22), (255, 190, 120)), seed=50)
    else:
        post(p, grain=6, vignette=0.45, tint=((40, 24, 40), (255, 220, 180)), seed=51)


def calle_noche():
    calle("noche")


def calle_alba():
    calle("alba")


def mansion():
    rnd = random.Random(481)
    d1 = grad("cieloM", [(0, "#01030a"), (1, "#14223a")])
    b = ['<rect width="1920" height="1080" fill="#1e2a26"/>']
    # papel mural de damasco
    for i in range(0, 1920, 120):
        for j in range(0, 820, 140):
            b.append(f'<path d="M{i+60},{j+20} C{i+100},{j+50} {i+100},{j+90} {i+60},{j+120} C{i+20},{j+90} {i+20},{j+50} {i+60},{j+20} Z" fill="#2a3a34" opacity="0.8"/>')
    b.append('<rect y="780" width="1920" height="40" fill="#3a2a1c"/><rect y="820" width="1920" height="260" fill="#2a1c14"/>')
    # ventana alta con el Bramador a lo lejos
    b.append('<rect x="1180" y="120" width="520" height="640" fill="url(#cieloM)"/>')
    b.append(f'<g clip-path="url(#ventM)">{estrellas(140, 482, y_max=500, w=1920)}'
             + cerro_bramador(1440, 700, 500, 170, "noche", seed=17, detalle=0.6) + '</g>')
    defs = d1 + '<clipPath id="ventM"><rect x="1180" y="120" width="520" height="640"/></clipPath>'
    b.append('<rect x="1180" y="120" width="520" height="640" fill="none" stroke="#2a1a0e" stroke-width="24"/>')
    b.append('<rect x="1430" y="120" width="20" height="640" fill="#2a1a0e"/><rect x="1180" y="430" width="520" height="16" fill="#2a1a0e"/>')
    b.append('<path d="M1120,90 C1180,300 1150,600 1200,800 L1100,800 C1080,600 1110,300 1080,90 Z" fill="#5a1a22"/>')
    b.append('<path d="M1760,90 C1700,300 1730,600 1680,800 L1780,800 C1800,600 1770,300 1800,90 Z" fill="#5a1a22"/>')
    b.append('<rect x="1060" y="70" width="760" height="30" rx="8" fill="#8a6a2a"/>')
    # lámpara de velas
    b.append('<line x1="700" y1="0" x2="700" y2="160" stroke="#8a6a2a" stroke-width="4"/>')
    b.append('<path d="M560,200 Q700,260 840,200" stroke="#a8862a" stroke-width="8" fill="none"/>')
    for k in range(5):
        x = 580 + k * 60
        b.append(vela(x, 210 + (12 if k in (1, 3) else 20 if k == 2 else 0), 0.6, botella=False, glow=0.6))
    # piano de cola
    b.append('<path d="M120,640 C140,520 520,520 640,600 L700,620 L700,700 L120,700 Z" fill="#0c0a08"/>')
    b.append('<rect x="120" y="700" width="580" height="30" fill="#0a0806"/>')
    for x in (160, 640, 420):
        b.append(f'<rect x="{x}" y="730" width="22" height="130" fill="#0c0a08"/>')
    b.append('<rect x="460" y="640" width="200" height="14" fill="#efe8d8"/>')
    # alfombra y arena en el suelo
    b.append('<path d="M200,1080 L520,860 L1500,860 L1820,1080 Z" fill="#5a2a1e"/>')
    b.append('<path d="M260,1060 L540,880 L1480,880 L1760,1060 Z" fill="none" stroke="#a8862a" stroke-width="6" opacity="0.6"/>')
    for k in range(12):
        x = rnd.uniform(1000, 1800)
        y = rnd.uniform(830, 1060)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(40,160):.0f}" ry="{rnd.uniform(8,22):.0f}" fill="#c9b48a" opacity="{rnd.uniform(0.35,0.7):.2f}" filter="url(#b4)"/>')
    b.append('<path d="M1200,790 C1300,780 1500,800 1700,795 L1700,830 L1200,830 Z" fill="#c9b48a" opacity="0.7" filter="url(#b2)"/>')
    # sillón vacío
    b.append('<path d="M760,880 L760,700 Q760,660 800,660 L960,660 Q1000,660 1000,700 L1000,880 Z" fill="#3a1418"/>')
    b.append('<rect x="740" y="760" width="40" height="140" rx="10" fill="#2a0e10"/><rect x="980" y="760" width="40" height="140" rx="10" fill="#2a0e10"/>')
    b.append('<rect width="1920" height="1080" fill="#06101a" opacity="0.28"/>')
    svg = doc("".join(b), defs + DEFS_FUEGO)
    p = f"{BG}/mansion.png"
    render(svg, p)
    post(p, grain=7, vignette=0.65, tint=((6, 10, 20), (255, 200, 140)), seed=52)


def caverna():
    rnd = random.Random(491)
    d1 = grad("oroV", [(0, "#fff0a8"), (0.5, "#f0b93c"), (1, "#8a5a10")])
    d2 = grad("oroH", [(0, "#8a5a10"), (0.5, "#ffe08a"), (1, "#8a5a10")], vertical=False)
    b = ['<rect width="1920" height="1080" fill="#0c0704"/>']
    b.append('<ellipse cx="960" cy="560" rx="900" ry="420" fill="#3a2008" opacity="0.8" filter="url(#b60)"/>')
    b.append('<ellipse cx="960" cy="620" rx="620" ry="260" fill="#f0b93c" opacity="0.35" filter="url(#b60)"/>')
    # ciudad de oro al fondo
    ciudad = []
    x = 360
    while x < 1560:
        w_ = rnd.uniform(60, 130)
        h_ = rnd.uniform(120, 300) * (1 - abs(x - 960) / 1400)
        yb = 720
        ciudad.append(f'<rect x="{x:.0f}" y="{yb - h_:.0f}" width="{w_:.0f}" height="{h_ + 10:.0f}" fill="url(#oroV)"/>')
        if rnd.random() < 0.4:
            ciudad.append(f'<path d="M{x:.0f},{yb - h_:.0f} L{x + w_/2:.0f},{yb - h_ - rnd.uniform(40,120):.0f} L{x + w_:.0f},{yb - h_:.0f} Z" fill="#ffe08a"/>')
        elif rnd.random() < 0.5:
            ciudad.append(f'<path d="M{x:.0f},{yb - h_:.0f} A{w_/2:.0f},{w_/2:.0f} 0 0 1 {x + w_:.0f},{yb - h_:.0f} Z" fill="#ffd060"/>')
        for k in range(rnd.randint(1, 3)):
            ax = x + w_ * rnd.uniform(0.2, 0.7)
            ay = yb - h_ * rnd.uniform(0.3, 0.8)
            ciudad.append(f'<path d="M{ax:.0f},{ay + 30:.0f} L{ax:.0f},{ay:.0f} A10,10 0 0 1 {ax + 20:.0f},{ay:.0f} L{ax + 20:.0f},{ay + 30:.0f} Z" fill="#6a400a"/>')
        x += w_ * rnd.uniform(0.7, 1.0)
    b.append("".join(ciudad))
    # trono de cuarzo al centro
    b.append('<path d="M900,720 L920,560 L960,520 L1000,560 L1020,720 Z" fill="#e8f0f4" opacity="0.8"/>')
    for k in range(9):
        a = -1.2 + k * 0.3
        b.append(f'<path d="M960,720 L{960 + math.sin(a)*120:.0f},{720 - math.cos(a)*rnd.uniform(140,240):.0f} L{960 + math.sin(a)*100 + 20:.0f},{720:.0f} Z" fill="#dfeaf0" opacity="0.55"/>')
    b.append('<rect x="860" y="720" width="200" height="30" fill="#f2d27a"/>')
    # plaza / suelo de oro
    b.append('<path d="M0,1080 L560,740 L1360,740 L1920,1080 Z" fill="url(#oroH)" opacity="0.9"/>')
    for k in range(10):
        b.append(f'<line x1="{560 + k*89}" y1="740" x2="{-200 + k*236}" y2="1080" stroke="#8a5a10" stroke-width="2" opacity="0.5"/>')
    # paredes de la caverna con vetas y caras
    b.append('<path d="M0,0 L520,0 L440,300 L560,740 L0,1080 Z" fill="#1e1206"/>')
    b.append('<path d="M1920,0 L1400,0 L1480,300 L1360,740 L1920,1080 Z" fill="#1a1005"/>')
    for k in range(40):
        side = rnd.choice([-1, 1])
        x0 = rnd.uniform(0, 480) if side < 0 else rnd.uniform(1440, 1920)
        y0 = rnd.uniform(0, 1000)
        d = f"M{x0:.0f},{y0:.0f}"
        for j in range(4):
            x0 += rnd.uniform(-60, 60)
            y0 += rnd.uniform(20, 70)
            d += f" L{x0:.0f},{y0:.0f}"
        b.append(f'<path d="{d}" stroke="#f0b93c" stroke-width="{rnd.uniform(2,6):.1f}" fill="none" opacity="0.8"/>')
    # caras fundidas en el oro
    for (fx, fy, fr) in [(180, 380, 46), (330, 560, 40), (120, 740, 52), (300, 860, 44), (1720, 360, 48), (1600, 560, 40),
                         (1780, 700, 50), (1620, 860, 44), (420, 220, 30), (1500, 220, 30)]:
        b.append(f'<ellipse cx="{fx}" cy="{fy}" rx="{fr*0.78:.0f}" ry="{fr:.0f}" fill="#b07a1e" opacity="0.85"/>')
        b.append(f'<ellipse cx="{fx}" cy="{fy}" rx="{fr*0.78:.0f}" ry="{fr:.0f}" fill="none" stroke="#f0c050" stroke-width="2" opacity="0.6"/>')
        for ex in (-0.3, 0.3):
            b.append(f'<ellipse cx="{fx + ex*fr:.0f}" cy="{fy - fr*0.2:.0f}" rx="{fr*0.14:.0f}" ry="{fr*0.1:.0f}" fill="#2a1604"/>')
        b.append(f'<ellipse cx="{fx}" cy="{fy + fr*0.42:.0f}" rx="{fr*0.15:.0f}" ry="{fr*0.2:.0f}" fill="#2a1604"/>')
        b.append(f'<path d="M{fx - fr*0.1:.0f},{fy - fr*0.05:.0f} L{fx:.0f},{fy + fr*0.2:.0f}" stroke="#7a4a10" stroke-width="2"/>')
    # techo con estalactitas
    b.append('<path d="M0,0 L1920,0 L1920,120 ' + " ".join(f"L{x},{120 + (40 + 60*abs(math.sin(x*0.013)))*(1 if (x//60)%2 else 0.4):.0f}" for x in range(1920, -1, -60)) + ' Z" fill="#0a0603"/>')
    # polvo dorado en el aire
    for k in range(120):
        b.append(f'<circle cx="{rnd.uniform(300,1620):.0f}" cy="{rnd.uniform(200,900):.0f}" r="{rnd.uniform(1,3):.1f}" fill="#ffe8a0" opacity="{rnd.uniform(0.3,0.9):.2f}"/>')
    b.append('<ellipse cx="960" cy="600" rx="500" ry="300" fill="#fff0b0" opacity="0.10" filter="url(#b60)"/>')
    svg = doc("".join(b), d1 + d2 + DEFS_FUEGO)
    p = f"{BG}/caverna.png"
    render(svg, p)
    post(p, grain=7, vignette=0.7, tint=((20, 10, 2), (255, 220, 150)), seed=53)


TODOS_FONDOS = ["cerro_noche", "cerro_tarde", "ladera", "puerta", "campamento", "desierto_alba", "chingana", "oficina",
                "rancho", "transito", "calle_noche", "calle_alba", "mansion", "caverna"]
