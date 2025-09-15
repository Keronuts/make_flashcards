import csv
import os
import sys
import argparse
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from pathlib import Path


# ---- GUI bits ----
import tkinter as tk
from tkinter import filedialog, messagebox

# Landscape page size
PAGE_W, PAGE_H = landscape(letter)
COLS, ROWS = 3, 3   # 9 per page (3 columns x 3 rows)
COL_W = PAGE_W / COLS
ROW_H = PAGE_H / ROWS

styles = getSampleStyleSheet()
QStyle = ParagraphStyle("QStyle", parent=styles["Heading5"], fontSize=10, leading=12, alignment=1, spaceBefore=4, spaceAfter=4)
AStyle = ParagraphStyle("AStyle", parent=styles["BodyText"], fontSize=9, leading=11, alignment=1, spaceBefore=4, spaceAfter=4)

def ensure_pdf(path: str) -> str:
    return path if path and path.lower().endswith(".pdf") else (path + ".pdf" if path else path)

def read_cards_from_csv(csv_path):
    cards = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        import csv as _csv
        reader = _csv.DictReader(f)
        if not {"question","answer"}.issubset({h.strip().lower() for h in reader.fieldnames or []}):
            raise ValueError("CSV must have headers: question,answer")
        for row in reader:
            q = (row.get("question") or "").strip()
            a = (row.get("answer") or "").strip()
            if q and a:
                cards.append((q, a))
    if not cards:
        raise ValueError("No cards found in CSV.")
    return cards

def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def draw_cutlines(canvas: Canvas, doc):
    """Draws cut lines aligned with landscape orientation grid (9 cards/page)."""
    canvas.saveState()
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor(colors.black)
    # Vertical cuts
    for c in range(1, COLS):
        x = c * COL_W
        canvas.line(x, 0, x, PAGE_H)
    # Horizontal cuts
    for r in range(1, ROWS):
        y = r * ROW_H
        canvas.line(0, y, PAGE_W, y)
    # Outer border
    canvas.rect(0, 0, PAGE_W, PAGE_H)
    canvas.restoreState()

def build_pdf(cards, path, side="Q"):
    doc = BaseDocTemplate(path, pagesize=(PAGE_W, PAGE_H), leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0)
    frame = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    template = PageTemplate(id="GridPage", frames=[frame], onPage=draw_cutlines)
    doc.addPageTemplates([template])

    story = []
    for page_cards in chunk(cards, 9):
        rows = [[], [], []]
        for idx_on_page, (q, a) in enumerate(page_cards):
            abs_index = cards.index((q, a)) + 1
            text = f"Q{abs_index}: {q}" if side == "Q" else f"A{abs_index}: {a}"
            para = Paragraph(text, QStyle if side == "Q" else AStyle)
            row = idx_on_page // 3
            rows[row].append(para)
        for row in rows:
            while len(row) < 3:
                row.append(Paragraph("", QStyle))
        tbl = Table(rows, colWidths=[COL_W]*3, rowHeights=[ROW_H]*3)
        tbl.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(tbl)
        story.append(PageBreak())
    if story and isinstance(story[-1], PageBreak):
        story.pop()  # remove trailing page break
    doc.build(story)

def main():
    root = tk.Tk()
    root.withdraw()

    try:
        # 1) Pick CSV (initial dir can be anywhere—first run we don’t know the CSV folder yet)
        csv_path = filedialog.askopenfilename(
            title="Select cards CSV (question,answer)",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not csv_path:
            return

        # Use the CSV's folder for all subsequent dialogs
        csv_dir = str(Path(csv_path).parent)
        stem = Path(csv_path).stem  # e.g., 'AZ900_cards'

        # 2) Save FRONT (Questions) in the same folder as the CSV by default
        fronts_path = filedialog.asksaveasfilename(
            title="Save FRONT (Questions) PDF",
            initialdir=csv_dir,
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"{stem}_Fronts.pdf",
        )
        if not fronts_path:
            return

        # 3) Save BACK (Answers) in the same folder as the CSV by default
        backs_path = filedialog.asksaveasfilename(
            title="Save BACK (Answers) PDF",
            initialdir=csv_dir,
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"{stem}_Backs.pdf",
        )
        if not backs_path:
            return

        # Build PDFs
        cards = read_cards_from_csv(csv_path)
        build_pdf(cards, ensure_pdf(fronts_path), side="Q")
        build_pdf(cards, ensure_pdf(backs_path),  side="A")

        messagebox.showinfo(
            "Done",
            f"Created:\n{fronts_path}\n{backs_path}\n\nPrint landscape, duplex, flip on long edge."
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()
