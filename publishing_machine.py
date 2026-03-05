#!/usr/bin/env python3
"""
KDP Publishing Machine Pro - Professional children's book generator
Supports: English/Spanish, multiple trim sizes, age groups, series
Amazon KDP best practices compliant
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, CMYKColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import textwrap
import os
import json
import random
from datetime import datetime

# Import expanded story library
try:
    from story_library_expansion import ADDITIONAL_STORIES_EN, ADDITIONAL_STORIES_ES
except ImportError:
    ADDITIONAL_STORIES_EN = {}
    ADDITIONAL_STORIES_ES = {}
from reportlab.lib.colors import HexColor, CMYKColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import textwrap
import os
import json
import random
from datetime import datetime

# ==================== KDP SPECIFICATIONS ====================
KDP_SIZES = {
    "8x10": {"width": 8*inch, "height": 10*inch, "bleed": 0.125*inch, "pages": "24-480"},
    "8.5x8.5": {"width": 8.5*inch, "height": 8.5*inch, "bleed": 0.125*inch, "pages": "24-480"},
    "7x10": {"width": 7*inch, "height": 10*inch, "bleed": 0.125*inch, "pages": "24-480"},
    "6x9": {"width": 6*inch, "height": 9*inch, "bleed": 0, "pages": "24-480"},
    "5.5x8.5": {"width": 5.5*inch, "height": 8.5*inch, "bleed": 0, "pages": "24-480"},
}

AGE_GROUPS = {
    "2-4": {"font_size": 20, "line_spacing": 32, "words_per_page": 15, "vocab_level": "simple"},
    "3-6": {"font_size": 18, "line_spacing": 28, "words_per_page": 20, "vocab_level": "simple"},
    "4-7": {"font_size": 18, "line_spacing": 28, "words_per_page": 25, "vocab_level": "early"},
    "5-7": {"font_size": 18, "line_spacing": 28, "words_per_page": 25, "vocab_level": "early"},
    "6-8": {"font_size": 16, "line_spacing": 26, "words_per_page": 35, "vocab_level": "growing"},
    "8-10": {"font_size": 14, "line_spacing": 22, "words_per_page": 50, "vocab_level": "growing"},
}

# Professional color palettes
PALETTES = {
    "warm": {"primary": "#E07A5F", "secondary": "#F2CC8F", "accent": "#81B29A", "text": "#3D405B"},
    "cool": {"primary": "#6B8E9F", "secondary": "#A8DADC", "accent": "#F1FAEE", "text": "#1D3557"},
    "pastel": {"primary": "#FFB3BA", "secondary": "#FFDFBA", "accent": "#FFFFBA", "text": "#6A4C93"},
    "nature": {"primary": "#588157", "secondary": "#A3B18A", "accent": "#DAD7CD", "text": "#344E41"},
    "bedtime": {"primary": "#4A4E69", "secondary": "#9A8C98", "accent": "#C9ADA7", "text": "#F2E9E4"},
}

# ==================== STORY TEMPLATES ====================
STORY_LIBRARY = {
    "en": {
        "brave_seed": {
            "title": "The Brave Little Seed",
            "subtitle": "A Story About Growing",
            "series": "Nature Friends",
            "book_number": 1,
            "age": "4-7",
            "palette": "nature",
            "description": "A tiny seed learns about courage and patience on its journey to becoming a flower.",
            "keywords": ["seed", "growing", "nature", "bravery", "patience", "garden"],
            "new_words": ["brave", "tumble", "burrow", "sprout", "bloom", "patience"],
            "chapters": [
                {"type": "copyright"},
                {"type": "dedication", "text": "For every child learning to grow"},
                {"type": "title_page"},
                {"type": "illustration", "desc": "seed_on_flower"},
                {"type": "text", "content": "High up in the garden, there lived a tiny seed. The seed was small and round and brown, no bigger than a drop of rain."},
                {"type": "text", "content": "The little seed loved its cozy home on the flower. It felt safe and warm in the sunshine."},
                {"type": "illustration", "desc": "wind_coming"},
                {"type": "text", "content": "But one day, a big wind came whooshing through the garden. The flowers swayed. The leaves rustled."},
                {"type": "text", "content": "Whoosh! The tiny seed did a big tumble through the air, spinning round and round."},
                {"type": "vocab", "word": "tumble", "definition": "To roll and fall over and over", "example": "The acorn did a tumble down the hill."},
                {"type": "illustration", "desc": "seed_falling"},
                {"type": "text", "content": "Down, down, down went the seed. It was scared, but it tried to be brave."},
                {"type": "vocab", "word": "brave", "definition": "Being strong even when you are scared", "example": "The brave puppy protected his friend."},
                {"type": "text", "content": "The seed landed with a tiny plop in the soft, dark dirt. It wiggled and made a little burrow to rest in."},
                {"type": "vocab", "word": "burrow", "definition": "A cozy little hole in the ground", "example": "The bunny made a burrow under the tree."},
                {"type": "illustration", "desc": "seed_underground"},
                {"type": "text", "content": "The seed was tired from its big adventure. It closed its eyes and went to sleep in its dark, warm burrow."},
                {"type": "text", "content": "Days passed. The rain came and gave the seed a drink. The sun warmed the earth above."},
                {"type": "text", "content": "The seed waited with patience, trusting that good things were coming."},
                {"type": "vocab", "word": "patience", "definition": "Waiting calmly for good things to happen", "example": "The bird showed patience waiting for the worm."},
                {"type": "illustration", "desc": "rain_and_sun"},
                {"type": "text", "content": "Then one morning, something magical happened! The seed felt a tickle deep inside."},
                {"type": "text", "content": "The seed began to sprout! A tiny green shoot pushed up through the dirt, reaching for the light."},
                {"type": "vocab", "word": "sprout", "definition": "When a plant starts to grow", "example": "We watched the bean sprout in the cup."},
                {"type": "illustration", "desc": "little_sprout"},
                {"type": "text", "content": "Up and up grew the little plant, getting taller every day. It stretched its leaves toward the warm sun."},
                {"type": "text", "content": "The rain came to give it water. The sun gave it energy. The plant grew stronger and stronger."},
                {"type": "illustration", "desc": "growing_plant"},
                {"type": "text", "content": "At last, the plant was big and strong. Its stem was tall. Its leaves were wide."},
                {"type": "text", "content": "And then, on a bright sunny morning... the plant opened its petals wide and showed the world its beautiful bloom!"},
                {"type": "vocab", "word": "bloom", "definition": "When a flower opens up", "example": "We waited all spring for the tulips to bloom."},
                {"type": "illustration", "desc": "beautiful_flower"},
                {"type": "text", "content": "The brave little seed had grown into the most lovely flower in the whole garden."},
                {"type": "text", "content": "And all because it was brave enough to tumble, patient enough to wait, and strong enough to grow."},
                {"type": "text", "content": "The End."},
                {"type": "back_matter"},
            ]
        },
        # ... (more English stories)
    },
    "es": {
        "semilla_valiente": {
            "title": "La Semillita Valiente",
            "subtitle": "Una Historia Sobre Crecer",
            "series": "Amigos de la Naturaleza",
            "book_number": 1,
            "age": "4-7",
            "palette": "nature",
            "description": "Una semilla pequeña aprende sobre coraje y paciencia en su viaje para convertirse en flor.",
            "keywords": ["semilla", "crecer", "naturaleza", "valiente", "paciencia", "jardín"],
            "new_words": ["valiente", "rodar", "madriguera", "brotar", "florecer", "paciencia"],
            "chapters": [
                {"type": "copyright"},
                {"type": "dedication", "text": "Para cada niño aprendiendo a crecer"},
                {"type": "title_page"},
                {"type": "illustration", "desc": "semilla_en_flor"},
                {"type": "text", "content": "Allá arriba en el jardín, vivía una semilla pequeña. La semilla era redonda y marrón, no más grande que una gota de lluvia."},
                {"type": "text", "content": "A la semillita le encantaba su hogar acogedor en la flor. Se sentía segura y calentita bajo el sol."},
                {"type": "illustration", "desc": "viento_acercandose"},
                {"type": "text", "content": "Pero un día, un viento grande vino soplando por el jardín. Las flores se balanceaban. Las hojas crujían."},
                {"type": "text", "content": "¡Whoosh! La semillita dio un gran rollo por el aire, girando y girando."},
                {"type": "vocab", "word": "rodar", "definition": "Caer y girar una y otra vez", "example": "La bellota rodó colina abajo."},
                {"type": "illustration", "desc": "semilla_cayendo"},
                {"type": "text", "content": "Abajo, abajo, abajo fue la semilla. Tenía miedo, pero trató de ser valiente."},
                {"type": "vocab", "word": "valiente", "definition": "Ser fuerte aunque tengas miedo", "example": "El perrito valiente protegió a su amigo."},
                {"type": "text", "content": "La semilla aterrizó con un pequeño plop en la tierra suave y oscura. Se retorció y hizo una pequeña madriguera para descansar."},
                {"type": "vocab", "word": "madriguera", "definition": "Un hueco acogedor bajo la tierra", "example": "El conejito hizo una madriguera bajo el árbol."},
                {"type": "illustration", "desc": "semilla_bajo_tierra"},
                {"type": "text", "content": "La semilla estaba cansada de su gran aventura. Cerró sus ojos y se durmió en su madriguera oscura y calentita."},
                {"type": "text", "content": "Pasaron los días. La lluvia vino y dio a la semilla un trago. El sol calentó la tierra de arriba."},
                {"type": "text", "content": "La semilla esperó con paciencia, confiando que cosas buenas vendrían."},
                {"type": "vocab", "word": "paciencia", "definition": "Esperar tranquilamente que pasen cosas buenas", "example": "El pájaro mostró paciencia esperando al gusano."},
                {"type": "illustration", "desc": "lluvia_y_sol"},
                {"type": "text", "content": "¡Entonces una mañana, algo mágico sucedió! La semilla sintió una cosquilla profunda adentro."},
                {"type": "text", "content": "¡La semilla comenzó a brotar! Un pequeño tallo verde empujó hacia arriba a través de la tierra, buscando la luz."},
                {"type": "vocab", "word": "brotar", "definition": "Cuando una planta empieza a crecer", "example": "Vimos al frijol brotar en el vaso."},
                {"type": "illustration", "desc": "pequeño_brote"},
                {"type": "text", "content": "Arriba y arriba creció la plantita, volviéndose más alta cada día. Estiró sus hojas hacia el sol calentito."},
                {"type": "text", "content": "La lluvia vino para darle agua. El sol le dio energía. La planta se hizo más y más fuerte."},
                {"type": "illustration", "desc": "planta_creciendo"},
                {"type": "text", "content": "Por fin, la planta era grande y fuerte. Su tallo era alto. Sus hojas eran anchas."},
                {"type": "text", "content": "Y entonces, en una mañana brillante y soleada... ¡la planta abrió sus pétalos de par en par y mostró al mundo su hermosa flor!"},
                {"type": "vocab", "word": "florecer", "definition": "Cuando una flor se abre", "example": "Esperamos toda la primavera a que los tulipanes florecieran."},
                {"type": "illustration", "desc": "hermosa_flor"},
                {"type": "text", "content": "La semillita valiente se había convertido en la flor más hermosa de todo el jardín."},
                {"type": "text", "content": "Y todo porque fue lo suficientemente valiente para rodar, lo suficientemente paciente para esperar, y lo suficientemente fuerte para crecer."},
                {"type": "text", "content": "Fin."},
                {"type": "back_matter"},
            ]
        },
    }
}

# Merge expanded story libraries
STORY_LIBRARY["en"].update(ADDITIONAL_STORIES_EN)
STORY_LIBRARY["es"].update(ADDITIONAL_STORIES_ES)

class KDPPublishingMachine:
    """Professional KDP book generator with Amazon best practices"""
    
    def __init__(self, story_key, lang="en", size="8x10", output_dir="output"):
        self.story = STORY_LIBRARY[lang][story_key]
        self.lang = lang
        self.size_key = size
        self.size = KDP_SIZES[size]
        self.age = AGE_GROUPS[self.story["age"]]
        self.palette = PALETTES[self.story["palette"]]
        self.output_dir = output_dir
        
        # Calculate dimensions with bleed if needed
        self.bleed = self.size["bleed"]
        self.page_width = self.size["width"] + (2 * self.bleed)
        self.page_height = self.size["height"] + (2 * self.bleed)
        
        # Margins inside trim
        self.margin = {
            "outer": 0.5 * inch,
            "inner": 0.75 * inch,  # Gutter for binding
            "top": 0.75 * inch,
            "bottom": 0.75 * inch
        }
        
        os.makedirs(output_dir, exist_ok=True)
        
    def generate(self):
        """Generate the complete KDP-ready PDF"""
        filename = f"{self.output_dir}/{self.story['title'].replace(' ', '_')}_{self.size_key}.pdf"
        
        self.c = canvas.Canvas(filename, pagesize=(self.page_width, self.page_height))
        self.c.setAuthor("KDP Publishing Machine")
        self.c.setTitle(self.story["title"])
        self.c.setSubject(self.story["description"])
        self.c.setKeywords(", ".join(self.story["keywords"]))
        
        page_count = 0
        for chapter in self.story["chapters"]:
            if page_count > 0:
                self.c.showPage()
            
            if chapter["type"] == "copyright":
                self.draw_copyright_page()
            elif chapter["type"] == "dedication":
                self.draw_dedication_page(chapter.get("text", ""))
            elif chapter["type"] == "title_page":
                self.draw_title_page()
            elif chapter["type"] == "text":
                self.draw_text_page(chapter["content"])
            elif chapter["type"] == "vocab":
                self.draw_vocab_page(chapter["word"], chapter["definition"], chapter.get("example", ""))
            elif chapter["type"] == "illustration":
                self.draw_illustration_page(chapter["desc"])
            elif chapter["type"] == "back_matter":
                self.draw_back_matter()
            
            page_count += 1
        
        self.c.save()
        
        # Generate metadata JSON for KDP upload
        self.generate_metadata()
        
        print(f"✅ Generated: {filename}")
        print(f"   Size: {self.size_key} ({self.size['width']/inch}\" x {self.size['height']/inch}\")")
        print(f"   Pages: {page_count}")
        print(f"   Age: {self.story['age']}")
        print(f"   Language: {self.lang.upper()}")
        
        return filename
    
    def draw_copyright_page(self):
        """Professional copyright page"""
        y = self.page_height - 2*inch
        
        # Copyright text
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(HexColor("#4a5568"))
        
        lines = [
            f"{self.story['title']}",
            f"{self.story['subtitle']}",
            "",
            f"© {datetime.now().year} KDP Publishing Machine",
            "All rights reserved.",
            "",
            "No part of this publication may be reproduced, distributed, or transmitted",
            "in any form or by any means without the prior written permission of the publisher.",
            "",
            f"ISBN: [To be assigned by KDP]",
            f"Library of Congress Control Number: [Apply if needed]",
            "",
            "First Edition",
            "",
            "Printed in the United States of America",
            "",
            "For information about permission to reproduce selections from this book,",
            "write to: permissions@kdppublishing.example.com",
        ]
        
        for line in lines:
            self.c.drawString(self.margin["inner"], y, line)
            y -= 14
    
    def draw_dedication_page(self, text):
        """Elegant dedication page"""
        self.c.setFont("Helvetica-Oblique", 14)
        self.c.setFillColor(HexColor(self.palette["text"]))
        
        # Center the dedication
        text_width = self.c.stringWidth(text, "Helvetica-Oblique", 14)
        x = (self.page_width - text_width) / 2
        y = self.page_height / 2
        
        self.c.drawString(x, y, text)
    
    def draw_title_page(self):
        """Professional title page with series info"""
        # Series name (if part of series)
        if self.story.get("series"):
            self.c.setFont("Helvetica", 12)
            self.c.setFillColor(HexColor(self.palette["primary"]))
            series_text = f"{self.story['series']} • Book {self.story['book_number']}"
            text_width = self.c.stringWidth(series_text, "Helvetica", 12)
            self.c.drawString((self.page_width - text_width) / 2, self.page_height - 2.5*inch, series_text)
        
        # Main title
        self.c.setFont("Helvetica-Bold", 36)
        self.c.setFillColor(HexColor(self.palette["text"]))
        title = self.story["title"]
        text_width = self.c.stringWidth(title, "Helvetica-Bold", 36)
        self.c.drawString((self.page_width - text_width) / 2, self.page_height - 3.5*inch, title)
        
        # Subtitle
        self.c.setFont("Helvetica", 18)
        self.c.setFillColor(HexColor(self.palette["primary"]))
        subtitle = self.story["subtitle"]
        text_width = self.c.stringWidth(subtitle, "Helvetica", 18)
        self.c.drawString((self.page_width - text_width) / 2, self.page_height - 4.2*inch, subtitle)
        
        # Decorative element
        self.c.setStrokeColor(HexColor(self.palette["secondary"]))
        self.c.setLineWidth(2)
        line_y = self.page_height - 4.8*inch
        self.c.line(2*inch, line_y, self.page_width - 2*inch, line_y)
    
    def draw_text_page(self, content):
        """Story text page with proper typography"""
        self.c.setFont("Helvetica", self.age["font_size"])
        self.c.setFillColor(HexColor(self.palette["text"]))
        
        # Text area
        text_width = self.page_width - self.margin["inner"] - self.margin["outer"]
        
        # Simple text wrapping
        words = content.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = " ".join(current_line + [word])
            if self.c.stringWidth(test_line, "Helvetica", self.age["font_size"]) < text_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        y = self.page_height - self.margin["top"] - 0.5*inch
        for line in lines:
            self.c.drawString(self.margin["inner"], y, line)
            y -= self.age["line_spacing"]
    
    def draw_vocab_page(self, word, definition, example):
        """Vocabulary learning page"""
        # Background box
        box_margin = 0.75 * inch
        box_top = self.page_height - 2*inch
        box_height = 3 * inch
        
        self.c.setFillColor(HexColor(self.palette["secondary"]))
        self.c.roundRect(box_margin, box_top - box_height, 
                        self.page_width - 2*box_margin, box_height, 
                        15, fill=1, stroke=0)
        
        # Word
        self.c.setFont("Helvetica-Bold", 32)
        self.c.setFillColor(HexColor(self.palette["primary"]))
        text_width = self.c.stringWidth(word.upper(), "Helvetica-Bold", 32)
        self.c.drawString((self.page_width - text_width) / 2, box_top - 0.8*inch, word.upper())
        
        # Definition
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(HexColor(self.palette["text"]))
        y = box_top - 1.5*inch
        for line in textwrap.wrap(definition, 40):
            text_width = self.c.stringWidth(line, "Helvetica", 14)
            self.c.drawString((self.page_width - text_width) / 2, y, line)
            y -= 20
        
        # Example
        if example:
            self.c.setFont("Helvetica-Oblique", 12)
            self.c.setFillColor(HexColor("#718096"))
            example_text = f'"{example}"'
            y -= 10
            for line in textwrap.wrap(example_text, 45):
                text_width = self.c.stringWidth(line, "Helvetica-Oblique", 12)
                self.c.drawString((self.page_width - text_width) / 2, y, line)
                y -= 18
    
    def draw_illustration_page(self, desc):
        """Full-page illustration placeholder"""
        # Draw placeholder box
        img_margin = 0.5 * inch
        img_width = self.page_width - 2*img_margin
        img_height = self.page_height - 2*img_margin
        
        self.c.setFillColor(HexColor(self.palette["accent"]))
        self.c.roundRect(img_margin, img_margin, img_width, img_height, 20, fill=1, stroke=0)
        
        # Placeholder text
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(HexColor(self.palette["text"]))
        placeholder = f"[Illustration: {desc}]"
        text_width = self.c.stringWidth(placeholder, "Helvetica", 14)
        self.c.drawString((self.page_width - text_width) / 2, self.page_height / 2, placeholder)
        
        self.c.setFont("Helvetica", 10)
        note = "Insert 300 DPI image at 100% size"
        text_width = self.c.stringWidth(note, "Helvetica", 10)
        self.c.drawString((self.page_width - text_width) / 2, self.page_height / 2 - 20, note)
    
    def draw_back_matter(self):
        """Back cover matter - about the series"""
        if self.story.get("series"):
            self.c.setFont("Helvetica-Bold", 16)
            self.c.setFillColor(HexColor(self.palette["primary"]))
            text = f"Also in the {self.story['series']} series:"
            self.c.drawString(self.margin["inner"], self.page_height - 3*inch, text)
            
            self.c.setFont("Helvetica", 12)
            self.c.setFillColor(HexColor(self.palette["text"]))
            self.c.drawString(self.margin["inner"], self.page_height - 3.5*inch, 
                            "Book 2: Coming Soon!")
    
    def generate_metadata(self):
        """Generate KDP upload metadata JSON"""
        metadata = {
            "title": self.story["title"],
            "subtitle": self.story["subtitle"],
            "series": self.story.get("series", ""),
            "volume": self.story.get("book_number", 1),
            "description": self.story["description"],
            "keywords": self.story["keywords"],
            "categories": ["Juvenile Fiction / Concepts / Words", 
                          "Juvenile Fiction / Animals / General",
                          "Juvenile Fiction / Social Themes / Self-Esteem"],
            "age_range": self.story["age"],
            "language": self.lang,
            "trim_size": self.size_key,
            "page_count": len(self.story["chapters"]),
            "color": "interior_bw",  # Change to "interior_color" for color books
            "paper": "white",
            "bleed": "yes" if self.bleed > 0 else "no",
            "suggested_price": {
                "US": 9.99,
                "UK": 7.99,
                "EU": 8.99
            }
        }
        
        meta_file = f"{self.output_dir}/{self.story['title'].replace(' ', '_')}_metadata.json"
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   Metadata: {meta_file}")


def batch_generate(lang="en", count=5):
    """Generate multiple books in a series"""
    stories = list(STORY_LIBRARY[lang].keys())[:count]
    
    print(f"\n{'='*60}")
    print(f"BATCH GENERATION: {lang.upper()} | {count} books")
    print('='*60)
    
    for story_key in stories:
        print()
        machine = KDPPublishingMachine(story_key, lang=lang, size="8x10")
        machine.generate()
    
    print(f"\n{'='*60}")
    print("BATCH COMPLETE")
    print('='*60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        lang = sys.argv[2] if len(sys.argv) > 2 else "en"
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        batch_generate(lang, count)
    else:
        # Generate single book
        story = sys.argv[1] if len(sys.argv) > 1 else "brave_seed"
        lang = sys.argv[2] if len(sys.argv) > 2 else "en"
        size = sys.argv[3] if len(sys.argv) > 3 else "8x10"
        
        machine = KDPPublishingMachine(story, lang=lang, size=size)
        machine.generate()
