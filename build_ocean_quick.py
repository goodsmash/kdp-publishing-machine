#!/usr/bin/env python3
"""
Quick Ocean Workbook - No images, instant generation
Add images later with separate script
"""

from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def build_ocean_quick():
    """Build Ocean Writing Skills - fast version"""
    
    ocean_words = [
        ("fish", "The fish swims fast."),
        ("shark", "The shark is big."),
        ("whale", "The whale can sing."),
        ("turtle", "The turtle swims slow."),
        ("octopus", "The octopus has eight legs."),
        ("crab", "The crab walks sideways."),
        ("starfish", "The starfish has five arms."),
        ("seahorse", "The seahorse is small."),
    ]
    
    pdf_path = OUT_DIR / "Ocean_Writing_Skills_Workbook.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
    
    # Cover
    c.setFillColor(HexColor("#0077B6"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#90E0EF"))
    c.circle(W*0.8, H*0.8, 100, fill=1, stroke=0)
    c.setFillColor(HexColor("#CAF0F8"))
    c.circle(W*0.2, H*0.2, 150, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 38)
    c.drawString(W*0.08, H*0.65, "Ocean Writing")
    c.drawString(W*0.08, H*0.55, "Skills Workbook")
    
    c.setFont("Helvetica", 16)
    c.drawString(W*0.08, H*0.45, "Trace Words and Sentences")
    c.drawString(W*0.08, H*0.40, "with Sea Friends")
    
    c.setFillColor(HexColor("#FFD700"))
    c.roundRect(W*0.08, H*0.28, 140, 45, 22, fill=1, stroke=0)
    c.setFillColor(HexColor("#1D3557"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W*0.10, H*0.30, "Ages 3-6")
    
    c.showPage()
    
    # Content pages
    for i, (word, sentence) in enumerate(ocean_words):
        c.setFillColor(HexColor("#0077B6"))
        c.setFont("Helvetica-Bold", 22)
        c.drawString(W*0.06, H*0.92, f"Word {i+1}: {word.title()}")
        
        # Placeholder for image
        c.setFillColor(HexColor("#E0F4F8"))
        c.roundRect(W*0.25, H*0.55, W*0.5, H*0.30, 15, fill=1, stroke=0)
        c.setFillColor(HexColor("#0077B6"))
        c.setFont("Helvetica", 14)
        c.drawString(W*0.35, H*0.72, f"[{word} illustration]")
        c.setFont("Helvetica", 10)
        c.drawString(W*0.32, H*0.68, "Generate with: python3 add_images.py")
        
        # Tracing lines
        c.setStrokeColor(HexColor("#90E0EF"))
        for row in range(6):
            y = H*0.45 - row*0.06
            c.line(W*0.08, y, W*0.92, y)
        
        # Big word
        c.setFillColor(HexColor("#1D3557"))
        c.setFont("Helvetica-Bold", 36)
        c.drawString(W*0.10, H*0.40, word)
        
        # Faded traces
        c.setFillColor(HexColor("#A8DADC"))
        c.setFont("Helvetica", 30)
        c.drawString(W*0.10 + 160, H*0.40, word)
        c.drawString(W*0.10 + 310, H*0.40, word)
        
        # Sentence
        c.setFillColor(HexColor("#0077B6"))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(W*0.08, H*0.15, "Trace the sentence:")
        
        c.setFillColor(HexColor("#1D3557"))
        c.setFont("Helvetica", 16)
        c.drawString(W*0.08, H*0.10, sentence)
        
        c.setFillColor(HexColor("#A8DADC"))
        c.drawString(W*0.08, H*0.05, sentence)
        
        c.showPage()
    
    # Certificate
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
    c.drawString(W*0.15, H*0.35, "has completed the Ocean Writing Skills workbook")
    c.drawString(W*0.22, H*0.30, "and learned to write 8 sea animal words!")
    
    c.save()
    print(f"✅ Created: {pdf_path}")
    return str(pdf_path)


if __name__ == "__main__":
    build_ocean_quick()
