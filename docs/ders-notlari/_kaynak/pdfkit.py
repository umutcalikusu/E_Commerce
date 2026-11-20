"""Ders notu PDF'leri için ortak yardımcı.

Her adımın içeriği ayrı bir dosyada (adim_XX.py) bir liste olarak tanımlanır,
bu modül onu PDF'e çevirir. Türkçe karakterler için Windows fontları kullanılır.
"""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

FONTS = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Sans", FONTS + "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONTS + "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", FONTS + "segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", FONTS + "segoeuiz.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FONTS + "consola.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", FONTS + "consolab.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                              italic="Sans-Italic", boldItalic="Sans-BoldItalic")
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold",
                              italic="Mono", boldItalic="Mono-Bold")

INK = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#5b6670")
ACCENT = colors.HexColor("#1d4ed8")
RULE = colors.HexColor("#d5dbe1")
CODE_BG = colors.HexColor("#f4f6f8")
NOTE_BG = colors.HexColor("#eef4ff")
WARN_BG = colors.HexColor("#fff6e5")
WARN_EDGE = colors.HexColor("#d97706")
TIP_BG = colors.HexColor("#ecfdf3")
TIP_EDGE = colors.HexColor("#15803d")

S = {
    "title": ParagraphStyle("title", fontName="Sans-Bold", fontSize=24, leading=30,
                            textColor=INK, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle", fontName="Sans", fontSize=12, leading=17,
                               textColor=MUTED, spaceAfter=14),
    "h1": ParagraphStyle("h1", fontName="Sans-Bold", fontSize=17, leading=22,
                         textColor=ACCENT, spaceBefore=16, spaceAfter=6, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=13, leading=17,
                         textColor=INK, spaceBefore=11, spaceAfter=4, keepWithNext=1),
    "p": ParagraphStyle("p", fontName="Sans", fontSize=10.5, leading=15.5,
                        textColor=INK, spaceAfter=6, alignment=TA_LEFT),
    "bullet": ParagraphStyle("bullet", fontName="Sans", fontSize=10.5, leading=15,
                             textColor=INK, leftIndent=14, bulletIndent=3, spaceAfter=2.5),
    "cell": ParagraphStyle("cell", fontName="Sans", fontSize=9.5, leading=13, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="Sans-Bold", fontSize=9.5, leading=13,
                            textColor=colors.white),
    "box": ParagraphStyle("box", fontName="Sans", fontSize=10, leading=14.5, textColor=INK),
    "boxh": ParagraphStyle("boxh", fontName="Sans-Bold", fontSize=10.5, leading=14.5,
                           textColor=INK, spaceAfter=2),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=8.8, leading=12, textColor=INK),
    "term": ParagraphStyle("term", fontName="Sans-Bold", fontSize=10, leading=14, textColor=INK),
    "flow": ParagraphStyle("flow", fontName="Sans-Bold", fontSize=9.5, leading=12.5,
                           textColor=INK, alignment=1),
    "flowsub": ParagraphStyle("flowsub", fontName="Sans", fontSize=8.3, leading=11,
                              textColor=MUTED, alignment=1),
}

WIDTH = A4[0] - 40 * mm


def _box(paras, bg, edge):
    t = Table([[paras]], colWidths=[WIDTH])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [Spacer(1, 3), t, Spacer(1, 7)]


def _render(block):
    kind, *a = block
    if kind == "h1":
        return [Paragraph(a[0], S["h1"])]
    if kind == "h2":
        return [Paragraph(a[0], S["h2"])]
    if kind == "p":
        return [Paragraph(a[0], S["p"])]
    if kind == "bullets":
        return [Paragraph(x, S["bullet"], bulletText="•") for x in a[0]] + [Spacer(1, 4)]
    if kind == "steps":
        return [Paragraph(x, S["bullet"], bulletText=f"{i}.") for i, x in enumerate(a[0], 1)] + [Spacer(1, 4)]
    if kind == "code":
        t = Table([[Preformatted(a[0].strip("\n"), S["code"])]], colWidths=[WIDTH])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
            ("BOX", (0, 0), (-1, -1), 0.5, RULE),
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        return [Spacer(1, 2), t, Spacer(1, 8)]
    if kind in ("note", "warn", "tip"):
        bg, edge = {"note": (NOTE_BG, ACCENT), "warn": (WARN_BG, WARN_EDGE),
                    "tip": (TIP_BG, TIP_EDGE)}[kind]
        return _box([Paragraph(a[0], S["boxh"]), Paragraph(a[1], S["box"])], bg, edge)
    if kind == "table":
        rows, widths = a[0], a[1]
        data = [[Paragraph(c, S["cellh"]) for c in rows[0]]]
        data += [[Paragraph(c, S["cell"]) for c in r] for r in rows[1:]]
        t = Table(data, colWidths=[w * WIDTH for w in widths], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CODE_BG]),
            ("GRID", (0, 0), (-1, -1), 0.4, RULE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return [Spacer(1, 2), t, Spacer(1, 9)]
    if kind == "terms":
        data = [[Paragraph(k, S["term"]), Paragraph(v, S["cell"])] for k, v in a[0]]
        t = Table(data, colWidths=[0.24 * WIDTH, 0.76 * WIDTH])
        t.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return [t, Spacer(1, 8)]
    if kind == "flow":
        # a[0]: [(başlık, alt yazı), ...] soldan sağa akış diyagramı
        nodes = a[0]
        n = len(nodes)
        arrow_w = 0.05 * WIDTH
        box_w = (WIDTH - arrow_w * (n - 1)) / n
        row, widths = [], []
        for i, (title, sub) in enumerate(nodes):
            row.append([Paragraph(title, S["flow"]), Paragraph(sub, S["flowsub"])])
            widths.append(box_w)
            if i < n - 1:
                row.append(Paragraph("→", S["flow"]))
                widths.append(arrow_w)
        t = Table([row], colWidths=widths)
        style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                 ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                 ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
        for i in range(0, 2 * n - 1, 2):
            style += [("BACKGROUND", (i, 0), (i, 0), NOTE_BG), ("BOX", (i, 0), (i, 0), 0.8, ACCENT)]
        t.setStyle(TableStyle(style))
        return [Spacer(1, 4), t, Spacer(1, 10)]
    if kind == "pagebreak":
        return [PageBreak()]
    if kind == "keep":
        inner = []
        for b in a[0]:
            inner += _render(b)
        return [KeepTogether(inner)]
    raise ValueError(kind)


def build(path, title, subtitle, blocks, footer):
    def on_page(c, doc):
        c.saveState()
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
        c.setFont("Sans", 8.5)
        c.setFillColor(MUTED)
        c.drawString(20 * mm, 10 * mm, footer)
        c.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Sayfa {doc.page}")
        c.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=22 * mm,
                            title=title, author="E-Commerce ders notları")
    story = [Paragraph(title, S["title"]), Paragraph(subtitle, S["subtitle"])]
    for b in blocks:
        story += _render(b)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
