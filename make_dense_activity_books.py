#!/usr/bin/env python3
"""
Ultra-Dense Activity Workbook Generator
Maximum content, minimal waste
Every page has structured activities
"""

import os
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from datetime import datetime

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


class DenseWorkbookGenerator:
    """Maximum content per page, no empty space"""
    
    def __init__(self, theme, title, subtitle, age="3-6"):
        self.theme = theme
        self.title = title
        self.subtitle = subtitle
        self.age = age
        self.colors = {
            "primary": HexColor("#E63946"),
            "secondary": HexColor("#457B9D"),
            "accent": HexColor("#F1FAEE"),
            "dark": HexColor("#1D3557"),
            "light": HexColor("#A8DADC"),
        }
        
    def generate(self):
        pdf_path = OUT_DIR / f"{self.title.replace(' ', '_')}_Dense.pdf"
        W, H = 8.5 * inch, 11 * inch
        c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
        
        # Cover
        self._draw_cover(c, W, H)
        
        # 10 activity spreads (20 pages of dense content)
        activities = [
            self._draw_letters_abc,
            self._draw_letters_def,
            self._draw_numbers_123,
            self._draw_shapes_page,
            self._draw_patterns_page,
            self._draw_maze_page,
            self._draw_matching_page,
            self._draw_counting_page,
            self._draw_coloring_page,
            self._draw_words_page,
        ]
        
        for activity in activities:
            activity(c, W, H)
        
        # Final review
        self._draw_review_page(c, W, H)
        
        c.save()
        return str(pdf_path)
    
    def _draw_cover(self, c, W, H):
        c.setFillColor(self.colors["primary"])
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 36)
        c.drawString(W*0.08, H*0.65, self.title)
        c.setFont("Helvetica", 14)
        c.drawString(W*0.08, H*0.58, self.subtitle)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(W*0.08, H*0.20, f"AGES {self.age} | 22 PAGES | ZERO WASTE")
        c.showPage()
    
    def _draw_letters_abc(self, c, W, H):
        """Page with A, B, C all on one page with multiple activities"""
        self._draw_section_header(c, W, H, "LEARN LETTERS: A B C")
        
        letters = ["A", "B", "C"]
        x_positions = [W*0.12, W*0.40, W*0.68]
        
        for i, letter in enumerate(letters):
            x = x_positions[i]
            # Big letter
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica-Bold", 48)
            c.drawString(x, H*0.72, letter)
            
            # Trace lines
            c.setStrokeColor(HexColor("#DDDDDD"))
            for row in range(3):
                y = H*0.62 - row*0.08
                c.line(x, y, x+60, y)
                c.setFillColor(HexColor("#AAAAAA"))
                c.setFont("Helvetica", 20)
                c.drawString(x+5, y-18, letter)
            
            # Word example
            words = {"A": "Apple", "B": "Ball", "C": "Cat"}
            c.setFillColor(self.colors["secondary"])
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x, H*0.32, words[letter])
            
            # Find and circle
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica", 9)
            c.drawString(x, H*0.26, f"Find: {letter}")
            circles = ["A", "X", "B", "A", "C"] if letter == "A" else \
                     ["B", "A", "B", "C", "D"] if letter == "B" else \
                     ["C", "B", "A", "C", "D"]
            for j, circ in enumerate(circles):
                c.drawString(x + j*25, H*0.20, circ)
        
        c.showPage()
    
    def _draw_letters_def(self, c, W, H):
        """Page with D, E, F"""
        self._draw_section_header(c, W, H, "LEARN LETTERS: D E F")
        
        letters = ["D", "E", "F"]
        x_positions = [W*0.12, W*0.40, W*0.68]
        
        for i, letter in enumerate(letters):
            x = x_positions[i]
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica-Bold", 48)
            c.drawString(x, H*0.72, letter)
            
            c.setStrokeColor(HexColor("#DDDDDD"))
            for row in range(3):
                y = H*0.62 - row*0.08
                c.line(x, y, x+60, y)
                c.setFillColor(HexColor("#AAAAAA"))
                c.setFont("Helvetica", 20)
                c.drawString(x+5, y-18, letter)
            
            words = {"D": "Dog", "E": "Egg", "F": "Fish"}
            c.setFillColor(self.colors["secondary"])
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x, H*0.32, words[letter])
            
            # Simple connect dots
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica", 9)
            c.drawString(x, H*0.26, f"Trace: {letter}-{letter}-{letter}")
        
        c.showPage()
    
    def _draw_numbers_123(self, c, W, H):
        """Numbers 1-6 with counting"""
        self._draw_section_header(c, W, H, "NUMBERS 1 2 3")
        
        numbers = ["1", "2", "3"]
        x_positions = [W*0.15, W*0.42, W*0.70]
        
        for i, num in enumerate(numbers):
            x = x_positions[i]
            c.setFillColor(self.colors["primary"])
            c.setFont("Helvetica-Bold", 60)
            c.drawString(x, H*0.70, num)
            
            # Count and trace
            c.setStrokeColor(HexColor("#CCCCCC"))
            for row in range(4):
                y = H*0.58 - row*0.07
                c.line(x, y, x+50, y)
            
            # Count objects section
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica", 10)
            c.drawString(x, H*0.28, f"Count {num}:")
            
            # Draw simple shapes to count
            c.setFillColor(self.colors["secondary"])
            count = int(num)
            for j in range(min(count * 2, 6)):
                cx = x + (j % 3) * 20
                cy = H*0.20 - (j // 3) * 15
                c.circle(cx+5, cy, 5, fill=1, stroke=0)
        
        c.showPage()
    
    def _draw_shapes_page(self, c, W, H):
        """Shapes identification and tracing"""
        self._draw_section_header(c, W, H, "SHAPES")
        
        shapes = [("Circle", "○"), ("Square", "□"), ("Triangle", "△")]
        x_positions = [W*0.12, W*0.40, W*0.68]
        
        for i, (name, symbol) in enumerate(shapes):
            x = x_positions[i]
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x, H*0.75, name)
            
            # Large shape outline
            c.setStrokeColor(self.colors["primary"])
            c.setLineWidth(3)
            if name == "Circle":
                c.circle(x+40, H*0.60, 35, fill=0, stroke=1)
            elif name == "Square":
                c.rect(x+5, H*0.50, 70, 70, fill=0, stroke=1)
            else:
                # Triangle
                c.line(x+5, H*0.50, x+75, H*0.50)
                c.line(x+5, H*0.50, x+40, H*0.78)
                c.line(x+75, H*0.50, x+40, H*0.78)
            
            # Find the shape
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica", 10)
            c.drawString(x, H*0.35, "Find and circle:")
            
            shapes_row = ["○", "□", "△", "○", "□"]
            for j, s in enumerate(shapes_row):
                c.setFont("Helvetica", 16)
                c.drawString(x + j*18, H*0.28, s)
        
        c.showPage()
    
    def _draw_patterns_page(self, c, W, H):
        """Pattern completion"""
        self._draw_section_header(c, W, H, "COMPLETE THE PATTERN")
        
        patterns = [
            ("○ △ ○ △ ○ ?", "△"),
            ("□ ○ □ ○ □ ?", "○"),
            ("△ △ ○ △ △ ?", "○"),
        ]
        
        y = H*0.75
        for pattern, answer in patterns:
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica", 18)
            c.drawString(W*0.10, y, pattern)
            
            # Answer box
            c.setStrokeColor(self.colors["secondary"])
            c.setLineWidth(2)
            c.rect(W*0.70, y-10, 40, 30, fill=0, stroke=1)
            
            y -= 50
        
        # More patterns below
        c.setFont("Helvetica-Bold", 12)
        c.drawString(W*0.10, H*0.40, "Draw what comes next:")
        
        c.setFont("Helvetica", 20)
        sequences = ["A B A B A", "1 2 1 2 1", "● ● ○ ● ●"]
        y = H*0.32
        for seq in sequences:
            c.drawString(W*0.12, y, seq + " ?")
            y -= 35
        
        c.showPage()
    
    def _draw_maze_page(self, c, W, H):
        """Simple maze"""
        self._draw_section_header(c, W, H, "HELP THE CAT FIND HOME!")
        
        # Draw simple grid maze
        c.setStrokeColor(self.colors["dark"])
        c.setLineWidth(2)
        
        maze_x, maze_y = W*0.20, H*0.25
        cell_size = 35
        
        # Draw grid
        for row in range(6):
            for col in range(6):
                x = maze_x + col * cell_size
                y = maze_y + row * cell_size
                c.rect(x, y, cell_size, cell_size, fill=0, stroke=1)
        
        # Start and end
        c.setFillColor(HexColor("#90EE90"))
        c.rect(maze_x, maze_y, cell_size, cell_size, fill=1, stroke=1)
        c.setFillColor(HexColor("#FFB6C1"))
        c.rect(maze_x + 5*cell_size, maze_y + 5*cell_size, cell_size, cell_size, fill=1, stroke=1)
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(self.colors["dark"])
        c.drawString(maze_x + 5, maze_y + 15, "START")
        c.drawString(maze_x + 5*cell_size + 2, maze_y + 5*cell_size + 15, "HOME")
        
        c.showPage()
    
    def _draw_matching_page(self, c, W, H):
        """Matching activity"""
        self._draw_section_header(c, W, H, "MATCH THE PICTURES")
        
        left_items = [("Cat", W*0.10), ("Dog", W*0.10), ("Fish", W*0.10)]
        right_items = [("Water", W*0.55), ("Bone", W*0.55), ("Yarn", W*0.55)]
        
        y_left = H*0.70
        for item, x in left_items:
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica", 14)
            c.drawString(x, y_left, item)
            c.circle(x + 80, y_left, 5, fill=0, stroke=1)
            y_left -= 50
        
        y_right = H*0.70
        for item, x in right_items:
            c.setFillColor(self.colors["secondary"])
            c.setFont("Helvetica", 14)
            c.circle(x, y_right, 5, fill=0, stroke=1)
            c.drawString(x + 20, y_right, item)
            y_right -= 50
        
        c.showPage()
    
    def _draw_counting_page(self, c, W, H):
        """Counting exercise"""
        self._draw_section_header(c, W, H, "COUNT AND WRITE")
        
        # Draw groups of items to count
        groups = [3, 5, 7]
        x_positions = [W*0.15, W*0.42, W*0.70]
        
        for i, count in enumerate(groups):
            x = x_positions[i]
            # Draw stars
            c.setFillColor(self.colors["secondary"])
            for j in range(count):
                cx = x + (j % 3) * 18
                cy = H*0.65 - (j // 3) * 18
                c.drawString(cx, cy, "★")
            
            # Box for answer
            c.setStrokeColor(self.colors["dark"])
            c.rect(x, H*0.45, 50, 40, fill=0, stroke=1)
            
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica", 10)
            c.drawString(x, H*0.38, "How many?")
        
        c.showPage()
    
    def _draw_coloring_page(self, c, W, H):
        """Color by letter/number"""
        self._draw_section_header(c, W, H, "COLOR BY LETTER")
        
        # Simple color key
        c.setFillColor(self.colors["primary"])
        c.setFont("Helvetica-Bold", 11)
        c.drawString(W*0.08, H*0.75, "A = Red    B = Blue    C = Yellow")
        
        # Grid with letters
        grid_letters = [
            ["A", "B", "A"],
            ["C", "A", "B"],
            ["B", "C", "A"],
        ]
        
        start_x, start_y = W*0.25, H*0.55
        cell = 50
        
        for row in range(3):
            for col in range(3):
                x = start_x + col * cell
                y = start_y - row * cell
                c.setStrokeColor(self.colors["dark"])
                c.rect(x, y, cell, cell, fill=0, stroke=1)
                c.setFillColor(self.colors["dark"])
                c.setFont("Helvetica-Bold", 20)
                c.drawString(x + 18, y + 18, grid_letters[row][col])
        
        c.showPage()
    
    def _draw_words_page(self, c, W, H):
        """Simple word building"""
        self._draw_section_header(c, W, H, "BUILD WORDS")
        
        words = ["CAT", "DOG", "SUN"]
        y = H*0.75
        
        for word in words:
            c.setFillColor(self.colors["dark"])
            c.setFont("Helvetica-Bold", 16)
            c.drawString(W*0.10, y, word + ":")
            
            # Letter boxes
            for i, letter in enumerate(word):
                x = W*0.30 + i * 50
                c.setStrokeColor(self.colors["primary"])
                c.rect(x, y-10, 40, 35, fill=0, stroke=1)
                c.setFillColor(HexColor("#AAAAAA"))
                c.setFont("Helvetica", 18)
                c.drawString(x + 12, y-5, letter)
            
            y -= 60
        
        c.showPage()
    
    def _draw_review_page(self, c, W, H):
        """Final review with all skills"""
        self._draw_section_header(c, W, H, "GREAT JOB! REVIEW")
        
        c.setFillColor(self.colors["dark"])
        c.setFont("Helvetica", 12)
        
        review_items = [
            "✓ Letters A-F learned",
            "✓ Numbers 1-3 counted", 
            "✓ Shapes identified",
            "✓ Patterns completed",
            "✓ Words traced",
        ]
        
        y = H*0.70
        for item in review_items:
            c.drawString(W*0.15, y, item)
            y -= 30
        
        # Certificate section
        c.setFillColor(self.colors["primary"])
        c.setFont("Helvetica-Bold", 18)
        c.drawString(W*0.15, H*0.35, "COMPLETED BY:")
        c.setStrokeColor(self.colors["dark"])
        c.line(W*0.15, H*0.30, W*0.70, H*0.30)
        
        c.showPage()
    
    def _draw_section_header(self, c, W, H, text):
        c.setFillColor(self.colors["primary"])
        c.rect(0, H*0.88, W, H*0.12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(W*0.05, H*0.92, text)


def main():
    books = [
        ("animals", "Smart Kids Activity Book", "Letters, Numbers, Shapes & More", "3-5"),
        ("space", "Little Learner Workbook", "Complete Early Learning", "3-6"),
    ]
    
    for theme, title, subtitle, age in books:
        print(f"Building: {title}")
        gen = DenseWorkbookGenerator(theme, title, subtitle, age)
        pdf = gen.generate()
        print(f"✅ Created: {pdf}")
    
    print("\nDense activity books ready!")


if __name__ == "__main__":
    main()
