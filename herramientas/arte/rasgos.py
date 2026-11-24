"""Rasgos faciales reutilizables (ojos, cejas, boca, orejas) para los sprites."""
from lib import *

SW, SH = 820, 1080
LINE = "#16100f"


def sdoc(body, defs=""):
    return doc(body, defs, w=SW, h=SH)


def ojo(cx, cy, w, h, estado="neutral", lado=-1, iris="#2a1c18", blanco="#ece8ef", linea=LINE, pest=4.0,
        viejo=False, humedo=False, piel_sombra="#c9a594"):
    """Un ojo almendrado. lado=-1 (izquierda del espectador) o 1."""
    x0, x1 = cx - w / 2, cx + w / 2
    # extremo interno (hacia la nariz) un poco más bajo
    yi = cy + h * 0.10
    ye = cy - h * 0.05
    xin, xout = (x1, x0) if lado < 0 else (x0, x1)
    yin, yout = yi, ye
    up = h * (1.0 if estado == "neutral" else 0.62 if estado == "triste" else 0.75)
    lo = h * (0.45 if estado != "sonrisa" else -0.05)
    iris_dy = 0 if estado != "triste" else h * 0.18
    gid = f"eye{int(cx)}{int(cy)}{estado}"
    upper = f"M{xout:.1f},{yout:.1f} Q{cx:.1f},{cy - up*1.25:.1f} {xin:.1f},{yin:.1f}"
    lower = f"Q{cx:.1f},{cy + lo*1.3:.1f} {xout:.1f},{yout:.1f}"
    o = [f'<clipPath id="{gid}"><path d="{upper} {lower} Z"/></clipPath>']
    o.append(f'<path d="{upper} {lower} Z" fill="{blanco}"/>')
    ir = h * 0.62
    o.append(f'<g clip-path="url(#{gid})">'
             f'<circle cx="{cx + lado*0.0:.1f}" cy="{cy + iris_dy:.1f}" r="{ir:.1f}" fill="{iris}"/>'
             f'<circle cx="{cx:.1f}" cy="{cy + iris_dy:.1f}" r="{ir*0.45:.1f}" fill="#0a0606"/>'
             f'<circle cx="{cx + ir*0.35:.1f}" cy="{cy + iris_dy - ir*0.4:.1f}" r="{ir*0.26:.1f}" fill="#ffffff" opacity="0.9"/>'
             f'<path d="{upper} L{xin:.1f},{yin - h:.1f} L{xout:.1f},{yout - h:.1f} Z" fill="{piel_sombra}" opacity="0.25" transform="translate(0,{h*0.25:.1f})"/>'
             f'</g>')
    if humedo:
        o.append(f'<path d="M{cx - w*0.3:.1f},{cy + lo*0.9:.1f} Q{cx:.1f},{cy + lo*1.5:.1f} {cx + w*0.3:.1f},{cy + lo*0.9:.1f}" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.8"/>')
    # línea superior (pestañas)
    o.append(f'<path d="{upper}" stroke="{linea}" stroke-width="{pest}" fill="none" stroke-linecap="round"/>')
    if pest >= 4:
        # pestañas exteriores
        o.append(f'<path d="M{xout:.1f},{yout:.1f} l{lado*-1*-7:.1f},{-5:.1f}" stroke="{linea}" stroke-width="{pest*0.7:.1f}" stroke-linecap="round"/>')
    # pliegue del párpado
    o.append(f'<path d="M{xout + (w*0.1 if lado<0 else -w*0.1):.1f},{yout - h*0.5:.1f} Q{cx:.1f},{cy - up*1.25 - h*0.55:.1f} {xin + (-w*0.15 if lado<0 else w*0.15):.1f},{yin - h*0.55:.1f}" stroke="{linea}" stroke-width="1.6" fill="none" opacity="0.45"/>')
    if estado == "sonrisa":
        o.append(f'<path d="M{xout:.1f},{yout + h*0.2:.1f} Q{cx:.1f},{cy + h*0.25:.1f} {xin:.1f},{yin + h*0.15:.1f}" stroke="{linea}" stroke-width="1.6" fill="none" opacity="0.5"/>')
    else:
        o.append(f'<path d="{"M%.1f,%.1f " % (xin, yin)}{lower}" stroke="{linea}" stroke-width="1.4" fill="none" opacity="0.45"/>')
    if viejo:
        o.append(f'<path d="M{cx - w*0.4:.1f},{cy + h*1.15:.1f} Q{cx:.1f},{cy + h*1.7:.1f} {cx + w*0.4:.1f},{cy + h*1.15:.1f}" stroke="{linea}" stroke-width="1.5" fill="none" opacity="0.4"/>')
        for k in range(3):
            o.append(f'<path d="M{xout + lado*-1*-4:.1f},{yout - 4 + k*6:.1f} l{lado*-1*-14:.1f},{-4 + k*4:.1f}" stroke="{linea}" stroke-width="1.3" opacity="0.35"/>')
    return "".join(o)


