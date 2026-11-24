"""Personajes de EL BRAMADOR (820x1080, fondo transparente)."""
import math
import random
import sys

from rasgos import *

SP = OUT + "/sprites"
CAB = '<g transform="translate(411 480) scale(1.2) translate(-411 -480)">'


def boca_abierta(cx, cy, w, h, dientes=True, labio="#9a5a52"):
    o = [f'<path d="M{cx-w/2:.1f},{cy:.1f} Q{cx:.1f},{cy-h*0.35:.1f} {cx+w/2:.1f},{cy:.1f} Q{cx:.1f},{cy+h:.1f} {cx-w/2:.1f},{cy:.1f} Z" fill="#2a0c0c" stroke="{LINE}" stroke-width="2.5"/>']
    if dientes:
        o.append(f'<path d="M{cx-w*0.38:.1f},{cy-h*0.05:.1f} Q{cx:.1f},{cy-h*0.28:.1f} {cx+w*0.38:.1f},{cy-h*0.05:.1f} L{cx+w*0.34:.1f},{cy+h*0.12:.1f} Q{cx:.1f},{cy:.1f} {cx-w*0.34:.1f},{cy+h*0.12:.1f} Z" fill="#efe6d6"/>')
    o.append(f'<path d="M{cx-w*0.25:.1f},{cy+h*0.55:.1f} Q{cx:.1f},{cy+h*0.75:.1f} {cx+w*0.25:.1f},{cy+h*0.55:.1f}" stroke="{labio}" stroke-width="3" fill="none" opacity="0.6"/>')
    return "".join(o)


