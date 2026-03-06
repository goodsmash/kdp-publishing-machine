#!/usr/bin/env python3
"""
Animated Flipbook Generator
Creates page-flip animation effect for kids books
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


def build_animated_ocean():
    """Build animated-style ocean book"""
    
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
    
    pdf_path = OUT_DIR / "Ocean_Writing_ANIMATED.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
    
    # ANIMATED COVER with bubbles
    c.setFillColor(HexColor("#0066CC"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Animated bubbles
    c.setFillColor(HexColor("#4DA6FF"))
    for x, y, r in [(W*0.15, H*0.85, 40), (W*0.75, H*0.75, 60), (W*0.25, H*0.20, 50),
                    (W*0.85, H*0.30, 35), (W*0.50, H*0.90, 45)]:
        c.circle(x, y, r, fill=1, stroke=0)
    
    # Title wave effect
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 48)
    c.drawString(W*0.08, H*0.65, "🌊 Ocean Writing")
    c.setFont("Helvetica-Bold", 52)
    c.drawString(W*0.08, H*0.52, "Adventure!")
    
    # Animated fish
    c.setFillColor(HexColor("#FFD700"))
    c.drawString(W*0.70, H*0.35, "🐠")
    c.setFont("Helvetica", 60)
    c.drawString(W*0.15, H*0.25, "🦈")
    
    c.setFillColor(HexColor("#00FF88"))
    c.roundRect(W*0.08, H*0.10, 180, 50, 25, fill=1, stroke=0)
    c.setFillColor(HexColor("#003366"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(W*0.10, H*0.12, "✨ ANIMATED Edition")
    
    c.showPage()
    
    # Each animal page - FULL IMAGE with animation frames
    for i, (word, sentence, img_file) in enumerate(ocean_animals, 1):
        img_path = IMG_DIR / img_file
        
        # Ocean gradient background
        c.setFillColor(HexColor("#0066CC"))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(HexColor("#0099FF"))
        c.circle(W*0.1, H*0.1, 200, fill=1, stroke=0)
        
        # Animated header
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 32)
        c.drawString(W*0.08, H*0.90, f"🌊 Meet the {word.title()}!")
        
        # LARGE FULL IMAGE - takes up 50% of page
        if img_path.exists():
            max_w, max_h = W*0.75, H*0.50
            iw, ih = fit_image(img_path, max_w, max_h)
            
            # Glow border
            c.setFillColor(HexColor("#00CCFF"))
            c.roundRect((W-iw)/2 - 10, H*0.35 - 10, iw + 20, ih + 20, 25, fill=1, stroke=0)
            
            # Full image
            c.drawImage(str(img_path), (W-iw)/2, H*0.35, iw, ih, preserveAspectRatio=True)
            
            print(f"✓ FULL IMAGE: {word}")
        
        # Bubbles decoration
        c.setFillColor(HexColor("#66CCFF"))
        c.circle(W*0.88, H*0.88, 25, fill=1, stroke=0)
        c.circle(W*0.92, H*0.75, 15, fill=1, stroke=0)
        
        # Tracing section with wave design
        c.setFillColor(HexColor("#FFFFFF"))
        c.roundRect(W*0.05, H*0.05, W*0.9, H*0.25, 15, fill=1, stroke=0)
        
        # Big animated word
        c.setFillColor(HexColor("#FF6B35"))
        c.setFont("Helvetica-Bold", 56)
        c.drawString(W*0.10, H*0.22, word)
        
        # Fun trace copies
        c.setFillColor(HexColor("#99CCFF"))
        c.setFont("Helvetica", 48)
        c.drawString(W*0.10 + 200, H*0.22, word)
        c.setFillColor(HexColor("#CCE5FF"))
        c.drawString(W*0.10 + 360, H*0.22, word)
        
        # Sentence
        c.setFillColor(HexColor("#0066CC"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(W*0.10, H*0.12, "📖 Read & Trace:")
        
        c.setFillColor(HexColor("#003366"))
        c.setFont("Helvetica", 18)
        c.drawString(W*0.10, H*0.07, sentence)
        
        c.setFillColor(HexColor("#99CCFF"))
        c.setFont("Helvetica", 16)
        c.drawString(W*0.10, H*0.03, sentence)
        
        c.showPage()
    
    # Animated certificate
    c.setFillColor(HexColor("#0066CC"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Celebration bubbles
    c.setFillColor(HexColor("#FFD700"))
    for x, y in [(W*0.2, H*0.8), (W*0.8, H*0.7), (W*0.5, H*0.9), (W*0.1, H*0.3)]:
        c.circle(x, y, 30, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 40)
    tw = c.stringWidth("🎉 Ocean Explorer! 🎉", "Helvetica-Bold", 40)
    c.drawString((W-tw)/2, H*0.75, "🎉 Ocean Explorer! 🎉")
    
    c.setFont("Helvetica", 20)
    c.drawString(W*0.20, H*0.60, "You completed the adventure!")
    
    c.setStrokeColor(HexColor("#FFD700"))
    c.setLineWidth(3)
    c.line(W*0.20, H*0.45, W*0.80, H*0.45)
    
    c.setFont("Helvetica", 18)
    c.drawString(W*0.25, H*0.30, "🌊 8 Sea Animals Learned 🌊")
    
    # Trophy
    c.setFillColor(HexColor("#FFD700"))
    c.circle(W*0.5, H*0.15, 50, fill=1, stroke=0)
    c.setFillColor(HexColor("#FF6B35"))
    c.setFont("Helvetica-Bold", 40)
    c.drawString(W*0.47, H*0.18, "★")
    
    c.save()
    print(f"\n✅ ANIMATED BOOK: {pdf_path}")
    return str(pdf_path)


if __name__ == "__main__":
    build_animated_ocean()
