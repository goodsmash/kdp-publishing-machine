#!/usr/bin/env python3
"""
Comprehensive Multi-Activity Book Generator
Combines coloring, tracing, puzzles, and learning in one book
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, gray
import os
import random

class ComprehensiveActivityBook:
    """Generate all-in-one activity books"""
    
    PAGE_WIDTH = 8.5 * inch
    PAGE_HEIGHT = 11 * inch
    MARGIN = 0.6 * inch
    
    THEMES = {
        "dinosaurs": {
            "title": "Dinosaur Activity Book for Kids",
            "subtitle": "Coloring, Tracing, Puzzles, and Fun Facts!",
            "creatures": ["T-Rex", "Triceratops", "Stegosaurus", "Velociraptor", "Brachiosaurus"],
            "facts": ["T-Rex had teeth the size of bananas!", "Some dinosaurs had feathers like birds."]
        },
        "space": {
            "title": "Space Activity Book for Kids",
            "subtitle": "Rockets, Planets, Astronauts, and Galaxy Fun!",
            "creatures": ["Astronaut", "Alien", "Rocket", "Robot"],
            "facts": ["The Sun is so big that 1 million Earths could fit inside!"]
        },
        "ocean": {
            "title": "Ocean Activity Book for Kids",
            "subtitle": "Sea Creatures, Mermaids, and Underwater Adventures!",
            "creatures": ["Dolphin", "Shark", "Whale", "Octopus", "Seahorse"],
            "facts": ["The blue whale is the largest animal ever to live!"]
        },
        "unicorns": {
            "title": "Unicorn and Rainbow Activity Book",
            "subtitle": "Magic, Fantasy, and Sparkly Fun!",
            "creatures": ["Unicorn", "Pegasus", "Fairy", "Mermaid"],
            "facts": ["Unicorns are said to be symbols of purity and grace."]
        },
        "construction": {
            "title": "Construction Vehicles Activity Book",
            "subtitle": "Trucks, Excavators, Bulldozers, and Building Fun!",
            "creatures": ["Dump Truck", "Excavator", "Bulldozer", "Crane"],
            "facts": ["The largest dump truck can carry 450 tons!"]
        }
    }
    
    def __init__(self, theme="dinosaurs"):
        self.theme_data = self.THEMES[theme]
        self.theme = theme
        self.page_num = 0
        os.makedirs("activity_books/output", exist_ok=True)
        
        self.colors = {
            "primary": HexColor("#4A90E2"),
            "secondary": HexColor("#7ED321"),
            "accent": HexColor("#F5A623"),
            "text": HexColor("#333333"),
            "light": HexColor("#F5F5F5"),
            "gray": HexColor("#CCCCCC")
        }
    
    def generate(self):
        """Generate complete activity book"""
        filename = f"activity_books/output/{self.theme}_activity_book.pdf"
        self.c = canvas.Canvas(filename, pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT))
        
        self.draw_title_page()
        self.draw_belongs_to_page()
        self.draw_contents_page()
        
        # Coloring pages
        self.draw_section_header("COLORING FUN", "Bring the pictures to life!")
        for creature in self.theme_data["creatures"]:
            self.draw_coloring_page(creature)
        
        # Tracing pages
        self.draw_section_header("TRACE AND DRAW", "Practice your pencil skills!")
        for creature in self.theme_data["creatures"][:4]:
            self.draw_tracing_page(creature)
        
        # Dot-to-dot
        self.draw_section_header("DOT-TO-DOT", "Connect the numbers!")
        for i in range(5):
            self.draw_dot_to_dot_page(i)
        
        # Mazes
        self.draw_section_header("AMAZING MAZES", "Find your way through!")
        for i in range(5):
            self.draw_maze_page(i)
        
        # Counting
        self.draw_section_header("COUNT AND LEARN", "Numbers are fun!")
        for i in range(1, 11):
            self.draw_counting_page(i)
        
        # Word Search
        self.draw_section_header("WORD SEARCH", "Find the hidden words!")
        for i in range(3):
            self.draw_word_search_page(i)
        
        # Fun Facts
        self.draw_section_header("DID YOU KNOW?", "Amazing facts!")
        for fact in self.theme_data["facts"]:
            self.draw_fact_page(fact)
        
        self.draw_certificate()
        
        self.c.save()
        print(f"✅ Activity Book Created: {filename}")
        print(f"   Pages: {self.page_num}")
        print(f"   Theme: {self.theme.title()}")
        return filename
    
    def new_page(self):
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(gray)
        self.c.drawString(self.PAGE_WIDTH - self.MARGIN - 30, 0.3*inch, str(self.page_num))
    
    def draw_title_page(self):
        self.new_page()
        self.c.setFillColor(self.colors["primary"])
        self.c.rect(0, self.PAGE_HEIGHT - 2.5*inch, self.PAGE_WIDTH, 2.5*inch, fill=1, stroke=0)
        
        self.c.setFont("Helvetica-Bold", 36)
        self.c.setFillColor(HexColor("#FFFFFF"))
        title_width = self.c.stringWidth(self.theme_data["title"], "Helvetica-Bold", 36)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - 1.5*inch, 
                         self.theme_data["title"])
        
        self.c.setFont("Helvetica", 18)
        self.c.setFillColor(self.colors["text"])
        subtitle_width = self.c.stringWidth(self.theme_data["subtitle"], "Helvetica", 18)
        self.c.drawString((self.PAGE_WIDTH - subtitle_width)/2, self.PAGE_HEIGHT - 3*inch,
                         self.theme_data["subtitle"])
        
        # Features
        features = ["🎨 Coloring", "✏️ Tracing", "🔢 Dot-to-Dot", "🌀 Mazes", 
                   "➕ Math", "🔍 Word Search", "💡 Facts"]
        y = 4*inch
        for i, feature in enumerate(features):
            self.c.setFont("Helvetica-Bold", 12)
            self.c.setFillColor(self.colors["accent"])
            self.c.drawString(self.MARGIN + (i % 2) * 3.5*inch, y - (i // 2) * 0.5*inch, feature)
        
        self.c.setFont("Helvetica-Bold", 16)
        self.c.setFillColor(self.colors["secondary"])
        self.c.drawString(self.MARGIN, 1.5*inch, "Ages 4-8 | Over 40 Activities!")
    
    def draw_section_header(self, title, subtitle):
        self.new_page()
        self.c.setFillColor(self.colors["primary"])
        self.c.roundRect(self.MARGIN - 0.2*inch, self.PAGE_HEIGHT/2 - 0.8*inch,
                        self.PAGE_WIDTH - 2*self.MARGIN + 0.4*inch, 1.6*inch,
                        20, fill=1, stroke=0)
        
        self.c.setFont("Helvetica-Bold", 32)
        self.c.setFillColor(HexColor("#FFFFFF"))
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 32)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT/2 + 0.2*inch, title)
        
        self.c.setFont("Helvetica", 16)
        self.c.setFillColor(self.colors["text"])
        subtitle_width = self.c.stringWidth(subtitle, "Helvetica", 16)
        self.c.drawString((self.PAGE_WIDTH - subtitle_width)/2, self.PAGE_HEIGHT/2 - 0.4*inch, subtitle)
    
    def draw_coloring_page(self, creature):
        self.new_page()
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Color the {creature}!")
        
        cx = self.PAGE_WIDTH / 2
        cy = self.PAGE_HEIGHT / 2 + 0.5*inch
        size = 2.5*inch
        
        self.c.setStrokeColor(black)
        self.c.setLineWidth(4)
        self.c.roundRect(cx - size*0.8, cy - size*0.7, size*1.6, size*1.4, size*0.3, fill=0, stroke=1)
        
        # Simple face
        self.c.circle(cx - size*0.3, cy + size*0.2, size*0.15, fill=0, stroke=1)
        self.c.circle(cx + size*0.3, cy + size*0.2, size*0.15, fill=0, stroke=1)
        self.c.arc(cx - size*0.3, cy - size*0.2, cx + size*0.3, cy + size*0.1, startAng=200, extent=140)
    
    def draw_tracing_page(self, creature):
        self.new_page()
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Trace the {creature}")
        
        cx = self.PAGE_WIDTH / 2
        cy = self.PAGE_HEIGHT / 2 + 1*inch
        size = 2*inch
        
        self.c.setDash(5, 5)
        self.c.setStrokeColor(gray)
        self.c.setLineWidth(6)
        self.c.roundRect(cx - size*0.8, cy - size*0.7, size*1.6, size*1.4, size*0.3, fill=0, stroke=1)
        self.c.setDash()
    
    def draw_dot_to_dot_page(self, index):
        self.new_page()
        creature = self.theme_data["creatures"][index % len(self.theme_data["creatures"])]
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Connect: {creature}")
        
        cx = self.PAGE_WIDTH / 2
        cy = self.PAGE_HEIGHT / 2
        
        dots = [(cx - 1.5*inch, cy + 1*inch, 1), (cx + 1.5*inch, cy + 1*inch, 2),
                (cx + 1.5*inch, cy - 1*inch, 3), (cx - 1.5*inch, cy - 1*inch, 4)]
        
        self.c.setFont("Helvetica-Bold", 14)
        for x, y, num in dots:
            self.c.setFillColor(self.colors["accent"])
            self.c.circle(x, y, 12, fill=1, stroke=0)
            self.c.setFillColor(HexColor("#FFFFFF"))
            num_width = self.c.stringWidth(str(num), "Helvetica-Bold", 14)
            self.c.drawString(x - num_width/2, y - 5, str(num))
    
    def draw_maze_page(self, index):
        self.new_page()
        titles = ["Find the Treasure!", "Help Get Home!", "Find the Way Out!", "Reach the Goal!", "Solve the Puzzle!"]
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, titles[index % len(titles)])
        
        maze_x = self.PAGE_WIDTH / 2 - 2*inch
        maze_y = self.PAGE_HEIGHT / 2 - 1.5*inch
        self.c.setStrokeColor(black)
        self.c.setLineWidth(3)
        self.c.rect(maze_x, maze_y, 4*inch, 4*inch, fill=0, stroke=1)
        
        self.c.setFont("Helvetica", 16)
        self.c.drawString(maze_x - 0.4*inch, maze_y + 0.1*inch, "🚀")
        self.c.drawString(maze_x + 4.1*inch, maze_y + 3.8*inch, "🏁")
    
    def draw_counting_page(self, number):
        self.new_page()
        self.c.setFont("Helvetica-Bold", 28)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Count to {number}")
        
        creature = self.theme_data["creatures"][number % len(self.theme_data["creatures"])]
        self.c.setFont("Helvetica", 40)
        for i in range(number):
            col = i % 5
            row = i // 5
            x = self.MARGIN + 1*inch + col * 1.2*inch
            y = self.PAGE_HEIGHT - self.MARGIN - 2*inch - row * 1*inch
            self.c.drawString(x, y, creature[0])
    
    def draw_word_search_page(self, index):
        self.new_page()
        words = self.theme_data["creatures"][:4]
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Word Search!")
        
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(gray)
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.4*inch,
                         f"Find: {', '.join([w[:6].upper() for w in words])}")
    
    def draw_fact_page(self, fact):
        self.new_page()
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        title = "Did You Know?"
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 24)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - self.MARGIN - 0.5*inch, title)
        
        self.c.setFillColor(HexColor("#FFF9E6"))
        self.c.roundRect(self.MARGIN, self.PAGE_HEIGHT/2 - 1*inch,
                        self.PAGE_WIDTH - 2*self.MARGIN, 2.5*inch, 15, fill=1, stroke=0)
        
        self.c.setFont("Helvetica-Bold", 18)
        self.c.setFillColor(self.colors["text"])
        self.c.drawString(self.MARGIN + 0.5*inch, self.PAGE_HEIGHT/2 + 0.5*inch, fact[:60])
    
    def draw_belongs_to_page(self):
        self.new_page()
        self.c.setFont("Helvetica-Bold", 28)
        self.c.setFillColor(self.colors["primary"])
        title = "This Book Belongs To:"
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 28)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - 2*inch, title)
        
        self.c.setStrokeColor(self.colors["primary"])
        self.c.setLineWidth(3)
        self.c.roundRect(self.MARGIN + 0.5*inch, self.PAGE_HEIGHT/2 - 0.5*inch,
                        self.PAGE_WIDTH - 2*self.MARGIN - 1*inch, 1.5*inch, 15, fill=0, stroke=1)
    
    def draw_contents_page(self):
        self.new_page()
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.3*inch, "What's Inside")
    
    def draw_certificate(self):
        self.new_page()
        self.c.setStrokeColor(self.colors["accent"])
        self.c.setLineWidth(4)
        self.c.rect(self.MARGIN, self.MARGIN, 
                   self.PAGE_WIDTH - 2*self.MARGIN, 
                   self.PAGE_HEIGHT - 2*self.MARGIN, fill=0, stroke=1)
        
        self.c.setFont("Helvetica-Bold", 36)
        self.c.setFillColor(self.colors["primary"])
        title = "Certificate of Completion"
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 36)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - self.MARGIN - 1.5*inch, title)


if __name__ == "__main__":
    import sys
    theme = sys.argv[1] if len(sys.argv) > 1 else "dinosaurs"
    
    print(f"Creating {theme} activity book...")
    book = ComprehensiveActivityBook(theme)
    book.generate()