def ojos_miedo(cx, cy, w, h, iris="#2a1c18", lado=-1):
    """Ojo muy abierto con iris chico."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h}" fill="#f2eee8" stroke="{LINE}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{h*0.42:.1f}" fill="{iris}"/><circle cx="{cx}" cy="{cy}" r="{h*0.2:.1f}" fill="#000"/>'
            f'<circle cx="{cx + h*0.15:.1f}" cy="{cy - h*0.15:.1f}" r="{h*0.1:.1f}" fill="#fff"/>')


def guardar_sprite(nombre, body, defs=""):
    p = f"{SP}/{nombre}.png"
    render(sdoc(body, defs), p)
    post_sprite(p, grain=3)
    return p


# ---------------------------------------------------------------------------
#  ROSARIO
# ---------------------------------------------------------------------------

def rosario(estado="neutral"):
    piel, som = "#d6a27e", "#9a6a52"
    pelo = "#1a120e"
    b = []
    defs = ('<pattern id="rebozo" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#34465a"/>'
            '<path d="M0,8 L16,8" stroke="#2a3a4c" stroke-width="3"/><path d="M8,0 L8,16" stroke="#3e5268" stroke-width="1"/></pattern>')
    # trenzas de atrás
    b.append(f'<path d="M318,320 C300,420 320,480 340,520 L380,520 C360,470 350,400 360,330 Z" fill="{pelo}"/>')
    # cuello y cuerpo
    b.append(f'<path d="M376,440 L370,560 L452,560 L446,440 Z" fill="{piel}"/>')
    b.append(f'<path d="M376,456 Q411,496 446,456 L448,520 Q411,540 374,520 Z" fill="{som}" opacity="0.6"/>')
    b.append(f'<path d="M340,540 C280,556 210,580 180,620 C150,664 140,760 136,860 L128,1080 L694,1080 L686,860 C682,760 672,664 642,620 C612,580 542,556 482,540 Z" fill="#7a2a22" stroke="{LINE}" stroke-width="4"/>')
    # blusa blanca con escote redondo
    b.append(f'<path d="M340,540 Q411,600 482,540 L500,560 Q411,640 322,560 Z" fill="#efe8dc" stroke="{LINE}" stroke-width="3"/>')
    # rebozo cruzado sobre el pecho
    b.append(f'<path d="M190,610 C230,570 300,548 352,548 C360,640 420,720 520,780 L600,1080 L140,1080 L150,860 C150,760 160,660 190,610 Z" fill="url(#rebozo)" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M632,610 C592,570 522,548 470,548 C460,640 400,720 300,800 L330,1080 L690,1080 L676,860 C676,760 664,660 632,610 Z" fill="url(#rebozo)" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M632,610 C664,660 676,760 676,860 L690,1080 L560,1080 C580,860 600,700 590,600 Z" fill="#141c26" opacity="0.5"/>')
    for k in range(14):
        x = 330 + k * 22
        b.append(f'<line x1="{x}" y1="1040" x2="{x - 4}" y2="1080" stroke="#2a3a4c" stroke-width="3"/>')
    # trenzas delanteras sobre el rebozo
    for side, x0 in ((-1, 336), (1, 486)):
        for k in range(8):
            y = 470 + k * 34
            b.append(f'<ellipse cx="{x0 + side*k*3}" cy="{y}" rx="15" ry="20" fill="{pelo}" stroke="#000" stroke-width="1.5"/>')
        b.append(f'<path d="M{x0 + side*24 - 8},{746} l16,0 l-4,18 l-8,0 Z" fill="#a3192d"/>')
    b.append(CAB)
    b.append(orejas(330, 492, 344, piel, som, ry=26))
    b.append(f'<circle cx="330" cy="374" r="5" fill="#e0b040"/><circle cx="492" cy="374" r="5" fill="#e0b040"/>')
    face = "M332,298 C332,222 490,222 490,298 C492,372 466,432 411,462 C356,432 330,372 332,298 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M490,300 C492,372 466,432 411,462 C450,424 470,372 474,300 Z" fill="{som}" opacity="0.5"/>')
    b.append(f'<ellipse cx="366" cy="390" rx="20" ry="11" fill="#d0705a" opacity="0.22"/><ellipse cx="456" cy="390" rx="20" ry="11" fill="#d0705a" opacity="0.18"/>')
    b.append(ceja(372, 306, 48, estado, -1, pelo, 5))
    b.append(ceja(450, 306, 48, estado, 1, pelo, 5))
    b.append(ojo(372, 338, 46, 13, estado, -1, iris="#2a1a10", piel_sombra=som))
    b.append(ojo(450, 338, 46, 13, estado, 1, iris="#2a1a10", piel_sombra=som))
    b.append(f'<path d="M414,342 Q422,372 414,384" stroke="{som}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M401,388 Q411,394 421,388" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.5"/>')
    b.append(boca(411, 418, 38, estado, labio="#a85a54"))
    # pelo partido al medio, tirante hacia atrás
    b.append(f'<path d="M326,320 C316,226 360,188 411,188 C462,188 506,226 496,320 C486,262 452,232 411,236 C370,232 336,262 326,320 Z" fill="{pelo}" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<path d="M411,190 L411,236" stroke="#3a2a22" stroke-width="2"/>')
    b.append(f'<path d="M350,230 C370,206 400,198 408,198 M472,230 C452,206 422,198 414,198" stroke="#4a3a3a" stroke-width="3" fill="none" opacity="0.6"/>')
    b.append('</g>')
    return guardar_sprite(f"rosario_{estado}", "".join(b), defs)


# ---------------------------------------------------------------------------
#  CELESTINO
# ---------------------------------------------------------------------------

def celestino(estado="neutral"):
    piel, som = "#b07a58", "#7a4e38"
    b = []
    defs = ('<pattern id="ponchoC" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#6e4a30"/>'
            '<path d="M0,10 L60,10" stroke="#a3743f" stroke-width="6"/><path d="M0,22 L60,22" stroke="#3a2618" stroke-width="4"/>'
            '<path d="M0,44 L60,44" stroke="#8a2a20" stroke-width="5"/></pattern>')
    b.append(f'<path d="M372,446 L364,560 L458,560 L450,446 Z" fill="{piel}"/>')
    b.append(f'<path d="M362,520 L460,520 C560,560 690,640 760,760 L790,1080 L30,1080 L60,760 C130,640 262,560 362,520 Z" fill="url(#ponchoC)" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M460,520 C560,560 690,640 760,760 L790,1080 L540,1080 C570,860 550,680 460,560 Z" fill="#1d130c" opacity="0.4"/>')
    for k in range(30):
        x = 40 + k * 25
        b.append(f'<line x1="{x}" y1="1050" x2="{x - 3}" y2="1080" stroke="#3a2618" stroke-width="4"/>')
    # pañuelo rojo al cuello
    b.append(f'<path d="M354,520 C380,556 444,556 470,520 L482,550 C450,590 372,590 340,550 Z" fill="#a3192d" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M400,570 L420,640 L440,572 Z" fill="#8a1424" stroke="{LINE}" stroke-width="2"/>')
    b.append(CAB)
    b.append(orejas(322, 500, 344, piel, som))
    face = "M324,296 C324,214 498,214 498,296 C500,376 472,440 411,470 C350,440 322,376 324,296 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M498,300 C500,376 472,440 411,470 C456,428 478,376 480,300 Z" fill="{som}" opacity="0.5"/>')
    # arrugas
    for y in (262, 276):
        b.append(f'<path d="M374,{y} Q411,{y-6} 448,{y}" stroke="{som}" stroke-width="2" fill="none" opacity="0.8"/>')
    b.append(f'<path d="M384,388 Q370,410 378,436 M438,388 Q452,410 444,436" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.4"/>')
    # barba de días
    rnd = random.Random(7)
    for _ in range(200):
        x = rnd.uniform(346, 476)
        y = rnd.uniform(404, 466)
        if (x - 411) ** 2 / 70 ** 2 + (y - 400) ** 2 / 68 ** 2 < 1.1:
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.3" fill="#7a7068" opacity="0.6"/>')
    if estado == "miedo":
        b.append(ceja(370, 300, 52, "triste", -1, "#3a3430", 7))
        b.append(ceja(452, 300, 52, "triste", 1, "#3a3430", 7))
        b.append(ojos_miedo(370, 336, 40, 13))
        b.append(ojos_miedo(452, 336, 40, 13))
    else:
        b.append(ceja(370, 304, 52, "sonrisa" if estado == "risa" else "neutral", -1, "#3a3430", 7))
        b.append(ceja(452, 304, 52, "sonrisa" if estado == "risa" else "neutral", 1, "#3a3430", 7))
        e = "sonrisa" if estado == "risa" else "neutral"
        b.append(ojo(370, 336, 40, 10, e, -1, iris="#2a1a12", pest=3.5, viejo=True, piel_sombra=som))
        b.append(ojo(452, 336, 40, 10, e, 1, iris="#2a1a12", pest=3.5, viejo=True, piel_sombra=som))
    b.append(f'<path d="M412,336 Q426,378 416,394" stroke="{som}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M394,396 Q411,406 430,396" stroke="{LINE}" stroke-width="2.4" fill="none" opacity="0.6"/>')
    # bigote
    b.append(f'<path d="M370,414 C382,402 404,404 411,408 C418,404 440,402 452,414 C444,426 428,424 411,420 C394,424 378,426 370,414 Z" fill="#4a4440"/>')
    if estado == "risa":
        b.append(boca_abierta(411, 432, 52, 24))
    elif estado == "miedo":
        b.append(boca_abierta(411, 434, 30, 30, dientes=False))
    else:
        b.append(f'<path d="M394,436 Q411,442 428,436" stroke="{LINE}" stroke-width="2.4" fill="none"/>')
    # chupalla
    b.append(f'<ellipse cx="411" cy="250" rx="190" ry="40" fill="#c9a86a" stroke="{LINE}" stroke-width="3"/>')
    for k in range(18):
        a = k / 18 * math.pi * 2
        b.append(f'<line x1="{411 + math.cos(a)*60:.0f}" y1="{250 + math.sin(a)*14:.0f}" x2="{411 + math.cos(a)*186:.0f}" y2="{250 + math.sin(a)*38:.0f}" stroke="#a8884a" stroke-width="2"/>')
    b.append(f'<path d="M330,250 C326,180 350,150 411,148 C472,150 496,180 492,250 C460,262 362,262 330,250 Z" fill="#d6b67a" stroke="{LINE}" stroke-width="3"/>')
    for k in range(6):
        y = 170 + k * 14
        b.append(f'<path d="M{334 + k*1},{y} Q411,{y - 8} {488 - k*1},{y}" stroke="#a8884a" stroke-width="2" fill="none"/>')
    b.append(f'<path d="M332,232 C362,244 460,244 490,232 L492,250 C460,262 362,262 330,250 Z" fill="#2a1a10"/>')
    b.append('</g>')
    return guardar_sprite(f"celestino_{estado}", "".join(b), defs)


# ---------------------------------------------------------------------------
#  DON FERMÍN
# ---------------------------------------------------------------------------

def fermin(estado="neutral"):
    piel, som = "#e3c3aa", "#a88a7a"
    canas = "#bdb8b0"
    b = []
    b.append(f'<path d="M372,440 L366,560 L456,560 L450,440 Z" fill="{piel}"/>')
    # levita negra
    b.append(f'<path d="M348,532 C280,548 200,576 160,620 C120,666 110,770 106,870 L96,1080 L726,1080 L716,870 C712,770 702,666 662,620 C622,576 542,548 474,532 Z" fill="#15171c" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M160,620 C120,666 110,770 106,870 L100,1000 C140,860 150,720 200,612 Z" fill="#3a4250" opacity="0.4"/>')
    # chaleco gris y cadena de reloj
    b.append(f'<path d="M350,540 L411,700 L472,540 L500,1080 L322,1080 Z" fill="#4a4a54" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M340,840 Q400,880 470,830" stroke="#e0b040" stroke-width="4" fill="none"/>')
    for y in (760, 860, 960):
        b.append(f'<circle cx="411" cy="{y}" r="7" fill="#2a2a30"/>')
    # cuello alto y corbatín
    b.append(f'<path d="M360,528 L384,590 L411,560 Z" fill="#f4f0e8" stroke="{LINE}" stroke-width="2.5"/>')
    b.append(f'<path d="M462,528 L438,590 L411,560 Z" fill="#dcd6cc" stroke="{LINE}" stroke-width="2.5"/>')
    b.append(f'<path d="M376,548 Q411,570 446,548 L440,590 Q411,606 382,590 Z" fill="#0a0a0c"/>')
    b.append(f'<path d="M396,590 L411,640 L426,590 Z" fill="#0a0a0c"/>')
    # solapas
    b.append(f'<path d="M348,540 L300,650 L360,700 L396,600 Z" fill="#0c0e12" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M474,540 L522,650 L462,700 L426,600 Z" fill="#090a0d" stroke="{LINE}" stroke-width="3"/>')
    b.append(CAB)
    b.append(orejas(326, 496, 344, piel, som))
    face = "M328,298 C328,214 494,214 494,298 C496,380 468,442 411,472 C354,442 326,380 328,298 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M494,300 C496,380 468,442 411,472 C452,430 474,380 476,300 Z" fill="{som}" opacity="0.5"/>')
    # patillas grandes
    b.append(f'<path d="M330,300 C326,350 334,400 352,430 C362,410 360,360 356,300 Z" fill="{canas}" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<path d="M492,300 C496,350 488,400 470,430 C460,410 462,360 466,300 Z" fill="#9a958e" stroke="{LINE}" stroke-width="2"/>')
    for y in (258, 270):
        b.append(f'<path d="M376,{y} Q411,{y-6} 446,{y}" stroke="{som}" stroke-width="2" fill="none" opacity="0.7"/>')
    e = "sonrisa" if estado == "sonrisa" else "neutral"
    b.append(ceja(372, 304, 50, "ceño", -1, "#8a8680", 6))
    b.append(ceja(450, 304, 50, "ceño", 1, "#8a8680", 6))
    b.append(ojo(372, 338, 40, 8 if estado == "neutral" else 7, e, -1, iris="#3a4a5a", pest=3, viejo=True, piel_sombra=som))
    b.append(ojo(450, 338, 40, 8 if estado == "neutral" else 7, e, 1, iris="#3a4a5a", pest=3, viejo=True, piel_sombra=som))
    b.append(f'<path d="M414,338 Q426,382 418,396" stroke="{som}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M398,400 Q411,408 426,400" stroke="{LINE}" stroke-width="2.4" fill="none" opacity="0.6"/>')
    if estado == "sonrisa":
        b.append(f'<path d="M386,428 Q411,446 440,424" stroke="{LINE}" stroke-width="2.8" fill="none" stroke-linecap="round"/>')
        b.append(f'<path d="M438,420 l6,-4" stroke="{LINE}" stroke-width="2.4"/>')
    else:
        b.append(f'<path d="M390,432 Q411,436 432,432" stroke="{LINE}" stroke-width="2.6" fill="none"/>')
    b.append(f'<path d="M380,394 Q368,414 380,440 M442,394 Q454,414 442,440" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.4"/>')
    # pelo canoso peinado de lado
    b.append(f'<path d="M326,296 C316,214 360,180 416,180 C474,180 508,220 496,298 C486,250 460,226 430,226 C404,224 370,232 352,262 C344,272 336,284 326,296 Z" fill="{canas}" stroke="{LINE}" stroke-width="2.5"/>')
    b.append(f'<path d="M380,196 C400,214 440,222 486,240" stroke="#8a8680" stroke-width="2" fill="none"/>')
    b.append('</g>')
    return guardar_sprite(f"fermin_{estado}", "".join(b))


# ---------------------------------------------------------------------------
#  DOÑA TRÁNSITO
# ---------------------------------------------------------------------------

def transito():
    piel, som = "#8a5a40", "#5a3a2a"
    b = []
    # rebozo negro que cubre la cabeza y el cuerpo
    b.append(f'<path d="M300,250 C300,140 520,140 522,250 C560,420 640,520 700,640 L740,1080 L80,1080 L120,640 C180,520 262,420 300,250 Z" fill="#1e1a22" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M522,250 C560,420 640,520 700,640 L740,1080 L560,1080 C600,800 580,560 500,360 Z" fill="#0e0c12" opacity="0.6"/>')
    for k in range(10):
        b.append(f'<path d="M{200 + k*40},{700 + (k%3)*10} q10,120 -10,360" stroke="#2c2632" stroke-width="3" fill="none" opacity="0.7"/>')
    # collar de semillas
    for k in range(18):
        a = math.pi * (0.15 + 0.7 * k / 17)
        b.append(f'<circle cx="{411 + math.cos(a)*120:.0f}" cy="{560 + math.sin(a)*120:.0f}" r="7" fill="{["#8a3a20","#c9a050","#5a2a18"][k%3]}"/>')
    b.append(f'<path d="M405,676 l12,0 l-6,22 Z" fill="#c9a050"/>')
    # manos juntas sosteniendo un manojo de ruda
    b.append(f'<path d="M330,860 C350,820 470,820 490,860 C480,900 340,900 330,860 Z" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    for k in range(7):
        b.append(f'<path d="M{400 + k*4},850 q{-30 + k*10},-80 {-40 + k*14},-130" stroke="#4a6a2a" stroke-width="5" fill="none"/>')
    b.append(CAB)
    face = "M338,300 C338,226 484,226 484,300 C486,372 462,430 411,458 C360,430 336,372 338,300 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M484,300 C486,372 462,430 411,458 C448,420 466,372 468,300 Z" fill="{som}" opacity="0.55"/>')
    # arrugas profundas
    for y in (262, 274, 286):
        b.append(f'<path d="M370,{y} Q411,{y-7} 452,{y}" stroke="{som}" stroke-width="2.4" fill="none"/>')
    for d in ("M384,388 Q366,412 376,440", "M438,388 Q456,412 446,440", "M364,404 Q370,424 386,440", "M458,404 Q452,424 436,440",
              "M392,446 Q411,452 430,446"):
        b.append(f'<path d="{d}" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.45"/>')
    b.append(ceja(374, 306, 44, "neutral", -1, "#d8d4cc", 5))
    b.append(ceja(448, 306, 44, "neutral", 1, "#d8d4cc", 5))
    b.append(ojo(374, 336, 34, 7, "neutral", -1, iris="#1a0e08", pest=3, viejo=True, piel_sombra=som))
    b.append(ojo(448, 336, 34, 7, "neutral", 1, iris="#1a0e08", pest=3, viejo=True, piel_sombra=som))
    b.append(f'<path d="M413,338 Q424,378 416,392" stroke="{som}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M396,394 Q411,402 428,394" stroke="{LINE}" stroke-width="2.4" fill="none" opacity="0.6"/>')
    b.append(f'<path d="M392,424 Q411,430 430,422" stroke="{LINE}" stroke-width="2.6" fill="none"/>')
    # trenzas blancas asomando
    for side, x0 in ((-1, 346), (1, 476)):
        for k in range(5):
            b.append(f'<ellipse cx="{x0 + side*4}" cy="{440 + k*26}" rx="11" ry="15" fill="#e6e2dc" stroke="#8a8680" stroke-width="1.5"/>')
    # borde del rebozo sobre la frente
    b.append(f'<path d="M318,300 C318,200 504,200 504,300 C490,250 450,232 411,232 C372,232 332,250 318,300 Z" fill="#1e1a22" stroke="{LINE}" stroke-width="3"/>')
    b.append('</g>')
    return guardar_sprite("transito_neutral", "".join(b))


# ---------------------------------------------------------------------------
#  ULISES
# ---------------------------------------------------------------------------

def ulises(estado="neutral"):
    lucido = estado == "lucido"
    piel, som = ("#c09070", "#86604a") if lucido else ("#a98060", "#6e5040")
    pelo = "#7a6a5a" if lucido else "#5a4a3a"
    rnd = random.Random(11)
    b = []
    # poncho raído
    borde = "".join(f" L{x},{1080 - (0 if lucido else rnd.uniform(0, 40)):.0f}" for x in range(790, 29, -40))
    b.append(f'<path d="M362,520 L460,520 C560,560 690,640 760,760 L790,1080{borde} L30,1080 L60,760 C130,640 262,560 362,520 Z" fill="#5a5048" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M460,520 C560,560 690,640 760,760 L790,1080 L540,1080 C570,860 550,680 460,560 Z" fill="#1e1a16" opacity="0.45"/>')
    if not lucido:
        for k in range(8):
            x, y = rnd.uniform(120, 700), rnd.uniform(700, 1000)
            b.append(f'<path d="M{x:.0f},{y:.0f} l{rnd.uniform(-30,30):.0f},{rnd.uniform(20,50):.0f} l{rnd.uniform(10,30):.0f},{rnd.uniform(-10,10):.0f}" stroke="#2a2420" stroke-width="3" fill="none"/>')
    b.append(CAB)
    # pelo largo detrás
    if lucido:
        b.append(f'<path d="M318,300 C300,200 360,170 411,170 C462,170 522,200 504,300 C510,380 500,440 480,470 L342,470 C322,440 312,380 318,300 Z" fill="{pelo}"/>')
    else:
        mech = "".join(f'<path d="M{411 + math.cos(a)*100:.0f},{300 + math.sin(a)*120:.0f} q{math.cos(a)*40 + rnd.uniform(-20,20):.0f},{math.sin(a)*40 + rnd.uniform(-10,30):.0f} {math.cos(a)*90 + rnd.uniform(-30,30):.0f},{math.sin(a)*70 + rnd.uniform(0,80):.0f}" stroke="{pelo}" stroke-width="{rnd.uniform(10,22):.0f}" fill="none" stroke-linecap="round"/>'
                       for a in np.linspace(math.pi * 0.95, math.pi * 2.05, 22))
        b.append(mech)
        b.append(f'<path d="M304,320 C290,190 360,150 411,150 C470,150 534,190 518,320 C530,400 520,470 500,500 L322,500 C302,470 292,400 304,320 Z" fill="{pelo}"/>')
    b.append(orejas(324, 498, 344, piel, som))
    face = "M328,298 C328,218 494,218 494,298 C496,376 468,436 411,466 C354,436 326,376 328,298 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M494,300 C496,376 468,436 411,466 C452,426 474,376 476,300 Z" fill="{som}" opacity="0.5"/>')
    if not lucido:
        for _ in range(30):
            b.append(f'<circle cx="{rnd.uniform(340,480):.0f}" cy="{rnd.uniform(240,420):.0f}" r="{rnd.uniform(3,9):.0f}" fill="#4a3a2a" opacity="0.18"/>')
    for y in (258, 270, 282):
        b.append(f'<path d="M372,{y} Q411,{y-6} 450,{y}" stroke="{som}" stroke-width="2" fill="none" opacity="0.7"/>')
    if lucido:
        b.append(ceja(370, 304, 50, "neutral", -1, "#5a4a3a", 6))
        b.append(ceja(452, 304, 50, "neutral", 1, "#5a4a3a", 6))
        b.append(ojo(370, 338, 40, 11, "neutral", -1, iris="#5a7a8a", pest=3, viejo=True, humedo=True, piel_sombra=som))
        b.append(ojo(452, 338, 40, 11, "neutral", 1, iris="#5a7a8a", pest=3, viejo=True, humedo=True, piel_sombra=som))
    else:
        b.append(ceja(370, 298, 52, "triste", -1, "#3a3028", 7))
        b.append(ceja(452, 296, 52, "ceño", 1, "#3a3028", 7))
        b.append(ojos_miedo(370, 338, 42, 14, iris="#8a7a3a"))
        b.append(ojos_miedo(454, 336, 42, 15, iris="#8a7a3a"))
        b.append(f'<path d="M346,358 Q370,372 394,358 M430,358 Q454,374 478,358" stroke="{som}" stroke-width="4" fill="none" opacity="0.7"/>')
    b.append(f'<path d="M413,340 Q426,380 416,394" stroke="{som}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # barba larga
    if lucido:
        b.append(f'<path d="M344,394 C352,470 380,520 411,530 C442,520 470,470 478,394 C460,420 440,428 411,430 C382,428 362,420 344,394 Z" fill="{pelo}" stroke="{LINE}" stroke-width="2"/>')
        b.append(f'<path d="M392,414 Q411,424 430,414" stroke="#2a2018" stroke-width="2.6" fill="none"/>')
    else:
        b.append(f'<path d="M336,390 C330,500 360,620 400,660 L420,600 L436,670 C470,600 498,500 486,390 C462,420 440,430 411,432 C382,430 360,420 336,390 Z" fill="{pelo}" stroke="{LINE}" stroke-width="2"/>')
        for k in range(30):
            x = rnd.uniform(350, 470)
            y = rnd.uniform(440, 640)
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5,3.5):.1f}" fill="#f2c84a" opacity="0.9"/>')
        for k in range(14):
            x = rnd.uniform(350, 470)
            b.append(f'<path d="M{x:.0f},440 q{rnd.uniform(-10,10):.0f},100 {rnd.uniform(-20,20):.0f},{rnd.uniform(120,200):.0f}" stroke="#3a3026" stroke-width="2" fill="none" opacity="0.6"/>')
        b.append(f'<ellipse cx="411" cy="418" rx="14" ry="9" fill="#2a0c0c"/>')
    b.append('</g>')
    return guardar_sprite(f"ulises_{'lucido' if lucido else 'neutral'}", "".join(b))


# ---------------------------------------------------------------------------
#  EL CABALLERO
# ---------------------------------------------------------------------------

def caballero(estado="neutral"):
    piel, som = "#ece2d8", "#a8a0b0"
    b = []
    defs = ('<radialGradient id="ojoGlow"><stop offset="0" stop-color="#ffe08a" stop-opacity="0.95"/>'
            '<stop offset="1" stop-color="#d4a24a" stop-opacity="0"/></radialGradient>')
    if estado == "revelado":
        # sombra con cuernos y cola, detrás de la figura
        b.append('<g opacity="0.85">'
                 '<path d="M120,1080 C100,800 160,600 260,520 C220,420 230,300 290,220 C270,140 250,70 300,20 C320,90 330,150 350,190 '
                 'C390,170 430,170 470,190 C490,150 500,90 520,20 C570,70 550,140 530,220 C590,300 600,420 560,520 C660,600 720,800 700,1080 Z" fill="#120406"/>'
                 '<path d="M690,900 C800,860 820,760 760,700 C740,680 780,640 800,680" stroke="#120406" stroke-width="26" fill="none" stroke-linecap="round"/>'
                 '<path d="M796,676 L830,650 L812,700 Z" fill="#120406"/>'
                 '</g>')
        b.append('<path d="M120,1080 C100,800 160,600 260,520" stroke="#d4602a" stroke-width="6" fill="none" opacity="0.5" filter="url(#b4)"/>')
    # levita negra con botones de plata
    b.append(f'<path d="M372,440 L366,560 L456,560 L450,440 Z" fill="{piel}"/>')
    b.append(f'<path d="M350,530 C280,546 200,576 160,620 C120,666 110,770 106,870 L96,1080 L726,1080 L716,870 C712,770 702,666 662,620 C622,576 542,546 472,530 Z" fill="#0c0b10" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M160,620 C120,666 110,770 106,870 L100,1000 C140,860 150,720 200,612 Z" fill="#4a3a5a" opacity="0.35"/>')
    b.append(f'<path d="M356,536 L411,690 L466,536 Z" fill="#f2eee8" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M376,548 Q411,572 446,548 L436,600 Q411,616 386,600 Z" fill="#060508"/>')
    b.append(f'<circle cx="411" cy="606" r="6" fill="#e0b040"/>')
    b.append(f'<path d="M350,540 L296,660 L360,712 L398,604 Z" fill="#050407" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M472,540 L526,660 L462,712 L424,604 Z" fill="#050407" stroke="{LINE}" stroke-width="3"/>')
    for y in (760, 840, 920, 1000):
        b.append(f'<circle cx="440" cy="{y}" r="9" fill="#c9ccd6" stroke="#5a5e68" stroke-width="2"/>')
    b.append(f'<path d="M300,860 Q370,900 440,860" stroke="#e0b040" stroke-width="3" fill="none"/>')
    b.append(CAB)
    b.append(orejas(328, 494, 344, piel, som, ry=26))
    face = "M330,296 C330,216 492,216 492,296 C494,376 466,440 411,472 C356,440 328,376 330,296 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M492,300 C494,376 466,440 411,472 C452,428 474,376 476,300 Z" fill="{som}" opacity="0.5"/>')
    b.append(f'<path d="M350,330 Q360,380 384,412 M472,330 Q462,380 438,412" stroke="{som}" stroke-width="3" fill="none" opacity="0.5"/>')
    # cejas finas y arqueadas, ojos dorados
    b.append(ceja(372, 302, 50, "sonrisa", -1, "#0a0808", 4))
    b.append(ceja(450, 302, 50, "sonrisa", 1, "#0a0808", 4))
    e = "sonrisa" if estado == "sonrisa" else "neutral"
    b.append(ojo(372, 336, 44, 10, e, -1, iris="#d4a24a", blanco="#f4eee0", piel_sombra=som))
    b.append(ojo(450, 336, 44, 10, e, 1, iris="#d4a24a", blanco="#f4eee0", piel_sombra=som))
    for ex in (372, 450):
        b.append(f'<ellipse cx="{ex}" cy="336" rx="2.6" ry="{6 if e == "sonrisa" else 7.5}" fill="#0a0604"/>')
        b.append(f'<circle cx="{ex}" cy="336" r="6.6" fill="none" stroke="#7a4a10" stroke-width="1.5" opacity="0.8"/>')
    glow_o = 0.9 if estado == "revelado" else 0.35
    b.append(f'<circle cx="372" cy="336" r="22" fill="url(#ojoGlow)" opacity="{glow_o}"/><circle cx="450" cy="336" r="22" fill="url(#ojoGlow)" opacity="{glow_o}"/>')
    b.append(f'<path d="M414,338 Q422,376 414,390" stroke="{som}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M400,394 Q411,400 422,394" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.5"/>')
    # bigote fino y perilla
    b.append(f'<path d="M378,410 C390,402 404,404 411,408 C418,404 432,402 444,410 C434,414 420,414 411,412 C402,414 388,414 378,410 Z" fill="#0a0808"/>')
    if estado in ("sonrisa", "revelado"):
        b.append(f'<path d="M386,424 Q411,446 436,424 Q411,436 386,424 Z" fill="#efe6d6" stroke="{LINE}" stroke-width="2.4"/>')
    else:
        b.append(f'<path d="M392,428 Q411,432 430,428" stroke="{LINE}" stroke-width="2.4" fill="none"/>')
    b.append(f'<path d="M398,446 C400,470 422,470 424,446 C416,452 406,452 398,446 Z" fill="#0a0808"/>')
    # pelo negro engominado
    b.append(f'<path d="M330,300 C326,236 360,214 411,214 C462,214 496,236 492,300 C486,268 462,250 411,250 C360,250 336,268 330,300 Z" fill="#0a0808"/>')
    # sombrero de ala ancha
    b.append(f'<ellipse cx="411" cy="236" rx="200" ry="36" fill="#0a090c" stroke="#2a2830" stroke-width="3"/>')
    b.append(f'<path d="M326,236 L334,128 C360,118 462,118 488,128 L496,236 C460,250 362,250 326,236 Z" fill="#0e0d12" stroke="#2a2830" stroke-width="3"/>')
    b.append(f'<path d="M330,206 C360,216 462,216 492,206 L494,226 C462,236 360,236 328,226 Z" fill="#8a8e98"/>')
    b.append(f'<path d="M216,236 C300,250 520,250 606,236" stroke="#3a3842" stroke-width="2" fill="none"/>')
    b.append('</g>')
    return guardar_sprite(f"caballero_{estado}", "".join(b), defs)


def todos():
    for e in ("neutral", "triste", "sonrisa"):
        rosario(e)
    for e in ("neutral", "risa", "miedo"):
        celestino(e)
    fermin("neutral"); fermin("sonrisa")
    transito()
    ulises("neutral"); ulises("lucido")
    for e in ("neutral", "sonrisa", "revelado"):
        caballero(e)


if __name__ == "__main__":
    todos()
    print("ok")
