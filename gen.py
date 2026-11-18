"""Draw entry.png: one day's world news as a 1024x1024 newspaper front page.

Tuesday 17 November 2026. Pillow only; fonts and gulf_coast.json sit beside this file.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

W = H = 1024
M = 40          # outer margin

PAPER = (247, 242, 232)
INK = (24, 21, 18)
MUTED = (96, 88, 78)
RED = (176, 58, 46)
HAIR = (206, 196, 180)
LAND = (170, 160, 143)
COAST = (104, 96, 84)
DM = "DMSerifDisplay-Regular.ttf"
PR = "Prata-Regular.ttf"
PSB = "PT_Serif-Web-Bold.ttf"
PSI = "PT_Serif-Web-Italic.ttf"
PSR = "PT_Serif-Web-Regular.ttf"
BCB = "BarlowCondensed-Bold.ttf"
BCS = "BarlowCondensed-SemiBold.ttf"
BCR = "BarlowCondensed-Regular.ttf"


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(text, font, width, max_lines=0):
    rows = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= width or not cur:
            cur = trial
        else:
            rows.append(cur)
            cur = word
    if cur:
        rows.append(cur)
    if max_lines and len(rows) > max_lines:
        rows = rows[:max_lines]
    return rows


def fit(text, name, width, start, max_lines, low=8):
    size = start
    while size > low:
        rows = wrap(text, F(name, size), width)
        if len(rows) <= max_lines:
            return F(name, size), rows
        size -= 1
    return F(name, low), wrap(text, F(name, low), width)


def caps(d, xy, text, font, fill, track=1.6):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + track
    return x


def caps_width(text, font, track=1.6):
    return sum(font.getlength(c) + track for c in text) - track


def caps_center(d, cx, y, text, font, fill, track=1.6):
    caps(d, (cx - caps_width(text, font, track) / 2, y), text, font, fill, track)


def rule(d, x0, y, x1, w=1, fill=INK):
    d.rectangle([x0, y, x1, y + w - 1], fill=fill)


def block(d, xy, rows, font, lead, fill):
    x, y = xy
    for row in rows:
        d.text((x, y), row, font=font, fill=fill)
        y += lead
    return y


def halftone(mask, cell, color, bg=None):
    w, h = mask.size
    out = bg.copy() if bg is not None else Image.new("RGB", (w, h), PAPER)
    dr = ImageDraw.Draw(out)
    px = mask.load()
    for gy in range(0, h, cell):
        for gx in range(0, w, cell):
            total = 0
            count = 0
            for y in range(gy, min(gy + cell, h), 2):
                for x in range(gx, min(gx + cell, w), 2):
                    total += px[x, y]
                    count += 1
            if not count:
                continue
            cover = total / (count * 255.0)
            if cover < 0.03:
                continue
            r = (cell * 0.28) * (cover ** 0.5)
            cx = gx + cell / 2.0
            cy = gy + cell / 2.0
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    return out
BOX = (43.5, 61.5, 19.5, 31.5)


def project(lon, lat, w, h):
    return ((lon - BOX[0]) / (BOX[1] - BOX[0]) * w, (BOX[3] - lat) / (BOX[3] - BOX[2]) * h)


def clip_ring(pts, w, h):
    edges = [
        (lambda p: p[0] >= 0, lambda a, b: inter_x(a, b, 0)),
        (lambda p: p[0] <= w, lambda a, b: inter_x(a, b, w)),
        (lambda p: p[1] >= 0, lambda a, b: inter_y(a, b, 0)),
        (lambda p: p[1] <= h, lambda a, b: inter_y(a, b, h)),
    ]
    out = pts
    for inside, inter in edges:
        if not out:
            break
        cur = []
        for i in range(len(out)):
            a = out[i]
            b = out[(i + 1) % len(out)]
            ia = inside(a)
            ib = inside(b)
            if ia:
                cur.append(a)
                if not ib:
                    cur.append(inter(a, b))
            elif ib:
                cur.append(inter(a, b))
        out = cur
    return out


def inter_x(a, b, x):
    t = (x - a[0]) / (b[0] - a[0])
    return (x, a[1] + t * (b[1] - a[1]))


def inter_y(a, b, y):
    t = (y - a[1]) / (b[1] - a[1])
    return (a[0] + t * (b[0] - a[0]), y)
def gulf_panel(w, h):
    data = json.load(open(os.path.join(HERE, "gulf_coast.json")))
    WW, WH = 5400, 2700
    world = Image.new("L", (WW, WH), 0)
    wd = ImageDraw.Draw(world)
    for ring in data["rings"]:
        pts = []
        for lon, lat in ring:
            pts.append(((lon + 180.0) / 360.0 * WW, (90.0 - lat) / 180.0 * WH))
        if len(pts) > 2:
            wd.polygon(pts, fill=255)
    x0 = (BOX[0] + 180.0) / 360.0 * WW
    x1 = (BOX[1] + 180.0) / 360.0 * WW
    y0 = (90.0 - BOX[3]) / 180.0 * WH
    y1 = (90.0 - BOX[2]) / 180.0 * WH
    box = (int(x0), int(y0), int(x1), int(y1))
    mask = world.crop(box).resize((w, h), Image.LANCZOS)
    lines = Image.new("L", (WW, WH), 0)
    ld = ImageDraw.Draw(lines)
    for ring in data["rings"]:
        pts = []
        for lon, lat in ring:
            pts.append(((lon + 180.0) / 360.0 * WW, (90.0 - lat) / 180.0 * WH))
        if len(pts) > 2:
            ld.line(pts, fill=255, width=3)
    coast = lines.crop(box).resize((w, h), Image.LANCZOS)

    img = Image.new("RGB", (w, h), PAPER)
    img.paste((236, 229, 215), (0, 0), mask)
    img = halftone(mask, 2, (188, 178, 161), img)
    img.paste(COAST, (0, 0), coast)
    d = ImageDraw.Draw(img)
    manama = project(50.58, 26.22, w, h)
    qeshm = project(55.90, 26.90, w, h)
    hormuz = project(56.45, 26.60, w, h)

    for r in (10, 17):
        d.ellipse([manama[0] - r, manama[1] - r, manama[0] + r, manama[1] + r], outline=RED, width=2)

    def curve(p0, p1, p2, color):
        pts = []
        for i in range(61):
            t = i / 60.0
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            pts.append((x, y))
        for i in range(0, 60, 3):
            d.line([pts[i], pts[i + 2]], fill=color, width=2)
        ax, ay = pts[60]
        bx, by = pts[55]
        ang = math.atan2(ay - by, ax - bx)
        for da in (2.6, -2.6):
            d.line([(ax, ay), (ax + 6 * math.cos(ang + da), ay + 6 * math.sin(ang + da))], fill=color, width=2)

    mid = (manama[0] + qeshm[0]) / 2.0
    curve(manama, (mid, 26), qeshm, RED)
    curve(qeshm, (mid, 142), manama, RED)

    for p in (manama, qeshm):
        d.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], fill=RED)

    def mlabel(x, y, txt, size, track, color):
        f = F(BCS, size)
        tw = caps_width(txt, f, track)
        d.rectangle([x - 3, y - 2, x + tw + 3, y + size + 1], fill=PAPER)
        caps(d, (x, y), txt, f, color, track)

    mlabel(manama[0] + 9, manama[1] - 18, "MANAMA", 11, 1.1, INK)
    mlabel(qeshm[0] - 56, qeshm[1] - 17, "QESHM", 11, 1.1, INK)
    mlabel(hormuz[0] - 19, hormuz[1] + 9, "HORMUZ", 7.5, 1.3, MUTED)

    mlabel(146, 8, "IRAN", 11.5, 2.0, MUTED)
    mlabel(8, 148, "SAUDI ARABIA", 10.5, 1.5, MUTED)
    mlabel(170, 130, "UAE", 10.5, 1.5, MUTED)
    mlabel(238, 162, "OMAN", 10.5, 1.5, MUTED)
    return img
VW, VH = 304, 56


def _pad():
    im = Image.new("RGB", (VW, VH), PAPER)
    return im, ImageDraw.Draw(im)


def bridge():
    im, d = _pad()
    sea = 45
    d.line([(0, sea), (VW, sea)], fill=INK, width=1)
    for x in range(2, VW, 7):
        d.line([(x, sea + 5), (x + 4, sea + 5)], fill=(176, 166, 150), width=1)
    for x in range(6, VW, 13):
        d.line([(x, sea + 9), (x + 5, sea + 9)], fill=(200, 191, 176), width=1)

    for x0 in (2, 194):
        x1 = x0 + 108
        d.line([(x0, 28), (x1, 28)], fill=INK, width=2)
        d.line([(x0, 34), (x1, 34)], fill=INK, width=1)
        for x in range(x0 + 4, x1 - 6, 14):
            d.line([(x, 28), (x, 34)], fill=INK, width=1)
            d.line([(x, 28), (x + 10, 34)], fill=(120, 112, 100), width=1)
            d.line([(x + 10, 28), (x, 34)], fill=(120, 112, 100), width=1)
    for x in (56, 242):
        d.rectangle([x, 34, x + 4, sea], fill=INK)
    d.line([(104, 28), (110, 24)], fill=INK, width=1)
    d.line([(194, 28), (188, 24)], fill=INK, width=1)

    d.line([(110, 28), (138, 43)], fill=INK, width=3)
    d.line([(192, 28), (166, 42)], fill=INK, width=3)
    d.line([(136, 41), (164, 40)], fill=INK, width=2)
    d.line([(126, 37), (136, 43)], fill=INK, width=1)
    for x in (146, 154):
        d.line([(x, 38), (x + 4, 40)], fill=INK, width=1)

    d.line([(110, 28), (104, 30), (110, 32), (104, 34)], fill=INK, width=1)
    d.line([(192, 28), (198, 30), (192, 32), (198, 34)], fill=INK, width=1)
    for ax in (120, 168):
        d.line([(ax, 35), (ax, 41)], fill=RED, width=1)
        d.line([(ax, 41), (ax - 3, 38)], fill=RED, width=1)
        d.line([(ax, 41), (ax + 3, 38)], fill=RED, width=1)
    return im


def summit():
    im, d = _pad()
    d.line([(16, 42), (288, 42)], fill=INK, width=2)
    d.rectangle([16, 42, 288, 47], outline=INK)
    d.line([(34, 47), (34, 56)], fill=INK, width=2)
    d.line([(270, 47), (270, 56)], fill=INK, width=2)

    for px, kind in ((44, "ph"), (92, "us"), (212, "au"), (260, "jp")):
        d.line([(px, 11), (px, 42)], fill=INK, width=1)
        if kind == "ph":
            d.rectangle([px, 13, px + 18, 18], fill=(176, 58, 46))
            d.rectangle([px, 18, px + 18, 23], fill=INK)
            d.polygon([(px, 13), (px + 7, 18), (px, 23)], fill=PAPER, outline=INK)
        elif kind == "us":
            for yy in (15, 19, 23):
                d.line([(px, yy), (px + 18, yy)], fill=(176, 58, 46))
            d.rectangle([px, 13, px + 6, 18], fill=INK)
        elif kind == "au":
            d.rectangle([px, 13, px + 18, 23], outline=INK)
            d.rectangle([px, 13, px + 8, 18], fill=INK)
            for cx, cy in ((12, 20), (15, 21), (11, 22)):
                d.ellipse([px + cx - 1, cy - 1, px + cx + 1, cy + 1], fill=PAPER)
        else:
            d.ellipse([px + 2, 14, px + 16, 23], fill=(176, 58, 46))

    d.polygon([(134, 30), (146, 26), (158, 30), (155, 36), (146, 38), (137, 36)], outline=INK)
    d.line([(140, 30), (146, 38)], fill=INK)

    for x0 in (104, 196):
        d.rectangle([x0, 33, x0 + 44, 41], outline=INK)
        d.line([(x0 + 4, 36), (x0 + 32, 36)], fill=(150, 140, 125), width=1)
    d.polygon([(148, 30), (154, 24), (160, 30), (160, 38), (154, 34), (148, 38)], outline=(176, 58, 46))
    return im


def chips():
    im, d = _pad()
    d.rectangle([26, 10, 120, 46], outline=INK, width=2)
    d.rectangle([36, 18, 110, 40], outline=(120, 112, 100), width=1)
    for x in range(34, 122, 8):
        d.line([(x, 10), (x, 5)], fill=INK)
        d.line([(x, 46), (x, 51)], fill=INK)
    for y in range(16, 46, 8):
        d.line([(26, y), (21, y)], fill=INK)
        d.line([(120, y), (125, y)], fill=INK)
    d.text((52, 17), "AI", font=F(BCB, 17), fill=INK)

    for x in range(130, 182, 9):
        d.line([(x, 28), (x + 5, 28)], fill=INK)
    d.polygon([(182, 28), (176, 24), (176, 32)], fill=INK)

    for x in (186, 192, 198):
        d.line([(x, 4), (x, 52)], fill=RED, width=2)
    d.line([(186, 14), (198, 14)], fill=RED, width=2)
    d.line([(186, 34), (198, 34)], fill=RED, width=2)

    for i in range(5):
        cx = 214
        cy = 8 + i * 9
        d.rectangle([cx, cy, cx + 7, cy + 7], outline=INK)
    return im


VIGS = [bridge, summit, chips]

M = 40
W = H = 1024

MAST = "THE WORLD TODAY"
DATE = "TUESDAY  \u00b7  17 NOVEMBER 2026"

LEAD_KICK = "MIDDLE EAST  \u00b7  IRAN WAR"
LEAD_HEAD = "Iran strikes a US radar in Bahrain, and America answers at Qeshm"
LEAD_DECK = ("Tehran calls it payback for the strike at Sirik. Bahrain says it "
             "intercepted the drones; five ships burn off Hormuz after mines, "
             "and a tanker crew is missing.")
LEAD_BY = "WORLD DESK  \u00b7  MANAMA, QESHM AND THE GULF"

COLS = [
    ("EUROPE  \u00b7  UKRAINE WAR",
     "A span of the Kerch bridge falls into the sea",
     "Second day of strikes, the seventh stage of the campaign. Moscow calls an emergency meeting."),
    ("ASIA  \u00b7  DIPLOMACY",
     "Trump lands in Manila with a minerals pact",
     "Quad leaders sign critical-minerals deals before he flies on to see Xi and Putin in China."),
    ("AMERICAS  \u00b7  TECHNOLOGY",
     "Washington narrows China's remote access to AI chips",
     "Export licences now cover five countries, Singapore and Malaysia among them, from 19 November. Nvidia warns its buyers of legal risk, hours before its results."),
]

BRIEFS = [
    ("AFRICA", "EU keeps 87 African airlines on its blacklist"),
    ("ASIA", "Trump says he may meet Kim Jong Un while in China"),
    ("EUROPE", "France counts 146,000 marchers; unions claim 500,000"),
    ("EUROPE", "Sweden's speaker sets a Christmas deadline for a government"),
    ("OCEANIA", "Starlux adds its first Australia route, to Sydney"),
    ("SCIENCE", "COP31 backs a global plan on extreme heat and cooling"),
    ("SPORT", "Dhoni retires from the IPL at 45"),
    ("MARKETS", "Brent closes at $92.93, WTI at $85.56"),
    ("HEALTH", "UN urges limits on hormone-disrupting chemicals"),
    ("CLIMATE", "Rockstr\u00f6m warns COP31 that tipping points are near"),
]

STATS = [
    ("146,000", "MARCHERS IN FRANCE"),
    ("5", "SHIPS ON FIRE OFF HORMUZ"),
    ("$92.93", "A BARREL OF BRENT"),
    ("1m+", "GAZANS IN FLOOD-PRONE AREAS"),
]


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    caps(d, (M, 20), "THE DAY IN ONE IMAGE", F(BCS, 9), MUTED, 2.0)
    right = "WORLD EDITION"
    caps(d, (W - M - caps_width(right, F(BCS, 9), 2.0), 20), right, F(BCS, 9), MUTED, 2.0)
    rule(d, M, 36, W - M, 1)

    mast = fit(MAST, DM, W - 2 * M, 92, 1)[0]
    mw = mast.getlength(MAST)
    d.text(((W - mw) / 2, 40), MAST, font=mast, fill=INK)
    rule(d, M, 150, W - M, 3)
    rule(d, M, 156, W - M, 1)

    df = F(BCS, 27)
    dw = caps_width(DATE, df, 1.9)
    caps(d, ((W - dw) / 2, 165), DATE, df, INK, 1.9)
    rule(d, M, 200, W - M, 1)

    sf = F(BCS, 12.5)
    st = "6 CONTINENTS  \u00b7  ONE DAY"
    sw = caps_width(st, sf, 2.4)
    caps(d, ((W - sw) / 2, 209), st, sf, MUTED, 2.4)
    rule(d, M, 234, W - M, 1)

    kf = F(BCB, 17)
    caps(d, (M, 244), LEAD_KICK, kf, RED, 1.8)

    hf, hrows = fit(LEAD_HEAD, DM, 612, 45, 3)
    y = 268
    for row in hrows:
        d.text((M, y), row, font=hf, fill=INK)
        y += 51

    dfk = F(PSR, 16.2)
    y = block(d, (M, y + 2), wrap(LEAD_DECK, dfk, 604), dfk, 20.6, (60, 55, 48))
    caps(d, (M, y + 2), LEAD_BY, F(BCB, 11), RED, 1.4)

    rule(d, 676, 206, W - M, 1)
    caps(d, (676, 212), "THE DAY, MAPPED", F(BCS, 9.4), RED, 1.8)
    img.paste(gulf_panel(308, 190), (676, 232))
    d.rectangle([676, 232, 983, 421], outline=INK)
    cf = F(PSI, 10.4)
    d.text((676, 430), "Strikes exchanged across the Gulf,", font=cf, fill=MUTED)
    d.text((676, 444), "from Manama to Qeshm.", font=cf, fill=MUTED)

    rule(d, M, 490, W - M, 1)

    xs = [40, 360, 680]
    d.line([(350, 500), (350, 690)], fill=HAIR)
    d.line([(670, 500), (670, 690)], fill=HAIR)
    for i, (label, head, dek) in enumerate(COLS):
        x = xs[i]
        img.paste(VIGS[i](), (x, 500))
        caps(d, (x, 562), label, F(BCB, 12.2), RED, 1.5)
        hf2, rows2 = fit(head, BCB, 300, 22.5, 3)
        for j, row in enumerate(rows2):
            d.text((x, 578 + j * 25), row, font=hf2, fill=INK)
        dkf = F(PSR, 12.6)
        dy = 578 + len(rows2) * 25 + 3
        block(d, (x, dy), wrap(dek, dkf, 300), dkf, 15.6, (70, 64, 56))

    rule(d, M, 700, W - M, 1)

    caps(d, (M, 706), "THE REST OF THE DAY", F(BCB, 13), RED, 2.0)
    ibr = "IN BRIEF"
    caps(d, (W - M - caps_width(ibr, F(BCS, 9.6), 2.0), 709), ibr, F(BCS, 9.6), MUTED, 2.0)
    rule(d, M, 722, W - M, 1)
    d.line([(512, 730), (512, 846)], fill=HAIR)

    for i, (lab, txt) in enumerate(BRIEFS):
        col = i // 5
        row = i % 5
        x = M + col * 480
        y = 730 + row * 26
        d.text((x, y), lab, font=F(BCS, 10.6), fill=RED)
        d.text((x + 86, y - 1), txt, font=F(PSR, 12.6), fill=(38, 34, 30))

    rule(d, M, 856, W - M, 1)
    caps(d, (M, 862), "THE DAY IN NUMBERS", F(BCS, 9), MUTED, 2.2)

    for i, (num, lab) in enumerate(STATS):
        x = M + i * 236
        d.text((x, 870), num, font=F(DM, 31), fill=INK)
        caps(d, (x, 906), lab, F(BCS, 9.8), MUTED, 1.4)
        if i:
            d.line([(x - 18, 874), (x - 18, 908)], fill=HAIR)

    d.rectangle([0, 946, W, 988], fill=INK)
    d.rectangle([0, 946, W, 949], fill=RED)
    strap = "6 CONTINENTS  \u00b7  ONE DAY  \u00b7  TUESDAY 17 NOVEMBER 2026"
    sft = F(DM, 20)
    sw2 = sft.getlength(strap)
    d.text(((W - sw2) / 2, 955), strap, font=sft, fill=PAPER)

    caps_center(d, W / 2, 995, "AN ENTRY FOR MAKE.FUN", F(BCS, 9.8), MUTED, 2.2)

    img.save(path, optimize=True)
    return img


if __name__ == "__main__":
    render(os.path.join(HERE, "entry.png"))
    print("wrote entry.png")
