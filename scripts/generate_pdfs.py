# -*- coding: utf-8 -*-
"""Generate all printable checklist PDFs for Welcome Home."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

from data import SITE, SPECIES, CATEGORIES, CHECKLISTS

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "downloads")
os.makedirs(OUT_DIR, exist_ok=True)

BRAND = HexColor(SITE["color"])
BRAND_DARK = HexColor(SITE["color_dark"])
INK = HexColor("#2b2521")
MUTED = HexColor("#6b6058")
LINE = HexColor("#e4d8c9")

PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch


def draw_header(c, species_key, cat_key):
    species = SPECIES[species_key]
    category = CATEGORIES[cat_key]

    # Brand bar
    c.setFillColor(BRAND)
    c.rect(0, PAGE_H - 0.55 * inch, PAGE_W, 0.55 * inch, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN, PAGE_H - 0.37 * inch, f"{SITE['name']}")
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.37 * inch, "Free printable pet checklists")

    y = PAGE_H - 0.9 * inch

    # Title
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(MARGIN, y, category["title"])
    y -= 0.24 * inch

    c.setFont("Helvetica", 10.5)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, y, f"For: {species['label']}  —  {category['desc']}")
    y -= 0.3 * inch

    # Personalization line
    c.setFillColor(INK)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y, "Pet's name: ______________________")
    c.drawString(MARGIN + 3.1 * inch, y, "Date home: ______________________")
    y -= 0.18 * inch

    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    y -= 0.28 * inch
    return y


def draw_footer(c, page_num):
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 0.5 * inch, f"{SITE['name']} — {SITE['url']}")
    c.drawRightString(PAGE_W - MARGIN, 0.5 * inch, "Free to print and share. Not medical advice.")


def wrap_text(c, text, font, size, max_width):
    return simpleSplit(text, font, size, max_width)


def draw_checklist(c, y, sections, page_num):
    box = 0.16 * inch
    item_font_size = 10.5
    section_font_size = 11.5
    line_gap = 0.05 * inch
    text_x = MARGIN + box + 0.14 * inch
    max_text_width = PAGE_W - MARGIN - text_x

    for heading, items in sections:
        # Check for page break before section heading
        if y < 1.3 * inch:
            draw_footer(c, page_num)
            c.showPage()
            page_num += 1
            c.setFillColor(INK)
            y = PAGE_H - MARGIN

        c.setFillColor(BRAND_DARK)
        c.setFont("Helvetica-Bold", section_font_size)
        c.drawString(MARGIN, y, heading.upper())
        y -= 0.05 * inch
        c.setStrokeColor(LINE)
        c.setLineWidth(0.75)
        c.line(MARGIN, y, PAGE_W - MARGIN, y)
        y -= 0.22 * inch

        for item in items:
            lines = wrap_text(c, item, "Helvetica", item_font_size, max_text_width)
            needed = (len(lines) * 0.185 * inch) + line_gap
            if y - needed < 0.9 * inch:
                draw_footer(c, page_num)
                c.showPage()
                page_num += 1
                c.setFillColor(INK)
                y = PAGE_H - MARGIN

            # checkbox
            c.setStrokeColor(BRAND_DARK)
            c.setLineWidth(1.1)
            c.rect(MARGIN, y - box + 0.02 * inch, box, box, fill=0, stroke=1)

            c.setFillColor(INK)
            c.setFont("Helvetica", item_font_size)
            ty = y
            for i, line in enumerate(lines):
                c.drawString(text_x, ty - 0.11 * inch, line)
                ty -= 0.185 * inch
            y -= needed + 0.06 * inch

        y -= 0.16 * inch

    draw_footer(c, page_num)
    return page_num


def build_pdf(species_key, cat_key):
    sections = CHECKLISTS[(species_key, cat_key)]
    filename = f"{species_key}-{cat_key}-checklist.pdf"
    path = os.path.join(OUT_DIR, filename)

    c = canvas.Canvas(path, pagesize=letter)
    c.setTitle(f"{CATEGORIES[cat_key]['title']} — {SPECIES[species_key]['label']} — {SITE['name']}")
    c.setAuthor(SITE["name"])

    y = draw_header(c, species_key, cat_key)
    draw_checklist(c, y, sections, page_num=1)
    c.save()
    return filename


def main():
    made = []
    for species_key in SPECIES:
        for cat_key in CATEGORIES:
            fn = build_pdf(species_key, cat_key)
            made.append(fn)
    print(f"Generated {len(made)} PDFs in {OUT_DIR}")
    for fn in made:
        print(" -", fn)


if __name__ == "__main__":
    main()
