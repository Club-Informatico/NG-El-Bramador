"""Sonido original de EL BRAMADOR.

El bramido se sintetiza a partir del análisis de una grabación real del cerro:
fundamental entre ~68 y ~88 Hz con armónicos que caen ~16/28/36/41 dB,
fluctuación lenta de tono y de amplitud, y un ataque de 2-3 s (la avalancha).
"""
import sys
import numpy as np
from base import *   # SR, t_, mtof, lp, hp, bp, reverb, estereo, normalizar, fundir, plegar, guardar,
                     # cajita, piano, pad, guitarra, golpe, mezclar, rng

ARM_DB = [0, -24, -29, -35, -40, -44, -50, -55]


def ruido_lento(n, fc, seed):
    r = np.random.default_rng(seed)
    x = lp(r.normal(0, 1, n), fc, 2)
    return x / (np.max(np.abs(x)) + 1e-9)


def voz_bramido(dur, f_ini, f_fin, seed=0, jitter=0.010, am=0.35, curva=None, brillo=1.0):
    """Una 'voz' del cerro: tono grave con armónicos, deriva de tono y temblor de amplitud."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    if curva is None:
        fr = f_ini + (f_fin - f_ini) * (t / dur) ** 2
    else:
        fr = np.interp(t / dur, np.linspace(0, 1, len(curva)), curva)
    fr = fr * (1 + 0.02 * ruido_lento(n, 0.4, seed) + jitter * ruido_lento(n, 9, seed + 1))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    x = np.zeros(n)
    for k, db in enumerate(ARM_DB, 1):
        a = 10 ** (db / 20) * (brillo ** (k - 1))
        x += a * np.sin(k * ph + 0.3 * k)
    trem = 1 + am * ruido_lento(n, 5, seed + 2)
    return x * trem


def bramido_base(dur, f_ini, f_fin, seed, ataque=2.5, caida=2.5, voces=2, arena_nivel=0.012, brillo=1.0, curva=None):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for v in range(voces):
        det = 1 + (v - (voces - 1) / 2) * 0.012
        cv = None if curva is None else [c * det for c in curva]
        x += voz_bramido(dur, f_ini * det, f_fin * det, seed + 10 * v, curva=cv, brillo=brillo) / voces
    # retumbo de la arena (banda 40-400 Hz) y siseo de granos
    r = np.random.default_rng(seed + 99)
    retumbo = bp(r.normal(0, 1, n), 30, 120, 2)
    retumbo /= np.max(np.abs(retumbo)) + 1e-9
    siseo = bp(r.normal(0, 1, n), 1500, 4000, 2) * (0.5 + 0.5 * ruido_lento(n, 3, seed + 5))
    siseo /= np.max(np.abs(siseo)) + 1e-9
    x = lp(x + 0.3 * retumbo, 650, 4) + arena_nivel * siseo
    env = np.minimum(1, t / ataque) ** 1.6 * np.minimum(1, (dur - t) / caida) ** 1.3
    return x * env


def guardar_par(nombre, x, pico):
    """Versión completa (~6 dB más baja que antes) y versión suave.

    La suave quita la fundamental (~70 Hz) con un pasa-altos: el oído sigue
    reconociendo la misma nota por sus armónicos (fundamental ausente), pero
    con mucha menos energía grave.
    """
    x = hp(x, 45, 2)
    guardar(nombre, normalizar(x, pico))
    suave = hp(hp(x, 125, 4), 125, 4)
    suave = lp(suave, 3000, 2)
    guardar(nombre + "_suave", normalizar(suave, pico * 0.6))


def bramido():
    x = bramido_base(15.0, 69, 74, seed=1, curva=[68, 70, 71, 70, 72, 73, 74, 80, 86, 88], voces=2)
    x = estereo(x, 0.35)
    x = reverb(x, 1.4, 0.18, 2500, seed=21)
    guardar_par("bramido", x, 0.46)


def bramido_lejano():
    x = bramido_base(17.0, 71, 76, seed=2, ataque=4.0, caida=4.5, voces=2, arena_nivel=0.01,
                     curva=[70, 71, 72, 73, 73, 74, 76, 78])
    x = lp(x, 260, 3)
    x = estereo(x, 0.6)
    x = reverb(x, 3.5, 0.45, 900, seed=22)
    guardar_par("bramido_lejano", x, 0.3)


def bramido_furioso():
    a = bramido_base(13.0, 66, 70, seed=3, ataque=1.2, caida=3.0, voces=3, arena_nivel=0.1,
                     curva=[64, 68, 72, 70, 74, 80, 86, 90, 88], brillo=1.25)
    b = bramido_base(13.0, 73, 77, seed=4, ataque=1.8, caida=3.0, voces=2, arena_nivel=0.05,
                     curva=[73, 75, 74, 78, 84, 92, 96, 94], brillo=1.1)
    n = len(a)
    t = np.arange(n) / SR
    x = a + 0.7 * b
    x = np.tanh(x * 1.5) / 1.2
    x = estereo(x, 0.5)
    x = reverb(x, 2.2, 0.3, 2000, seed=23)
    guardar_par("bramido_furioso", x, 0.5)


def bramido_entrada():
    """Treinta segundos de bramido para la entrada al cerro, con la forma de la
    grabación real: arranque lento, una nota sostenida cerca de 70 Hz que tiembla,
    y hacia el final el cerro sube a ~86-88 Hz antes de apagarse."""
    dur = 31.0
    curva = [66, 68, 70, 69, 71, 70, 72, 71, 70, 72, 71, 70, 73, 72, 71, 72, 74, 80, 85, 87, 88, 87, 86]
    x = bramido_base(dur, 68, 86, seed=31, ataque=3.5, caida=2.5, voces=2, arena_nivel=0.012, curva=curva)
    # leve retumbo extra al cambiar de nota (como una segunda lengua de arena)
    n = len(x)
    t = np.arange(n) / SR
    x *= 1 + 0.25 * np.exp(-((t - 24.5) ** 2) / 4)
    x = estereo(x, 0.45)
    x = reverb(x, 2.0, 0.25, 2200, seed=32)
    guardar_par("bramido_entrada", x, 0.46)


def formante(x, f1, f2, f3=2500):
    return (bp(x, f1 * 0.85, f1 * 1.15, 2) * 1.0 + bp(x, f2 * 0.88, f2 * 1.12, 2) * 0.6 +
            bp(x, f3 * 0.9, f3 * 1.1, 2) * 0.25)


def bramido_coro():
    """Adentro del cerro: el bramido convertido en coro de almas (vocales oscuras)."""
    L = 40.0
    n = int((L + 6) * SR)
    x = np.zeros(n)
    r0 = np.random.default_rng(56)
    aire = bp(r0.normal(0, 1, n), 250, 1200)
    x += 0.05 * aire / (np.max(np.abs(aire)) + 1e-9)
    # voces: diente de sierra en armónicos del Re, con formantes de «u» y «o»
    notas = [73.4 * 2, 73.4 * 3, 110 * 2, 87.3 * 2, 73.4 * 4, 116.5 * 2]
    vocales = [(320, 800), (400, 750), (350, 640), (450, 850)]
    r = np.random.default_rng(55)
    for k in range(14):
        ini = r.uniform(0, L)
        dur = r.uniform(5, 10)
        f0 = notas[k % len(notas)] * (1 + r.uniform(-0.006, 0.006))
        tt = t_(dur)
        vib = 1 + 0.006 * np.sin(2 * np.pi * r.uniform(4.5, 5.5) * tt)
        ph = 2 * np.pi * np.cumsum(f0 * vib) / SR
        saw = np.zeros_like(tt)
        for h in range(1, 25):
            saw += np.sin(h * ph) / h
        f1, f2 = vocales[k % len(vocales)]
        v = formante(saw, f1, f2) * np.sin(np.pi * tt / dur) ** 2
        mezclar(x, v * 0.22, ini)
    x = estereo(x, 0.8)
    x = reverb(x, 4.5, 0.55, 3000, seed=24)
    x = hp(plegar(x, L), 120)
    guardar("bramido_coro", normalizar(x, 0.5))


# ---------------------------------------------------------------------------
#  Música
# ---------------------------------------------------------------------------

def drone_cerro(dur, nivel=0.25, seed=7):
    x = bramido_base(dur, 73.4, 73.4, seed=seed, ataque=4, caida=4, voces=2, arena_nivel=0.0,
                     curva=[73.4, 73.0, 73.8, 73.4])
    return lp(x, 400) * nivel


# Motivo del cerro (Re menor, compás de 6/8). (nota MIDI, corcheas)
MOTIVO = [(62, 3), (65, 1), (64, 1), (62, 1), (60, 2), (62, 1), (57, 3),
          (58, 2), (60, 1), (62, 2), (65, 1), (64, 3), (62, 3),
          (69, 3), (67, 1), (65, 1), (64, 1), (65, 2), (64, 1), (62, 3),
          (61, 2), (64, 1), (62, 6)]
ACORDES_TEMA = [[50, 57, 62, 65], [46, 58, 62, 65], [48, 55, 60, 64], [45, 57, 61, 64],
                [50, 57, 62, 65], [43, 58, 62, 67], [45, 57, 61, 64], [50, 57, 62, 65]]


def arpegio(x, ac, t0, corchea, vel=0.3):
    orden = [0, 2, 1, 3, 2, 1]
    for i, k in enumerate(orden):
        mezclar(x, guitarra(ac[k], 1.6, vel * (1.2 if i == 0 else 0.8)), t0 + i * corchea)


def tema_bramador():
    corchea = 60 / 150
    compas = 6 * corchea
    L = len(ACORDES_TEMA) * compas * 2
    x = np.zeros(int((L + 6) * SR))
    for vuelta in range(2):
        t0 = vuelta * len(ACORDES_TEMA) * compas
        for i, ac in enumerate(ACORDES_TEMA):
            arpegio(x, ac, t0 + i * compas, corchea, 0.32)
        t = t0
        for (m, d) in MOTIVO:
            mm = m + (12 if vuelta else 0)
            mezclar(x, guitarra(mm, d * corchea + 1.0, 0.55), t)
            t += d * corchea
    x = hp(x, 60)
    x = estereo(x, 0.5)
    x = reverb(x, 2.6, 0.35, 5000, seed=31)
    x = plegar(x, L)
    guardar("tema_bramador", normalizar(x, 0.6))


def chingana():
    """Una cueca original de chingana: rasgueo en 6/8, tormento y palmas."""
    corchea = 60 / 330
    compas = 6 * corchea
    prog = [[50, 57, 62, 66, 69], [50, 57, 62, 66, 69], [45, 57, 61, 64, 69], [45, 57, 61, 64, 67],
            [45, 57, 61, 64, 67], [45, 57, 61, 64, 67], [50, 57, 62, 66, 69], [50, 57, 62, 66, 69],
            [43, 55, 59, 62, 67], [43, 55, 59, 62, 67], [50, 57, 62, 66, 69], [45, 57, 61, 64, 67],
            [50, 57, 62, 66, 69], [45, 57, 61, 64, 67], [50, 57, 62, 66, 69], [50, 57, 62, 66, 69]]
    L = len(prog) * compas * 2
    x = np.zeros(int((L + 3) * SR))
    r = np.random.default_rng(9)
    acentos = [1.0, 0.45, 0.6, 0.9, 0.45, 0.6]
    for vuelta in range(2):
        for i, ac in enumerate(prog):
            t0 = (vuelta * len(prog) + i) * compas
            for j in range(6):
                a = acentos[j]
                arriba = j % 2 == 1
                notas = ac if not arriba else ac[::-1]
                for kk, nn in enumerate(notas):
                    mezclar(x, guitarra(nn, 0.5 if a < 0.8 else 0.9, 0.16 * a), t0 + j * corchea + kk * 0.008)
                # tormento / pandero
                if j in (0, 3):
                    mezclar(x, golpe(180, 0.12, 0.6, f1=150) * 0.35, t0 + j * corchea)
                s = hp(r.normal(0, 1, int(0.04 * SR)), 4000) * np.exp(-t_(0.04) / 0.01)
                mezclar(x, s * 0.12 * a, t0 + j * corchea)
            # palmas en 3 y 6
            for j in (2, 5):
                p = bp(r.normal(0, 1, int(0.05 * SR)), 900, 3000) * np.exp(-t_(0.05) / 0.012)
                mezclar(x, p * 0.25, t0 + j * corchea + r.uniform(-0.01, 0.01))
        # melodía simple de requinto en la segunda vuelta
        if vuelta == 1:
            mel = [74, 76, 78, 76, 74, 73, 71, 73, 74, 69, 71, 73, 74, 76, 74, 73]
            for i, nn in enumerate(mel):
                mezclar(x, guitarra(nn, 1.0, 0.35), (len(prog) + i) * compas + corchea * (i % 2))
    x = hp(x, 60)
    x = estereo(x, 0.5)
    x = reverb(x, 1.2, 0.2, 5000, seed=32)
    x = plegar(x, L)
    guardar("chingana", normalizar(x, 0.6))


def caballero():
    """Vals lento y desafinado del forastero, con el cerro debajo."""
    negra = 60 / 72
    L = 16 * 3 * negra
    x = np.zeros(int((L + 6) * SR))
    mel = [(74, 2), (73, 1), (74, 2), (80, 1), (77, 3), (None, 3),
           (76, 2), (75, 1), (76, 2), (82, 1), (79, 3), (None, 3),
           (74, 1), (77, 1), (80, 1), (83, 2), (82, 1), (79, 2), (76, 1), (73, 3),
           (74, 3), (68, 3), (62, 6)]
    t = 0.0
    for (m_, d) in mel:
        if m_:
            mezclar(x, cajita(m_ - 12, 3.0, 0.5) * 1.0, t)
            mezclar(x, cajita(m_ - 12 + 0.3, 3.0, 0.2) if False else cajita(m_ - 12, 3.0, 0.0), t)
        t += d * negra
    bajos = [50, 56, 50, 56, 49, 55, 50, 56, 50, 56, 49, 55, 50, 44, 50, 50]
    for i, b_ in enumerate(bajos):
        tb = i * 3 * negra
        mezclar(x, piano(b_, 3.5, 0.4), tb)
        mezclar(x, piano(b_ + 7, 1.5, 0.12), tb + negra)
        mezclar(x, piano(b_ + 6, 1.5, 0.12), tb + 2 * negra)
    # desafinar levemente (sensación de caja de música vieja)
    tt = np.arange(len(x)) / SR
    x = x * (1 + 0.04 * np.sin(2 * np.pi * 0.3 * tt))
    x = hp(x, 60)
    x = estereo(x, 0.6)
    x = reverb(x, 3.8, 0.45, 3500, seed=33)
    x = plegar(x, L)
    guardar("caballero", normalizar(x, 0.6))


def tension_cerro():
    """Tensión sin graves: cuerdas apagadas en registro medio, viento y campanitas."""
    L = 48.0
    n = int((L + 6) * SR)
    x = np.zeros(n)
    tt = np.arange(n) / SR
    r = np.random.default_rng(12)
    # acorde disonante sostenido (Re-Mib-La) en registro medio, respirando
    for m_, fase in ((62, 0.0), (63, 2.1), (69, 4.0), (74, 1.3)):
        env = (0.5 + 0.5 * np.sin(2 * np.pi * tt / 14 + fase)) ** 2
        x += pad([m_], L + 6, 0.5, ataque=4, brillo=1500)[:n] * env
    viento = lp(r.normal(0, 1, n), 900) * (0.4 + 0.6 * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 12)) ** 2)
    x = x + 0.12 * viento / (np.max(np.abs(viento)) + 1e-9)
    for k in range(7):
        mezclar(x, cajita(int(r.choice([86, 87, 92, 93])), 4, 0.1), 3 + k * 6.5 + r.uniform(-1, 1))
    x = hp(x, 90)
    x = estereo(x, 0.7)
    x = reverb(x, 4.0, 0.45, 3000, seed=34)
    x = plegar(x, L)
    guardar("tension_cerro", normalizar(x, 0.5))


def final_oscuro():
    corchea = 60 / 110
    compas = 6 * corchea
    acs = [[50, 57, 62, 65], [46, 58, 62, 65], [43, 55, 58, 62], [45, 57, 61, 64]] * 3
    L = len(acs) * compas
    x = np.zeros(int((L + 6) * SR))
    for i, ac in enumerate(acs):
        arpegio(x, ac, i * compas, corchea, 0.22)
        if i % 2 == 0:
            mezclar(x, piano(ac[-1] + 12, 4, 0.18), i * compas + corchea * 3)
    x = hp(x, 60)
    x = estereo(x, 0.5)
    x = reverb(x, 3.5, 0.45, 3000, seed=35)
    x = plegar(x, L)
    guardar("final_oscuro", normalizar(x, 0.55))


def final_luz():
    corchea = 60 / 140
    compas = 6 * corchea
    acs = [[50, 57, 62, 66], [47, 59, 62, 66], [43, 55, 59, 62], [45, 57, 61, 64],
           [50, 57, 62, 66], [43, 55, 59, 62], [45, 57, 61, 64], [50, 57, 62, 66]]
    L = len(acs) * compas * 2
    x = np.zeros(int((L + 6) * SR))
    mel = [(66, 3), (69, 1), (67, 1), (66, 1), (64, 2), (66, 1), (62, 3), (64, 2), (66, 1), (67, 2), (71, 1),
           (69, 3), (66, 3), (74, 3), (73, 1), (71, 1), (69, 1), (71, 2), (69, 1), (66, 3), (64, 2), (66, 1), (62, 6)]
    for vuelta in range(2):
        t0 = vuelta * len(acs) * compas
        for i, ac in enumerate(acs):
            arpegio(x, ac, t0 + i * compas, corchea, 0.26)
        if vuelta == 1:
            t = t0
            for (m_, d) in mel:
                mezclar(x, guitarra(m_ + 12, d * corchea + 1.2, 0.45), t)
                t += d * corchea
        mezclar(x, pad([50, 57, 62, 66], len(acs) * compas + 2, 0.35, ataque=3, brillo=1200), t0)
    x = hp(x, 40)
    x = estereo(x, 0.5)
    x = reverb(x, 2.8, 0.35, 6000, seed=36)
    x = plegar(x, L)
    guardar("final_luz", normalizar(x, 0.6))


# ---------------------------------------------------------------------------
#  Efectos
# ---------------------------------------------------------------------------

def viento_desierto():
    L = 40.0
    n = int((L + 3) * SR)
    t = np.arange(n) / SR
    r = np.random.default_rng(41)
    nn = r.normal(0, 1, n)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * t / 10.0) * np.sin(2 * np.pi * t / 20.0 + 1)
    x = lp(nn, 450) * (0.25 + 0.75 * lfo) + 0.35 * bp(nn, 500, 1300) * lfo ** 2
    # silbido entre las piedras
    f = 620 + 90 * np.sin(2 * np.pi * t / 7)
    x += 0.04 * np.sin(2 * np.pi * np.cumsum(f) / SR) * lfo ** 3
    x = estereo(x, 0.8)
    x = plegar(x, L)
    guardar("viento_desierto", normalizar(x, 0.5))


def fogata():
    L = 20.0
    n = int((L + 1) * SR)
    r = np.random.default_rng(42)
    base = lp(r.normal(0, 1, n), 600) * 0.5 + bp(r.normal(0, 1, n), 1500, 5000) * 0.08
    x = base
    for _ in range(int(L * 9)):
        ti = r.uniform(0, L)
        d = r.uniform(0.002, 0.012)
        s = hp(r.normal(0, 1, int(d * SR) + 8), r.uniform(1500, 4000)) * np.exp(-t_(d + 8 / SR) / (d / 3))
        mezclar(x, s * r.uniform(0.15, 0.5), ti)
    for _ in range(int(L / 2.5)):
        ti = r.uniform(0, L)
        s = hp(r.normal(0, 1, int(0.03 * SR)), 800) * np.exp(-t_(0.03) / 0.006)
        mezclar(x, s * 0.7, ti)
    x = estereo(x, 0.4)
    x = plegar(x, L)
    guardar("fogata", normalizar(x, 0.45))


def arena():
    dur = 5.0
    n = int(dur * SR)
    r = np.random.default_rng(43)
    t = np.arange(n) / SR
    granos = np.zeros(n)
    idx = r.integers(0, n, 30000)
    granos[idx] = r.uniform(-1, 1, len(idx))
    x = bp(granos, 1200, 7000) * 0.8 + lp(r.normal(0, 1, n), 300) * 0.4
    env = np.sin(np.pi * np.minimum(t / dur, 1)) ** 0.7
    x = estereo(x * env, 0.6)
    guardar("arena", normalizar(fundir(x, 0.05, 0.4), 0.5))


def cascos():
    dur = 7.0
    x = np.zeros(int(dur * SR))
    r = np.random.default_rng(44)
    t = 0.3
    paso = 0
    while t < dur - 0.6:
        f = 900 if paso % 2 else 700
        s = golpe(f, 0.12, 0.8, f1=f * 0.7) * 0.6
        s[: int(0.02 * SR)] += hp(r.normal(0, 1, int(0.02 * SR)), 2000) * 0.3 * np.exp(-t_(0.02) / 0.004)
        mezclar(x, s * (0.5 + 0.5 * min(1, t / 3)), t)
        t += 0.42 if paso % 2 else 0.18
        paso += 1
    x = reverb(x, 1.8, 0.35, 4000, seed=45)
    guardar("cascos", normalizar(fundir(x, 0.05, 0.5), 0.55))


def piedra():
    dur = 4.5
    n = int(dur * SR)
    t = np.arange(n) / SR
    r = np.random.default_rng(46)
    ruido = lp(r.normal(0, 1, n), 400)
    fr = np.abs(np.sin(2 * np.pi * 9 * t)) ** 4
    x = ruido * (0.5 + 0.5 * fr) + 0.4 * np.sin(2 * np.pi * 42 * t) * np.exp(-((t - dur + 0.6) ** 2) / 0.02)
    env = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.4)
    x = reverb(x * env, 2.5, 0.4, 1500, seed=47)
    guardar("piedra", normalizar(fundir(x, 0.02, 0.3), 0.8))


def oro():
    x = np.zeros(int(2.5 * SR))
    r = np.random.default_rng(48)
    for k in range(9):
        f0 = r.uniform(2400, 4200)
        d = 0.5
        tt = t_(d)
        s = (np.sin(2 * np.pi * f0 * tt) + 0.6 * np.sin(2 * np.pi * f0 * 2.76 * tt) + 0.3 * np.sin(2 * np.pi * f0 * 5.4 * tt)) * np.exp(-tt / 0.08)
        mezclar(x, s * r.uniform(0.3, 0.8), 0.05 + k * 0.11 + r.uniform(0, 0.05))
    x = reverb(x, 1.5, 0.3, 8000, seed=49)
    guardar("oro", normalizar(fundir(x, 0, 0.3), 0.5))


def golpes():
    x = np.zeros(int(2.8 * SR))
    for k in range(3):
        mezclar(x, golpe(170, 0.25, 0.5, f1=120), 0.1 + k * 0.55)
        mezclar(x, 0.4 * golpe(420, 0.08, 0.6), 0.1 + k * 0.55)
    x = reverb(x, 1.6, 0.35, 2500, seed=50)
    guardar("golpes", normalizar(fundir(x, 0, 0.4), 0.8))


def campana():
    dur = 9.0
    x = np.zeros(int(dur * SR))
    f = 293.0
    parciales = [(0.5, 1.0, 4.0), (1.0, 0.8, 3.0), (1.19, 0.5, 2.2), (1.5, 0.35, 1.8), (2.0, 0.45, 1.5), (2.52, 0.2, 1.0), (3.0, 0.15, 0.8)]
    for tg in (0.0, 3.2):
        tt = t_(dur - tg)
        s = sum(a * np.sin(2 * np.pi * f * p * tt) * np.exp(-tt / d) for (p, a, d) in parciales)
        s *= np.minimum(1, tt / 0.003)
        mezclar(x, s, tg)
    x = estereo(x, 0.5)
    x = reverb(x, 3.0, 0.4, 4000, seed=51)
    guardar("campana", normalizar(fundir(x, 0, 0.5), 0.45))


TODO = ["bramido", "bramido_lejano", "bramido_furioso", "bramido_entrada", "bramido_coro", "tema_bramador", "chingana",
        "caballero", "tension_cerro", "final_oscuro", "final_luz", "viento_desierto", "fogata", "arena",
        "cascos", "piedra", "oro", "golpes", "campana"]

if __name__ == "__main__":
    for nombre in sys.argv[1:] or TODO:
        globals()[nombre]()
