#!/usr/bin/env python3
"""
Premium Compact Workbook Generator
Shorter, punchier, higher quality workbooks (20-40 pages)
Premium design, better layouts, engaging content
"""

import os
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from PIL import Image
from datetime import datetime

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


class PremiumCompactWorkbook:
    def __init__(self, theme, title, subtitle, age="3-6"):
        self.theme = theme
        self.title = title
        self.subtitle = subtitle
        self.age = age
        self.words = self._get_words()
        self.colors = {
            "primary": HexColor("#FF6B6B"),
            "secondary": HexColor("#4ECDC4"),
            "accent": HexColor("#FFE66D"),
            "dark": HexColor("#2C3E50"),
            "light": HexColor("#F7F9FC"),
        }
        
    def _get_words(self):
        themes = {
            "animals": [
                ("cat", "The cat sleeps."),
                ("dog", "The dog runs fast."),
                ("bird", "Birds can fly high."),
                ("fish", "Fish swim in water."),
                ("bear", "Bears are big and strong."),
                ("frog", "Frogs love to hop."),
            ],
            "space": [
                ("star", "Stars twinkle at night."),
                ("moon", "The moon glows softly."),
                ("rocket", "Rockets zoom to space."),
                ("planet", "Planets orbit the sun."),
                ("alien", "Aliens might be friendly."),
                ("comet", "Comets have long tails."),
            ],
            "dinosaurs": [
                ("trex", "T-Rex has sharp teeth."),
                ("stego", "Stegosaurus has plates."),
                ("raptor", "Raptors run very fast."),
                ("bronto", "Brontosaurus is gentle."),
            ],
            "princess": [
                ("crown", "Crowns are shiny gold."),
                ("castle", "Castles have tall towers."),
                ("dress", "Dresses can sparkle."),
                ("wand", "Wands make magic happen."),
            ],
        }
        return themes.get(self.theme, themes["animals"])
    
    def generate(self, image_files=None):
        pdf_path = OUT_DIR / f"{self.title.replace(' ', '_')}_Premium.pdf"
        W, H = 8.5 * inch, 11 * inch
        c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
        
        # Bold cover
        self._draw_cover(c, W, H)
        
        # Quick start guide (1 page)
        self._draw_guide(c, W, H)
        
        # Word skills pages (4-6 words)
        for i, (word, sentence) in enumerate(self.words):
            img = image_files[i] if image_files and i < len(image_files) else None
            self._draw_skill_page(c, W, H, i+1, word, sentence, img)
        
        # Practice spread
        self._draw_practice_page(c, W, H)
        
        # Achievement page
        self._draw_achievement(c, W, H)
        
        c.save()
        return str(pdf_path)
    
    def _draw_cover(self, c, W, H):
        # Bold gradient background
        c.setFillColor(self.colors["primary"])
        c.rect(0, 0, W, H, fill=1, stroke=0)
        
        # Geometric accent
        c.setFillColor(self.colors["secondary"])
        c.circle(W*0.85, H*0.75, 100, fill=1, stroke=0)
        c.setFillColor(self.colors["accent"])
        c.circle(W*0.15, H*0.20, 80, fill=1, stroke=0)
        
        # Big bold title
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 48)
        words = self.title.split()
        y = H * 0.60
        for word in words[:3]:
            c.drawString(W*0.08, y, word)
            y -= 55
        
        # Subtitle
        c.setFont("Helvetica-Bold", 18)
        c.drawString(W*0.08, H*0.35, self.subtitle)
        
        # Age badge
        c.setFillColor(self.colors["accent"])
        c.roundRect(W*0.08, H*0.22, 120, 40, 20, fill=1, stroke=0)
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica-Bold", 14)
        c.drawString(W*0.10, H*0.23 + 15, f"Ages {self.age}")
        
        c.showPage()
    
    def _draw_guide(self, c, W, H):
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica-Bold", 24)
        c.drawString(W*0.08, H*0.88, "Let's Get Started!")
        
        steps = [
            ("1", "Trace the BIG word", "Use your finger first"),
            ("2", "Write it yourself", "Try without tracing"),
            ("3", "Trace the sentence", "Copy the whole line"),
            ("4", "Say it out loud", "Speak while you write"),
        ]
        
        y = H * 0.70
        for num, title, tip in steps:
            # Number circle
            c.setFillColor(self.colors["primary"])
            c.circle(W*0.12, y+10, 20, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(W*0.12-5, y+5, num)
            
            # Text
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica-Bold", 16)
            c.drawString(W*0.20, y+10, title)
            c.setFont("Helvetica", 11)
            c.setFillColor(HexColor("#666666"))
            c.drawString(W*0.20, y-8, tip)
            y -= 60
        
        # Pro tip
        c.setFillColor(self.colors["accent"])
        c.roundRect(W*0.08, H*0.25, W*0.84, 60, 10, fill=1, stroke=0)
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica-Bold", 13)
        c.drawString(W*0.12, H*0.30, "💡 Pro Tip: Practice 10 minutes every day!")
        
        c.showPage()
    
    def _draw_skill_page(self, c, W, H, num, word, sentence, img_path):
        # Header bar
        c.setFillColor(self.colors["primary"])
        c.rect(0, H*0.88, W, H*0.12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(W*0.05, H*0.92, f"#{num}  {word.upper()}")
        
        # Image or placeholder
        if img_path and Path(img_path).exists():
            iw, ih = fit_image(img_path, W*0.55, H*0.32)
            c.drawImage(str(img_path), (W-iw)/2, H*0.52, iw, ih, preserveAspectRatio=True)
        else:
            c.setFillColor(self.colors["light"])
            c.roundRect(W*0.22, H*0.52, W*0.56, H*0.30, 15, fill=1, stroke=0)
            c.setFillColor(HexColor("#CCCCCC"))
            c.setFont("Helvetica", 12)
            c.drawString(W*0.38, H*0.68, f"[{word} image]")
        
        # Big traceable word
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica-Bold", 42)
        c.drawString(W*0.08, H*0.38, word)
        
        # Faded traces
        c.setFillColor(HexColor("#DDDDDD"))
        c.setFont("Helvetica", 36)
        c.drawString(W*0.08 + 180, H*0.38, word)
        c.drawString(W*0.08 + 340, H*0.38, word)
        
        # Sentence section
        c.setFillColor(self.colors["secondary"])
        c.setFont("Helvetica-Bold", 13)
        c.drawString(W*0.08, H*0.22, "Write the sentence:")
        
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica", 15)
        c.drawString(W*0.08, H*0.16, sentence)
        
        c.setFillColor(HexColor("#BBBBBB"))
        c.drawString(W*0.08, H*0.10, sentence)
        
        c.showPage()
    
    def _draw_practice_page(self, c, W, H):
        c.setFillColor(self.colors["secondary"])
        c.rect(0, H*0.88, W, H*0.12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(W*0.05, H*0.92, "Extra Practice")
        
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica", 13)
        c.drawString(W*0.05, H*0.80, "Write your favorite words here:")
        
        # Writing lines
        c.setStrokeColor(HexColor("#E0E0E0"))
        for i in range(8):
            y = H*0.70 - i*0.07*inch
            c.line(W*0.05, y, W*0.95, y)
        
        c.showPage()
    
    def _draw_achievement(self, c, W, H):
        # Celebratory background
        c.setFillColor(self.colors["accent"])
        c.rect(0, 0, W, H, fill=1, stroke=0)
        
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica-Bold", 36)
        tw = c.stringWidth("Amazing Work!", "Helvetica-Bold", 36)
        c.drawString((W-tw)/2, H*0.75, "Amazing Work!")
        
        c.setFont("Helvetica", 16)
        c.drawString(W*0.20, H*0.65, "You completed your writing practice!")
        
        # Star badge
        c.setFillColor(self.colors["primary"])
        c.circle(W*0.5, H*0.45, 80, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 60)
        c.drawString(W*0.46, H*0.48, "★")
        
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica", 12)
        c.drawString(W*0.25, H*0.25, "Signed: ____________________")
        c.drawString(W*0.25, H*0.18, f"Date: ____________ {datetime.now().year}")
        
        c.showPage()


def main():
    books = [
        ("animals", "Wild Animals Write", "Trace and learn animal words", "3-5"),
        ("space", "Space Explorer Write", "Trace and learn space words", "4-6"),
        ("dinosaurs", "Dino Writer", "Trace and learn dinosaur words", "3-6"),
        ("princess", "Royal Writer", "Trace and learn royal words", "3-6"),
    ]
    
    for theme, title, subtitle, age in books:
        print(f"\n🎯 Building: {title}")
        gen = PremiumCompactWorkbook(theme, title, subtitle, age)
        pdf = gen.generate()
        print(f"   ✅ Created: {pdf}")
    
    print("\n" + "="*50)
    print("All premium compact books ready!")


if __name__ == "__main__":
    main()
