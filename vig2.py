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

    d.line([(110, 20), (110, 35)], fill=RED, width=2)
    d.line([(192, 20), (192, 35)], fill=RED, width=2)
    d.line([(128, 44), (136, 44)], fill=RED, width=1)
    d.line([(150, 44), (158, 44)], fill=RED, width=1)
    d.line([(168, 44), (176, 44)], fill=RED, width=1)
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
