#!/usr/bin/env python3
"""NEWS-23 B155 front-page-dense: THE WORLD TODAY, Monday 23 November 2026.
Draws entry.png 1024x1024 with PIL. Run: python3 draw.py [out.png]"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu"

def font(sz, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if (serif and bold) else \
           "DejaVuSerif.ttf" if serif else \
           "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"{FD}/{name}", sz)

def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

INK = (18, 18, 18)
PAPER = (252, 250, 244)
RED = (178, 34, 34)
GREEN = (26, 110, 60)
NAVY = (16, 32, 64)
TEAL = (14, 74, 74)
GREY = (90, 90, 90)
LBLUE = (214, 228, 238)
LTAN = (232, 220, 196)

def chip(d, x, y, text, color):
    f = font(10, bold=True)
    tw = d.textlength(text, font=f)
    w = int(tw) + 10
    d.rounded_rectangle([x, y, x + w, y + 16], radius=3, outline=color, width=1)
    d.text((x + 5, y + 2), text, font=f, fill=color)
    return w

def scene_kospi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 20:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(30, 56)
        by = y + h - bh
        d.rectangle([bx, by, bx + bw, y + h], fill=(30, 52, 96))
        for wy in range(by + 6, y + h - 6, 12):
            for wx in range(bx + 5, bx + bw - 5, 11):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 205, 92))
        bx += bw + 4
    d.text((x + 10, y + 4), "-3.3%", font=font(34, bold=True), fill=(255, 255, 255))
    d.text((x + 10, y + 42), "KOSPI 4,708.54", font=font(12, bold=True), fill=(255, 205, 92))
    pts = [(x + 14, y + 66), (x + 70, y + 74), (x + 130, y + 70),
           (x + 190, y + 84), (x + 250, y + 90), (x + w - 12, y + 100)]
    d.line(pts, fill=(255, 122, 26), width=4)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))

def scene_guterres(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy, r = x + 62, y + 54, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 140, 150),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(255, 255, 255), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(255, 255, 255), width=1)
    d.text((x + 122, y + 14), "REGULATE", font=font(26, bold=True), fill=(255, 205, 92))
    d.text((x + 122, y + 44), "AI NOW", font=font(26, bold=True), fill=(255, 205, 92))
    d.text((x + 122, y + 78), "150 delegates back", font=font(12), fill=(255, 255, 255))
    d.text((x + 122, y + 93), "a risk framework", font=font(12), fill=(255, 255, 255))

def scene_power(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    d.text((x + 10, y + 6), "ASIA POWER INDEX 2026", font=font(13, bold=True), fill=INK)
    bars = [("US", 78.9, (16, 32, 64), (255, 255, 255)),
            ("CHINA", 73.6, (178, 34, 34), (255, 255, 255)),
            ("INDIA", 40.5, (201, 162, 39), (18, 18, 18))]
    by = y + 30
    for name, val, col, tcol in bars:
        bw = int((w - 24) * val / 100.0)
        d.rectangle([x + 10, by, x + 10 + bw, by + 22], fill=col)
        lab = f"{name}  {val}"
        f = font(12, bold=True)
        tw = d.textlength(lab, font=f)
        d.text((x + 10 + bw - tw - 6, by + 4), lab, font=f, fill=tcol)
        by += 26

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16

    # ---- masthead ----
    d.rectangle([0, 0, W, 6], fill=INK)
    d.text((M, 12), "THE WORLD TODAY", font=font(58, bold=True, serif=True), fill=INK)
    df = font(19, bold=True)
    dt = "MONDAY 23 NOVEMBER 2026"
    d.text((W - M - d.textlength(dt, font=df), 34), dt, font=df, fill=INK)
    d.line([M, 78, W - M, 78], fill=INK, width=2)
    kf = font(15, bold=True)
    kick = "AI ROUT ROCKS ASIA  ·  GUTERRES: REGULATE AI NOW  ·  US LEAD OVER CHINA AT RECORD LOW"
    d.text(((W - d.textlength(kick, font=kf)) / 2, 86), kick, font=kf, fill=RED)
    d.line([M, 106, W - M, 106], fill=INK, width=1)

    # ---- number strip: 5 cols x 2 rows, 46px rows ----
    nums = [("-3.3%", "KOSPI FALLS"), ("5.3", "US-CHINA POWER GAP"),
            ("11,762", "EBOLA CASES, DRC"), ("10T WON", "SEOUL RESCUE FUND"),
            ("2%", "BILLIONAIRE TAX BACKED"), ("$450M", "SKUBAL METS DEAL"),
            ("165", "RUSSIAN MISSILES / WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
            ("264 KG", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO")]
    cw = (W - 2 * M) / 5
    nf, lf = font(27, bold=True), font(10.5, bold=True)
    for i, (num, lab) in enumerate(nums):
        col, row = i % 5, i // 5
        cx = M + col * cw
        cy = 112 + row * 46
        d.text((cx + 4, cy), num, font=nf, fill=INK)
        d.text((cx + 4, cy + 31), lab, font=lf, fill=GREY)
        if col < 4:
            d.line([cx + cw - 4, cy + 2, cx + cw - 4, cy + 40], fill=(200, 200, 200), width=1)
    d.line([M, 208, W - M, 208], fill=INK, width=1)

    # ---- region bar ----
    d.rectangle([M, 212, W - M, 234], fill=INK)
    rf = font(14, bold=True)
    reg = "ASIA-PACIFIC 7    ·    AMERICAS 8    ·    MIDDLE EAST 6    ·    EUROPE 5    ·    AFRICA 3    ·    WORLD 2"
    d.text(((W - d.textlength(reg, font=rf)) / 2, 217), reg, font=rf, fill=(255, 255, 255))

    # ---- heroes ----
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi sheds 161 pts, closes 4,708.54; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         "SEOUL · KOSPI", scene_kospi),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "Bridgetown summit: 150 delegates back a risk framework. A blueprint, not a treaty.",
         "BRIDGETOWN · UN", scene_guterres),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6. US diplomatic influence -6 to 76.7; India 3rd.",
         "LOWY INSTITUTE", scene_power),
    ]
    hx = [M, 349, 682]
    hw = 325
    for (head, body, src, scene), x in zip(heroes, hx):
        scene(d, x, 240, hw, 108)
        hf = font(18, bold=True)
        lines = wrap(d, head, hf, hw)
        hy = 354
        for ln in lines[:2]:
            d.text((x, hy), ln, font=hf, fill=INK)
            hy += 21
        bf = font(12)
        blines = wrap(d, body, bf, hw)
        by = hy + 2
        for ln in blines[:2]:
            d.text((x, by), ln, font=bf, fill=(40, 40, 40))
            by += 14
        sf = font(10, bold=True)
        d.text((x, 430), src, font=sf, fill=GREY)
        cw2 = chip(d, x + hw - 100, 428, "REPORTED", GREEN)
    d.line([M, 452, W - M, 452], fill=INK, width=1)

    # ---- cards: 5 cols x 2 rows, h 74 ----
    cards = [
        ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses the chipmaker over China sales.", "WASHINGTON", False),
        ("FBI PROBES NCIC HACK", "Police-database breach under federal investigation.", "WASHINGTON", False),
        ("TRUMP: IRAN STRIKES MAY RESUME", "President says action could return in the New Year.", "WASHINGTON", False),
        ("NASDAQ FUTURES JUMP 3%", "Holiday-week rally lifts US tech stocks.", "NEW YORK", False),
        ("SKUBAL'S $450M METS DEAL", "Two-time Cy Young winner signs a nine-year pact.", "NEW YORK", False),
        ("TOM JACKSON DIES AT 75", "NFL star turned broadcaster is mourned.", "DENVER", False),
        ("STATES SUE SPACEX", "AI safety claims challenged in court.", "US", False),
        ("ANTHROPIC IPO AT $107.3B", "Shares priced $83; debut close $97.17.", "NEW YORK", False),
        ("POLAND: 3 MISSILES CROSSED", "Warsaw says Russian Kh-101s entered its airspace.", "WARSAW", True),
        ("RUSSIA'S NUCLEAR SATELLITE", "Intel warns of an orbital weapon programme.", "WASHINGTON", True),
    ]
    cardw, cardh = 192, 74
    for i, (head, body, src, claim) in enumerate(cards):
        col, row = i % 5, i // 5
        x = M + col * (cardw + 8)
        y = 458 + row * (cardh + 8)
        d.rectangle([x, y, x + cardw, y + cardh], outline=(190, 190, 190), width=1)
        hf = font(13, bold=True)
        lines = wrap(d, head, hf, cardw - 12)
        hy = y + 4
        for ln in lines[:2]:
            d.text((x + 6, hy), ln, font=hf, fill=INK)
            hy += 15
        bf = font(10)
        blines = wrap(d, body, bf, cardw - 12)
        by = hy + 1
        for ln in blines[:2]:
            d.text((x + 6, by), ln, font=bf, fill=(60, 60, 60))
            by += 12
        sf = font(9, bold=True)
        d.text((x + 6, y + cardh - 14), src, font=sf, fill=GREY)
        lab = "CLAIM" if claim else "REPORTED"
        colr = RED if claim else GREEN
        f10 = font(9, bold=True)
        tw = d.textlength(lab, font=f10)
        chipx = x + cardw - int(tw) - 12
        d.rounded_rectangle([chipx, y + cardh - 15, chipx + int(tw) + 8, y + cardh - 2],
                            radius=3, outline=colr, width=1)
        d.text((chipx + 4, y + cardh - 13), lab, font=f10, fill=colr)

    # ---- map + ALSO ----
    d.rectangle([M, 622, 600, 642], fill=INK)
    d.text((M + 8, 626), "WHERE IT HAPPENED", font=font(13, bold=True), fill=(255, 255, 255))
    d.rectangle([616, 622, W - M, 642], fill=INK)
    d.text((624, 626), "ALSO ON MONDAY", font=font(13, bold=True), fill=(255, 255, 255))
    d.rectangle([M, 648, 600, 778], fill=LBLUE)
    d.polygon([(60, 656), (150, 648), (175, 688), (145, 766), (95, 776), (50, 708)],
              fill=LTAN)
    d.polygon([(300, 656), (560, 646), (582, 686), (545, 742), (425, 764),
               (300, 726), (282, 678)], fill=LTAN)
    d.polygon([(330, 730), (400, 724), (410, 772), (350, 776), (322, 752)],
              fill=LTAN)
    pins = [(540, 670, "1"), (150, 750, "2"), (505, 668, "3"), (372, 672, "4"),
            (340, 668, "5"), (425, 666, "6"), (400, 678, "7"), (425, 700, "8"),
            (452, 680, "9"), (472, 704, "10"), (380, 708, "11"), (390, 748, "12"),
            (350, 768, "13")]
    pf = font(10, bold=True)
    for px, py, n in pins:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
        tw = d.textlength(n, font=pf)
        d.text((px - tw / 2, py - 7), n, font=pf, fill=(255, 255, 255))
    lf2 = font(10.5)
    legend = ["1 Seoul · 2 Bridgetown · 3 Beijing · 4 Paris · 5 Manchester",
              "6 Kyiv · 7 Antalya · 8 Gaza · 9 Beirut · 10 Bahrain",
              "11 Benghazi · 12 Khartoum · 13 DRC (Ebola teams trapped)"]
    ly = 784
    for ln in legend:
        d.text((M, ly), ln, font=lf2, fill=INK)
        ly += 14
    # ALSO list, two columns
    also_a = [
        "1. Paris: 100+ nations back 2% billionaire tax",
        "2. Manchester: 12,000 cleared after scare",
        "3. Zelenskyy: 165 Russian missiles in a week",
        "4. COP31: the day after Antalya pact rejected",
        "5. Israel unity talks resume",
        "6. Gaza: two killed in Israeli strike",
        "7. West Bank settler attacks rise",
        "8. Iran war: no deal in sight",
        "9. Lebanon seizes 264 kg explosives",
    ]
    also_b = [
        "10. Bahrain: Iranian strike, 2 hurt",
        "11. Benghazi: UN probe [CLAIM]",
        "12. Sudan: drones downed [CLAIM]",
        "13. DRC: Ebola teams trapped",
        "14. Bangladesh: Hasina jailed if back",
        "15. Seoul minister quits in AI chaos",
        "16. SK Telecom falls 7.3%",
        "17. China margin rules cut to 80%",
        "18. Seoul readies 10T-won fund",
    ]
    af = font(11)
    for colx, items in ((616, also_a), (812, also_b)):
        ay = 648
        for item in items:
            for ln in wrap(d, item, af, 188):
                d.text((colx, ay), ln, font=af, fill=INK)
                ay += 12
            ay += 1
    d.line([M, 842, W - M, 842], fill=INK, width=1)

    # ---- DATE CHECK red box ----
    d.rectangle([M, 850, W - M, 946], outline=RED, width=2, fill=(253, 238, 238))
    d.text((M + 10, 856), "DATE CHECK — LEFT OUT (NOT 23 NOVEMBER)",
           font=font(14, bold=True), fill=RED)
    df2 = font(12)
    lo = wrap(d, "Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)",
              df2, W - 2 * M - 20)
    yy = 878
    for ln in lo:
        d.text((M + 10, yy), ln, font=df2, fill=INK)
        yy += 16
    d.text((M + 10, yy + 2), "NOT YET:", font=font(12, bold=True), fill=RED)
    ny = wrap(d, "Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
              df2, W - 2 * M - 90)
    ny_y = yy + 2
    for ln in ny:
        d.text((M + 86, ny_y), ln, font=df2, fill=INK)
        ny_y += 16

    # ---- footer ----
    d.line([M, 954, W - M, 954], fill=INK, width=1)
    d.text((M, 962), "Sources: AP · Reuters · Bloomberg · Yonhap · Lowy Institute · UN News",
           font=font(11), fill=GREY)
    d.text((M, 978), "THE DAY IN UTC ~ APPROX", font=font(10, bold=True), fill=GREY)
    leg = "■ REPORTED = confirmed by wires      ■ CLAIM = one side's claim"
    d.text((W - M - d.textlength(leg, font=font(11)), 962), leg, font=font(11), fill=GREY)
    d.text((W - M - d.textlength("31 stories · Monday 23 November 2026", font=font(11)), 978),
           "31 stories · Monday 23 November 2026", font=font(11), fill=GREY)

    img.save(out)
    print("saved", out)

if __name__ == "__main__":
    main()
