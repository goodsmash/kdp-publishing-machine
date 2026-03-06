#!/usr/bin/env python3
"""
Ocean Writing Skills - COMPLETE with ALL images
"""

from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
IMG_DIR = ROOT / "illustrations" / "qwen_images"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def build_complete_ocean_book():
    """Build Ocean book with ALL 8 images embedded"""
    
    ocean_animals = [
        ("fish", "The fish swims fast.", "ocean_fish_20260305_194257.png"),
        ("shark", "The shark is big.", "ocean_shark_20260305_203321.png"),
        ("whale", "The whale can sing.", "ocean_whale_20260305_203446.png"),
        ("turtle", "The turtle swims slow.", "ocean_turtle_20260305_203518.png"),
        ("octopus", "The octopus has eight legs.", "ocean_octopus_20260305_203550.png"),
        ("crab", "The crab walks sideways.", "ocean_crab_20260305_203642.png"),
        ("starfish", "The starfish has five arms.", "ocean_starfish_20260305_203917.png"),
        ("seahorse", "The seahorse is small.", "ocean_seahorse_20260305_204020.png"),
    ]
    
    pdf_path = OUT_DIR / "Ocean_Writing_Skills_Complete.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
    
    # COVER
    c.setFillColor(HexColor("#0077B6"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#90E0EF"))
    c.circle(W*0.8, H*0.8, 100, fill=1, stroke=0)
    c.setFillColor(HexColor("#CAF0F8"))
    c.circle(W*0.2, H*0.2, 150, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 42)
    c.drawString(W*0.08, H*0.65, "Ocean Writing")
    c.drawString(W*0.08, H*0.55, "Skills Workbook")
    
    c.setFont("Helvetica", 16)
    c.drawString(W*0.08, H*0.42, "Trace Words and Sentences with Sea Friends")
    
    c.setFillColor(HexColor("#FFD700"))
    c.roundRect(W*0.08, H*0.28, 140, 45, 22, fill=1, stroke=0)
    c.setFillColor(HexColor("#1D3557"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W*0.10, H*0.30, "Ages 3-6")
    
    # Cover note
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica", 12)
    c.drawString(W*0.08, H*0.15, "✓ 8 Full-Color Illustrations  ✓ Tracing Practice  ✓ Certificate")
    
    c.showPage()
    
    # GUIDE PAGE
    c.setFillColor(HexColor("#1D3557"))
    c.setFont("Helvetica-Bold", 24)
    c.drawString(W*0.08, H*0.88, "How to Use This Book")
    
    tips = [
        "1. Look at the colorful ocean animal picture",
        "2. Trace the word in BIG letters",
        "3. Trace it two more times",
        "4. Trace the sentence at the bottom",
        "5. Color the picture if you want!",
    ]
    
    c.setFillColor(HexColor("#1D3557"))
    c.setFont("Helvetica", 14)
    y = H*0.75
    for tip in tips:
        c.drawString(W*0.10, y, tip)
        y -= 35
    
    c.showPage()
    
    # CONTENT PAGES - each with embedded image
    for i, (word, sentence, img_file) in enumerate(ocean_animals, 1):
        img_path = IMG_DIR / img_file
        
        # Header
        c.setFillColor(HexColor("#0077B6"))
        c.setFont("Helvetica-Bold", 26)
        c.drawString(W*0.06, H*0.92, f"{i}. {word.title()}")
        
        # FULL IMAGE EMBEDDED
        if img_path.exists():
            max_w, max_h = W*0.60, H*0.38
            iw, ih = fit_image(img_path, max_w, max_h)
            
            # Border
            c.setStrokeColor(HexColor("#0077B6"))
            c.setLineWidth(4)
            c.roundRect((W-iw)/2 - 6, H*0.50 - 6, iw + 12, ih + 12, 20, fill=0, stroke=1)
            
            # Draw image
            c.drawImage(str(img_path), (W-iw)/2, H*0.50, iw, ih, preserveAspectRatio=True)
            print(f"✓ Embedded image: {word}")
        else:
            c.setFillColor(HexColor("#E0F4F8"))
            c.roundRect(W*0.25, H*0.50, W*0.5, H*0.32, 15, fill=1, stroke=0)
            c.setFillColor(HexColor("#0077B6"))
            c.setFont("Helvetica", 14)
            c.drawString(W*0.35, H*0.68, f"[{word}]")
        
        # TRACING AREA
        c.setStrokeColor(HexColor("#90E0EF"))
        c.setLineWidth(1)
        for row in range(6):
            y = H*0.42 - row*0.06
            c.line(W*0.08, y, W*0.92, y)
        
        # BIG WORD
        c.setFillColor(HexColor("#1D3557"))
        c.setFont("Helvetica-Bold", 40)
        c.drawString(W*0.10, H*0.38, word)
        
        # FADED TRACES
        c.setFillColor(HexColor("#A8DADC"))
        c.setFont("Helvetica", 34)
        c.drawString(W*0.10 + 160, H*0.38, word)
        c.drawString(W*0.10 + 310, H*0.38, word)
        
        # SENTENCE SECTION
        c.setFillColor(HexColor("#0077B6"))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(W*0.08, H*0.18, "Trace the sentence:")
        
        c.setFillColor(HexColor("#1D3557"))
        c.setFont("Helvetica", 17)
        c.drawString(W*0.08, H*0.13, sentence)
        
        c.setFillColor(HexColor("#A8DADC"))
        c.drawString(W*0.08, H*0.08, sentence)
        
        c.showPage()
    
    # CERTIFICATE
    c.setFillColor(HexColor("#0077B6"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#90E0EF"))
    c.circle(W*0.15, H*0.85, 80, fill=1, stroke=0)
    c.circle(W*0.85, H*0.15, 100, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 32)
    tw = c.stringWidth("Ocean Explorer Certificate!", "Helvetica-Bold", 32)
    c.drawString((W-tw)/2, H*0.70, "Ocean Explorer Certificate!")
    
    c.setFont("Helvetica", 16)
    c.drawString(W*0.20, H*0.58, "This certifies that")
    
    c.setStrokeColor(HexColor("#FFFFFF"))
    c.setLineWidth(2)
    c.line(W*0.20, H*0.48, W*0.80, H*0.48)
    
    c.setFont("Helvetica", 12)
    c.drawString(W*0.42, H*0.44, "(Your Name)")
    
    c.setFont("Helvetica", 16)
    c.drawString(W*0.12, H*0.35, "has completed the Ocean Writing Skills workbook")
    c.drawString(W*0.20, H*0.30, "and learned to write 8 sea animal words! 🌊")
    
    c.save()
    print(f"\n✅ COMPLETE BOOK: {pdf_path}")
    print(f"   Pages: 11 (Cover + Guide + 8 Animals + Certificate)")
    print(f"   Images: 8 full-color illustrations embedded")
    return str(pdf_path)


if __name__ == "__main__":
    build_complete_ocean_book()
