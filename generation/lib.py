# -*- coding: utf-8 -*-
"""Petit moteur de mise en page PDF (ReportLab) partagé par tous les documents."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, KeepTogether, ListFlowable,
                                ListItem)
from reportlab.pdfgen import canvas as rl_canvas
from ref import DISCLAIMER

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DVC", FD + "DejaVuSansCondensed.ttf"))
pdfmetrics.registerFont(TTFont("DVCB", FD + "DejaVuSansCondensed-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "corpus")
FIG = os.path.join(ROOT, "gen", "fig")
os.makedirs(FIG, exist_ok=True)

INK = colors.HexColor("#1d2733")
ACC = {"NORDAL Énergie": colors.HexColor("#0b5d4b"), "VOLTARIS": colors.HexColor("#22408c"),
       "Exploitation": colors.HexColor("#5a5a5a")}

S = {
 "body": ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=5),
 "small": ParagraphStyle("small", fontName="DV", fontSize=8, leading=10.5, textColor=INK),
 "cell": ParagraphStyle("cell", fontName="DVC", fontSize=8, leading=10, textColor=INK),
 "cellb": ParagraphStyle("cellb", fontName="DVCB", fontSize=8, leading=10, textColor=colors.white),
 "h1": ParagraphStyle("h1", fontName="DVB", fontSize=15, leading=19, spaceBefore=4, spaceAfter=8, textColor=INK),
 "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=5, textColor=INK),
 "h3": ParagraphStyle("h3", fontName="DVB", fontSize=10, leading=13, spaceBefore=5, spaceAfter=3, textColor=INK),
 "cap": ParagraphStyle("cap", fontName="DVI", fontSize=8.5, leading=11, alignment=TA_CENTER, spaceAfter=8, textColor=INK),
 "title": ParagraphStyle("title", fontName="DVB", fontSize=24, leading=30, textColor=INK, spaceAfter=10),
 "sub": ParagraphStyle("sub", fontName="DV", fontSize=13, leading=18, textColor=INK, spaceAfter=6),
}


class Doc(BaseDocTemplate):
    """Document avec en-tête/pied de page et relevé des pages des figures et tableaux."""
    def __init__(self, path, maker, title, ref, version, **kw):
        super().__init__(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                         topMargin=24*mm, bottomMargin=20*mm, title=title, author=maker, **kw)
        self.maker, self.doctitle, self.ref, self.version = maker, title, ref, version
        self.anchors = []
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=self._decorate)])

    def _decorate(self, c, doc):
        w, h = A4
        acc = ACC.get(self.maker, INK)
        c.saveState()
        c.setFillColor(acc); c.rect(0, h - 14*mm, w, 14*mm, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("DVB", 9.5)
        c.drawString(20*mm, h - 9*mm, self.maker.upper())
        c.setFont("DV", 8.5)
        c.drawRightString(w - 20*mm, h - 9*mm, f"{self.doctitle}  ·  Réf. {self.ref}  ·  {self.version}")
        c.setStrokeColor(colors.HexColor("#c8cdd3")); c.line(20*mm, 14*mm, w - 20*mm, 14*mm)
        c.setFillColor(colors.HexColor("#6b7480")); c.setFont("DV", 7)
        c.drawString(20*mm, 9.5*mm, DISCLAIMER)
        c.restoreState()

    def afterFlowable(self, f):
        a = getattr(f, "_anchor", None)
        if a:
            self.anchors.append((a, self.page))


class NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        n = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            self.setFont("DV", 8); self.setFillColor(colors.HexColor("#4a525c"))
            self.drawRightString(A4[0] - 20*mm, 9.5*mm, f"Page {self._pageNumber} / {n}")
            super().showPage()
        super().save()


# ---------------------------------------------------------------- briques
def P(t, st="body"): return Paragraph(t, S[st])
def H1(t): return Paragraph(t, S["h1"])
def H2(t): return Paragraph(t, S["h2"])
def H3(t): return Paragraph(t, S["h3"])
def SP(h=4): return Spacer(1, h*mm)
def PB(): return PageBreak()

def bullets(items, numbered=False):
    lst = [ListItem(Paragraph(i, S["body"]), leftIndent=12) for i in items]
    return ListFlowable(lst, bulletType="1" if numbered else "bullet", start=1 if numbered else None,
                        bulletFontName="DV", bulletFontSize=9, leftIndent=14)

def table(rows, widths, anchor=None, caption=None, header_color=None, zebra=True, font=8):
    st = ParagraphStyle("c", parent=S["cell"], fontSize=font, leading=font + 2)
    sh = ParagraphStyle("h", parent=S["cellb"], fontSize=font, leading=font + 2)
    data = [[Paragraph(str(x), sh) for x in rows[0]]] + \
           [[Paragraph(str(x), st) for x in r] for r in rows[1:]]
    W = 170*mm
    t = Table(data, colWidths=[w * W for w in widths], repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), header_color or INK),
             ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa3ad")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#eef1f4")))
    t.setStyle(TableStyle(style))
    out = []
    if caption:
        cp = Paragraph(caption, S["cap"])
        if anchor: cp._anchor = anchor
        out.append(cp)
    out.append(t); out.append(SP(3))
    return out

def figure(img, width_mm, caption, anchor):
    from PIL import Image as PI
    w, h = PI.open(img).size
    im = Image(img, width=width_mm*mm, height=width_mm*mm*h/w)
    cp = Paragraph(caption, S["cap"]); cp._anchor = anchor
    return [KeepTogether([im, SP(1), cp])]

def note(text, kind="ATTENTION"):
    col = {"DANGER": "#b3261e", "ATTENTION": "#c26a00", "NOTE": "#22408c"}[kind]
    t = Table([[Paragraph(f"<b>{kind}</b>", ParagraphStyle("n", parent=S["cellb"], fontSize=8.5)),
                Paragraph(text, S["body"])]], colWidths=[26*mm, 144*mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), colors.HexColor(col)),
                           ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(col)),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
    return [t, SP(3)]

def cover(maker, title, subtitle, ref, version, equip, extra=None):
    out = [SP(30), P(maker, "sub"), P(title, "title"), P(subtitle, "sub"), SP(8)]
    rows = [["Champ", "Valeur"], ["Référence document", ref], ["Version", version],
            ["Équipement(s)", equip]] + (extra or [])
    out += table(rows, [0.35, 0.65], header_color=ACC.get(maker, INK))
    return out

def build(relpath, maker, title, ref, version, story):
    path = os.path.join(CORPUS, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d = Doc(path, maker, title, ref, version)
    d.build(story, canvasmaker=NumberedCanvas)
    import fitz
    n = fitz.open(path).page_count
    return dict(path=path, pages=n, anchors=d.anchors)