def ceja(cx, cy, w, estado, lado, color, grosor=5.0):
    xin = cx + (w / 2 if lado < 0 else -w / 2)
    xout = cx - (w / 2 if lado < 0 else -w / 2)
    if estado == "triste":
        yin, yout, ctrl = cy - 7, cy + 2, cy - 6
    elif estado == "sonrisa":
        yin, yout, ctrl = cy + 1, cy + 3, cy - 8
    elif estado == "ceño":
        yin, yout, ctrl = cy + 6, cy - 3, cy - 4
    else:
        yin, yout, ctrl = cy + 2, cy + 3, cy - 7
    return (f'<path d="M{xin:.1f},{yin:.1f} Q{cx:.1f},{ctrl:.1f} {xout:.1f},{yout:.1f}" stroke="{color}" stroke-width="{grosor}" '
            f'fill="none" stroke-linecap="round"/>')


def boca(cx, cy, w, estado, labio="#a9545c", linea=LINE, labios=True):
    o = []
    if estado == "sonrisa":
        o.append(f'<path d="M{cx-w/2:.1f},{cy-2:.1f} Q{cx:.1f},{cy+11:.1f} {cx+w/2:.1f},{cy-2:.1f}" stroke="{linea}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
        if labios:
            o.append(f'<path d="M{cx-w*0.35:.1f},{cy+5:.1f} Q{cx:.1f},{cy+15:.1f} {cx+w*0.35:.1f},{cy+5:.1f} Q{cx:.1f},{cy+9:.1f} {cx-w*0.35:.1f},{cy+5:.1f} Z" fill="{labio}" opacity="0.85"/>')
    elif estado == "triste":
        o.append(f'<path d="M{cx-w/2:.1f},{cy+4:.1f} Q{cx:.1f},{cy-3:.1f} {cx+w/2:.1f},{cy+4:.1f}" stroke="{linea}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
        if labios:
            o.append(f'<path d="M{cx-w*0.35:.1f},{cy+4:.1f} Q{cx:.1f},{cy+14:.1f} {cx+w*0.35:.1f},{cy+4:.1f} Q{cx:.1f},{cy+2:.1f} {cx-w*0.35:.1f},{cy+4:.1f} Z" fill="{labio}" opacity="0.8"/>')
    else:
        if labios:
            o.append(f'<path d="M{cx-w/2:.1f},{cy:.1f} Q{cx-w*0.25:.1f},{cy-7:.1f} {cx:.1f},{cy-4:.1f} Q{cx+w*0.25:.1f},{cy-7:.1f} {cx+w/2:.1f},{cy:.1f} Q{cx:.1f},{cy+2:.1f} {cx-w/2:.1f},{cy:.1f} Z" fill="{labio}" opacity="0.9"/>')
            o.append(f'<path d="M{cx-w*0.42:.1f},{cy+1:.1f} Q{cx:.1f},{cy+15:.1f} {cx+w*0.42:.1f},{cy+1:.1f} Q{cx:.1f},{cy+4:.1f} {cx-w*0.42:.1f},{cy+1:.1f} Z" fill="{labio}"/>')
            o.append(f'<path d="M{cx-w*0.15:.1f},{cy+7:.1f} Q{cx:.1f},{cy+9:.1f} {cx+w*0.15:.1f},{cy+7:.1f}" stroke="#ffffff" stroke-width="2" opacity="0.35" fill="none"/>')
        o.append(f'<path d="M{cx-w/2:.1f},{cy:.1f} Q{cx:.1f},{cy+3:.1f} {cx+w/2:.1f},{cy:.1f}" stroke="{linea}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    return "".join(o)


def tejido_pattern(pid, base, linea, paso=9):
    return (f'<pattern id="{pid}" width="{paso}" height="14" patternUnits="userSpaceOnUse">'
            f'<rect width="{paso}" height="14" fill="{base}"/>'
            f'<path d="M0,0 L{paso/2},6 L{paso},0 M0,7 L{paso/2},13 L{paso},7" stroke="{linea}" stroke-width="1.6" fill="none" opacity="0.55"/>'
            f'</pattern>')


def orejas(xl, xr, y, piel, sombra, ry=30):
    return (f'<ellipse cx="{xl}" cy="{y}" rx="16" ry="{ry}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>'
            f'<path d="M{xl+2},{y-14} Q{xl-8},{y} {xl+2},{y+14}" stroke="{sombra}" stroke-width="3" fill="none"/>'
            f'<ellipse cx="{xr}" cy="{y}" rx="16" ry="{ry}" fill="{sombra}" stroke="{LINE}" stroke-width="3"/>'
            f'<path d="M{xr-2},{y-14} Q{xr+8},{y} {xr-2},{y+14}" stroke="#5a4038" stroke-width="3" fill="none"/>')
