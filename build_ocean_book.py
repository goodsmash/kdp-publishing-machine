#!/usr/bin/env python3
"""
Ocean Writing Skills Workbook
Full production with Alibaba model rotation
"""

import os
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

from alibaba_model_rotator import AlibabaModelRotator


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def build_ocean_book():
    """Build Ocean Writing Skills with Qwen illustrations"""
    
    rotator = AlibabaModelRotator()
    
    # Ocean theme words and prompts
    ocean_content = [
        ("fish", "The fish swims fast.", "colorful tropical fish swimming in coral reef, children's book illustration"),
        ("shark", "The shark is big.", "friendly cartoon shark smiling, underwater scene, children's book style"),
        ("whale", "The whale can sing.", "cute blue whale spouting water, ocean background, children's illustration"),
        ("turtle", "The turtle swims slow.", "cute sea turtle with shell, underwater, children's book art"),
        ("octopus", "The octopus has eight legs.", "friendly pink octopus with tentacles, ocean floor, kids book style"),
        ("crab", "The crab walks sideways.", "cute red crab on sandy beach, children's illustration"),
        ("starfish", "The starfish has five arms.", "colorful starfish on ocean floor, children's book art"),
        ("seahorse", "The seahorse is small.", "cute yellow seahorse swimming, coral reef, kids illustration"),
    ]
    
    print("🌊 Building Ocean Writing Skills Workbook")
    print("="*60)
    
    # Generate all images first
    images = []
    for word, sentence, prompt in ocean_content:
        print(f"\n🎨 Generating: {word}")
        img_path = rotator.generate_image(prompt, f"ocean_{word}")
        if img_path:
            images.append(img_path)
            print(f"   ✅ Saved: {img_path}")
        else:
            print(f"   ⚠️  Failed, will use placeholder")
            images.append(None)
    
    # Build PDF
    print("\n📚 Building PDF...")
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
    
    c.setFillColor(white)
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
    
    # Guide page
    c.setFillColor(HexColor("#1D3557"))
    c.setFont("Helvetica-Bold", 24)
    c.drawString(W*0.08, H*0.88, "How to Use This Book")
    
    tips = [
        "1. Look at the ocean animal picture",
        "2. Trace the word in BIG letters",
        "3. Trace it two more times",
        "4. Trace the sentence at the bottom",
        "5. Color the picture when done!",
    ]
    
    c.setFont("Helvetica", 14)
    y = H*0.75
    for tip in tips:
        c.drawString(W*0.10, y, tip)
        y -= 35
    
    c.showPage()
    
    # Content pages
    for i, (word, sentence, _) in enumerate(ocean_content):
        img_path = images[i] if i < len(images) else None
        
        # Header
        c.setFillColor(HexColor("#0077B6"))
        c.setFont("Helvetica-Bold", 22)
        c.drawString(W*0.06, H*0.92, f"Word {i+1}: {word.title()}")
        
        # Image
        if img_path and Path(img_path).exists():
            max_w, max_h = W*0.55, H*0.35
            iw, ih = fit_image(img_path, max_w, max_h)
            c.drawImage(str(img_path), (W-iw)/2, H*0.52, iw, ih, preserveAspectRatio=True)
        else:
            c.setFillColor(HexColor("#E0F4F8"))
            c.roundRect(W*0.25, H*0.52, W*0.5, H*0.32, 15, fill=1, stroke=0)
            c.setFillColor(HexColor("#0077B6"))
            c.setFont("Helvetica", 14)
            c.drawString(W*0.35, H*0.68, f"[{word} illustration]")
        
        # Tracing lines
        c.setStrokeColor(HexColor("#90E0EF"))
        for row in range(6):
            y = H*0.42 - row*0.06
            c.line(W*0.08, y, W*0.92, y)
        
        # Big word
        c.setFillColor(HexColor("#1D3557"))
        c.setFont("Helvetica-Bold", 36)
        c.drawString(W*0.10, H*0.38, word)
        
        # Faded traces
        c.setFillColor(HexColor("#A8DADC"))
        c.setFont("Helvetica", 30)
        c.drawString(W*0.10 + 160, H*0.38, word)
        c.drawString(W*0.10 + 310, H*0.38, word)
        
        # Sentence section
        c.setFillColor(HexColor("#0077B6"))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(W*0.08, H*0.18, "Trace the sentence:")
        
        c.setFillColor(HexColor("#1D3557"))
        c.setFont("Helvetica", 16)
        c.drawString(W*0.08, H*0.13, sentence)
        
        c.setFillColor(HexColor("#A8DADC"))
        c.drawString(W*0.08, H*0.08, sentence)
        
        c.showPage()
    
    # Certificate
    c.setFillColor(HexColor("#0077B6"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(HexColor("#90E0EF"))
    c.circle(W*0.15, H*0.85, 80, fill=1, stroke=0)
    c.circle(W*0.85, H*0.15, 100, fill=1, stroke=0)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 32)
    tw = c.stringWidth("Ocean Explorer Certificate!", "Helvetica-Bold", 32)
    c.drawString((W-tw)/2, H*0.70, "Ocean Explorer Certificate!")
    
    c.setFont("Helvetica", 16)
    c.drawString(W*0.20, H*0.58, "This certifies that")
    
    c.setStrokeColor(white)
    c.setLineWidth(2)
    c.line(W*0.20, H*0.48, W*0.80, H*0.48)
    
    c.setFont("Helvetica", 12)
    c.drawString(W*0.42, H*0.44, "(Your Name)")
    
    c.setFont("Helvetica", 16)
    c.drawString(W*0.15, H*0.35, "has completed the Ocean Writing Skills workbook")
    c.drawString(W*0.22, H*0.30, "and learned to write 8 sea animal words!")
    
    c.setFillColor(HexColor("#FFD700"))
    c.circle(W*0.5, H*0.18, 30, fill=1, stroke=0)
    c.setFillColor(HexColor("#1D3557"))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(W*0.48, H*0.19, "★")
    
    c.save()
    print(f"\n✅ Created: {pdf_path}")
    
    # Show quota status
    print("\n" + "="*60)
    print("QUOTA USED TODAY")
    print("="*60)
    status = rotator.get_status()
    total_used = sum(status["usage"].values())
    print(f"Total generations: {total_used}")
    
    return str(pdf_path)


if __name__ == "__main__":
    build_ocean_book()
