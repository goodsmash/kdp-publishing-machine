#!/usr/bin/env python3
"""
KDP Cover Generator
Creates simple, professional covers for children's books
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

# Cover templates with different layouts
COVER_TEMPLATES = {
    "center": {
        "title_y": 7.5 * inch,
        "subtitle_y": 6.8 * inch,
        "image_y": 4 * inch,
        "author_y": 1.5 * inch
    },
    "top": {
        "title_y": 9 * inch,
        "subtitle_y": 8.2 * inch,
        "image_y": 4.5 * inch,
        "author_y": 1.5 * inch
    },
    "bottom": {
        "title_y": 9.5 * inch,
        "subtitle_y": 8.8 * inch,
        "image_y": 2.5 * inch,
        "author_y": 1 * inch
    }
}

# Background patterns (simple colors for now)
BACKGROUNDS = {
    "sunset": ["#FF6B6B", "#FFE66D"],
    "ocean": ["#4ECDC4", "#556270"],
    "forest": ["#96CEB4", "#FFEAA7"],
    "night": ["#2C3E50", "#4A69BD"],
    "candy": ["#FD79A8", "#FDCB6E"],
    "spring": ["#A8E6CF", "#DCEDC1"]
}

SIMPLE_ICONS = {
    "seed": "🌱",
    "flower": "🌸",
    "owl": "🦉",
    "moon": "🌙",
    "bear": "🐻",
    "honey": "🍯",
    "dog": "🐕",
    "rainbow": "🌈",
    "crab": "🦀",
    "shell": "🐚",
    "star": "⭐",
    "heart": "❤️"
}

class CoverGenerator:
    """Generate professional KDP book covers"""
    
    # KDP cover sizes (front only, no spine or back for now)
    SIZES = {
        "8x10": {"width": 8 * inch, "height": 10 * inch},
        "8.5x8.5": {"width": 8.5 * inch, "height": 8.5 * inch},
        "7x10": {"width": 7 * inch, "height": 10 * inch},
        "6x9": {"width": 6 * inch, "height": 9 * inch},
    }
    
    def __init__(self, title, subtitle, size="8x10", template="center", bg="sunset", icon="star"):
        self.title = title
        self.subtitle = subtitle
        self.size_key = size
        self.size = self.SIZES[size]
        self.template = COVER_TEMPLATES[template]
        self.bg_colors = BACKGROUNDS[bg]
        self.icon = SIMPLE_ICONS.get(icon, "⭐")
        
        os.makedirs("covers", exist_ok=True)
        
    def generate(self, author="KDP Publishing"):
        """Generate the cover PDF"""
        filename = f"covers/{self.title.replace(' ', '_')}_cover_{self.size_key}.pdf"
        
        c = canvas.Canvas(filename, pagesize=(self.size["width"], self.size["height"]))
        
        # Background gradient (simulated with rectangle)
        c.setFillColor(HexColor(self.bg_colors[0]))
        c.rect(0, 0, self.size["width"], self.size["height"], fill=1, stroke=0)
        
        # Bottom gradient
        c.setFillColor(HexColor(self.bg_colors[1]))
        c.rect(0, 0, self.size["width"], self.size["height"] * 0.4, fill=1, stroke=0)
        
        # Decorative border
        margin = 0.25 * inch
        c.setStrokeColor(HexColor("#FFFFFF"))
        c.setLineWidth(3)
        c.roundRect(margin, margin, 
                   self.size["width"] - 2*margin, 
                   self.size["height"] - 2*margin, 
                   20, fill=0, stroke=1)
        
        # Title
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(HexColor("#FFFFFF"))
        title_width = c.stringWidth(self.title, "Helvetica-Bold", 36)
        c.drawString((self.size["width"] - title_width) / 2, 
                    self.template["title_y"], 
                    self.title)
        
        # Subtitle
        c.setFont("Helvetica", 18)
        subtitle_width = c.stringWidth(self.subtitle, "Helvetica", 18)
        c.drawString((self.size["width"] - subtitle_width) / 2,
                    self.template["subtitle_y"],
                    self.subtitle)
        
        # Central icon/image placeholder
        c.setFont("Helvetica", 120)
        icon_width = c.stringWidth(self.icon, "Helvetica", 120)
        c.drawString((self.size["width"] - icon_width) / 2,
                    self.template["image_y"],
                    self.icon)
        
        # Author
        c.setFont("Helvetica", 14)
        c.setFillColor(HexColor("#FFFFFF"))
        author_text = f"By {author}"
        author_width = c.stringWidth(author_text, "Helvetica", 14)
        c.drawString((self.size["width"] - author_width) / 2,
                    self.template["author_y"],
                    author_text)
        
        # Series info (if applicable)
        c.setFont("Helvetica", 10)
        series_text = "A Children's Learning Book"
        series_width = c.stringWidth(series_text, "Helvetica", 10)
        c.drawString((self.size["width"] - series_width) / 2,
                    0.5 * inch,
                    series_text)
        
        c.save()
        print(f"✅ Cover created: {filename}")
        return filename


def generate_covers_for_books():
    """Generate covers for all existing books"""
    
    books = [
        ("The Brave Little Seed", "A Story About Growing", "forest", "seed"),
        ("La Semillita Valiente", "Una Historia Sobre Crecer", "forest", "seed"),
        ("Luna and the Moon", "A Bedtime Story", "night", "moon"),
        ("Benny Bear's First Honey", "A Story About Trying New Things", "candy", "honey"),
        ("Mia Chases the Rainbow", "A Story About Colors", "spring", "rainbow"),
        ("Sammy Finds His Shell", "A Story About Being Yourself", "ocean", "shell"),
    ]
    
    print("Generating covers for all books...")
    print("=" * 50)
    
    for title, subtitle, bg, icon in books:
        print(f"\nCreating: {title}")
        gen = CoverGenerator(title, subtitle, size="8x10", template="center", bg=bg, icon=icon)
        gen.generate()
    
    print("\n" + "=" * 50)
    print("All covers generated in covers/ folder")
    print("\nNote: These are simple covers. For professional sales,")
    print("consider hiring an illustrator on Fiverr or 99designs.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        generate_covers_for_books()
    else:
        # Generate single cover
        title = sys.argv[1] if len(sys.argv) > 1 else "My Book Title"
        subtitle = sys.argv[2] if len(sys.argv) > 2 else "My Subtitle"
        bg = sys.argv[3] if len(sys.argv) > 3 else "sunset"
        icon = sys.argv[4] if len(sys.argv) > 4 else "star"
        
        gen = CoverGenerator(title, subtitle, bg=bg, icon=icon)
        gen.generate()
