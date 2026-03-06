#!/usr/bin/env python3
"""
Build African Safari book with generated images
"""

from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMG_DIR = ROOT / "illustrations" / "qwen_images"


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def build_book():
    pdf_path = OUT_DIR / "African_Safari_Animals_Premium.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
    
    # Cover
    c.setFillColor(HexColor("#2C1810"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#D4AF37"))
    c.roundRect(W*0.05, H*0.75, W*0.9, 80, 40, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 42)
    c.drawString(W*0.08, H*0.78, "African Safari Animals")
    c.setFont("Helvetica", 18)
    c.drawString(W*0.08, H*0.68, "Learn to Write with Real Animals")
    c.setFillColor(HexColor("#D4AF37"))
    c.roundRect(W*0.08, H*0.55, 200, 50, 25, fill=1, stroke=0)
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(W*0.10, H*0.57, "Premium Edition")
    c.showPage()
    
    # LION PAGE
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica-Bold", 26)
    c.drawString(W*0.06, H*0.92, "1. Lion")
    
    img_path = IMG_DIR / "premium_lion_20260305_195510.png"
    if img_path.exists():
        max_w, max_h = W*0.6, H*0.4
        iw, ih = fit_image(img_path, max_w, max_h)
        c.setStrokeColor(HexColor("#D4AF37"))
        c.setLineWidth(4)
        c.roundRect((W-iw)/2 - 5, H*0.50 - 5, iw + 10, ih + 10, 15, fill=0, stroke=1)
        c.drawImage(str(img_path), (W-iw)/2, H*0.50, iw, ih, preserveAspectRatio=True)
    
    c.setStrokeColor(HexColor("#D4AF37"))
    for row in range(5):
        y = H*0.38 - row*0.065
        c.line(W*0.08, y, W*0.92, y)
    
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica-Bold", 44)
    c.drawString(W*0.10, H*0.35, "lion")
    c.setFillColor(HexColor("#CCCCCC"))
    c.setFont("Helvetica", 36)
    c.drawString(W*0.10 + 180, H*0.35, "lion")
    c.drawString(W*0.10 + 340, H*0.35, "lion")
    
    c.setFillColor(HexColor("#8B4513"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W*0.08, H*0.18, "Read and trace:")
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica", 18)
    c.drawString(W*0.08, H*0.13, "The lion is the king of the jungle.")
    c.setFillColor(HexColor("#AAAAAA"))
    c.drawString(W*0.08, H*0.08, "The lion is the king of the jungle.")
    c.showPage()
    
    # ELEPHANT PAGE
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica-Bold", 26)
    c.drawString(W*0.06, H*0.92, "2. Elephant")
    
    img_path = IMG_DIR / "premium_elephant_20260305_195611.png"
    if img_path.exists():
        max_w, max_h = W*0.6, H*0.4
        iw, ih = fit_image(img_path, max_w, max_h)
        c.setStrokeColor(HexColor("#D4AF37"))
        c.setLineWidth(4)
        c.roundRect((W-iw)/2 - 5, H*0.50 - 5, iw + 10, ih + 10, 15, fill=0, stroke=1)
        c.drawImage(str(img_path), (W-iw)/2, H*0.50, iw, ih, preserveAspectRatio=True)
    
    c.setStrokeColor(HexColor("#D4AF37"))
    for row in range(5):
        y = H*0.38 - row*0.065
        c.line(W*0.08, y, W*0.92, y)
    
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica-Bold", 44)
    c.drawString(W*0.10, H*0.35, "elephant")
    c.setFillColor(HexColor("#CCCCCC"))
    c.setFont("Helvetica", 36)
    c.drawString(W*0.10 + 220, H*0.35, "elephant")
    
    c.setFillColor(HexColor("#8B4513"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W*0.08, H*0.18, "Read and trace:")
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica", 18)
    c.drawString(W*0.08, H*0.13, "The elephant has a long trunk.")
    c.setFillColor(HexColor("#AAAAAA"))
    c.drawString(W*0.08, H*0.08, "The elephant has a long trunk.")
    c.showPage()
    
    # Certificate
    c.setFillColor(HexColor("#2C1810"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#D4AF37"))
    c.setLineWidth(5)
    c.roundRect(W*0.08, H*0.15, W*0.84, H*0.70, 30, fill=0, stroke=1)
    c.setFillColor(HexColor("#D4AF37"))
    c.setFont("Helvetica-Bold", 38)
    tw = c.stringWidth("Safari Explorer Certificate", "Helvetica-Bold", 38)
    c.drawString((W-tw)/2, H*0.72, "Safari Explorer Certificate")
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica", 16)
    c.drawString(W*0.20, H*0.60, "This certifies that")
    c.setStrokeColor(HexColor("#D4AF37"))
    c.line(W*0.20, H*0.50, W*0.80, H*0.50)
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#AAAAAA"))
    c.drawString(W*0.42, H*0.46, "(Student Name)")
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica", 16)
    c.drawString(W*0.18, H*0.38, "has completed the African Safari Animals")
    c.drawString(W*0.30, H*0.33, "writing workbook!")
    c.save()
    
    print(f"✅ Book created: {pdf_path}")
    return str(pdf_path)


if __name__ == "__main__":
    build_book()
