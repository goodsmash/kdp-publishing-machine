#!/usr/bin/env python3
"""
Learn-to-Write Workbook Generator
Creates educational workbooks with pen control, tracing, letters, numbers
Optimized for KDP printing (8.5x11" standard workbook size)
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, gray
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import textwrap

class WorkbookGenerator:
    """Generate educational workbooks for kids"""
    
    # Workbook specifications
    PAGE_WIDTH = 8.5 * inch  # Standard US Letter
    PAGE_HEIGHT = 11 * inch
    MARGIN = 0.75 * inch
    
    # Grade levels and content
    LEVELS = {
        "preschool": {"age": "3-5", "line_height": 0.6*inch, "font_size": 72, "guide": True},
        "kindergarten": {"age": "5-6", "line_height": 0.5*inch, "font_size": 60, "guide": True},
        "first_grade": {"age": "6-7", "line_height": 0.4*inch, "font_size": 48, "guide": False},
    }
    
    def __init__(self, title, subtitle, level="preschool", theme="animals"):
        self.title = title
        self.subtitle = subtitle
        self.level = self.LEVELS[level]
        self.theme = theme
        self.page_num = 0
        
        os.makedirs("workbooks/output", exist_ok=True)
        
        # Colors for different activities
        self.colors = {
            "primary": HexColor("#4A90E2"),
            "secondary": HexColor("#7ED321"),
            "accent": HexColor("#F5A623"),
            "text": HexColor("#333333"),
            "light_gray": HexColor("#E8E8E8"),
            "medium_gray": HexColor("#CCCCCC"),
            "trace": HexColor("#B8B8B8"),
        }
        
    def generate_workbook(self):
        """Generate complete workbook PDF"""
        filename = f"workbooks/output/{self.title.replace(' ', '_')}_Workbook.pdf"
        
        self.c = canvas.Canvas(filename, pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT))
        
        # Title page
        self.draw_title_page()
        
        # Instructions page
        self.draw_instructions_page()
        
        # Table of contents
        self.draw_table_of_contents()
        
        # Section 1: Pen Control (Lines)
        self.draw_section_header("Part 1: Pen Control", "Practice drawing straight and curvy lines!")
        self.draw_line_practice("straight", 4)
        self.draw_line_practice("curvy", 4)
        self.draw_line_practice("zigzag", 3)
        self.draw_line_practice("loops", 3)
        
        # Section 2: Shapes
        self.draw_section_header("Part 2: Shapes", "Trace the shapes!")
        shapes = ["circle", "square", "triangle", "star", "heart", "diamond"]
        for shape in shapes:
            self.draw_shape_page(shape)
        
        # Section 3: Uppercase Letters
        self.draw_section_header("Part 3: Uppercase Letters", "A to Z - Let's practice the ABCs!")
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.draw_letter_page(letter.upper())
        
        # Section 4: Lowercase Letters
        self.draw_section_header("Part 4: Lowercase Letters", "a to z - Practice makes perfect!")
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.draw_letter_page(letter.lower())
        
        # Section 5: Numbers
        self.draw_section_header("Part 5: Numbers", "Count and write 0 to 20!")
        for num in range(0, 21):
            self.draw_number_page(num)
        
        # Section 6: Words
        self.draw_section_header("Part 6: First Words", "Write your first words!")
        words = ["CAT", "DOG", "SUN", "MOON", "HAT", "BED", "TOY", "BALL"]
        for word in words:
            self.draw_word_page(word)
        
        # Section 7: Fun Activities
        self.draw_section_header("Part 7: Fun Activities", "Mazes and puzzles!")
        self.draw_maze_page()
        self.draw_matching_page()
        self.draw_coloring_page()
        
        # Certificate
        self.draw_certificate()
        
        self.c.save()
        print(f"✅ Workbook created: {filename}")
        print(f"   Pages: {self.page_num}")
        print(f"   Level: Preschool (Ages 3-5)")
        print(f"   Activities: Pen control, shapes, letters, numbers, words")
        return filename
    
    def new_page(self):
        """Start a new page"""
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        
        # Page number at bottom
        self.c.setFont("Helvetica", 10)
        self.c.setFillColor(self.colors["medium_gray"])
        self.c.drawString(self.PAGE_WIDTH - self.MARGIN - 20, 0.4*inch, str(self.page_num))
    
    def draw_title_page(self):
        """Colorful title page"""
        self.new_page()
        
        # Background color block at top
        self.c.setFillColor(self.colors["primary"])
        self.c.rect(0, self.PAGE_HEIGHT - 3*inch, self.PAGE_WIDTH, 3*inch, fill=1, stroke=0)
        
        # Title
        self.c.setFont("Helvetica-Bold", 42)
        self.c.setFillColor(HexColor("#FFFFFF"))
        
        # Center title
        title_width = self.c.stringWidth(self.title, "Helvetica-Bold", 42)
        x = (self.PAGE_WIDTH - title_width) / 2
        self.c.drawString(x, self.PAGE_HEIGHT - 1.8*inch, self.title)
        
        # Subtitle
        self.c.setFont("Helvetica", 20)
        self.c.setFillColor(HexColor("#333333"))
        subtitle_width = self.c.stringWidth(self.subtitle, "Helvetica", 20)
        x = (self.PAGE_WIDTH - subtitle_width) / 2
        self.c.drawString(x, self.PAGE_HEIGHT - 3.5*inch, self.subtitle)
        
        # Decorative elements
        self.c.setFillColor(self.colors["accent"])
        self.c.circle(self.PAGE_WIDTH/2, 4*inch, 0.5*inch, fill=1, stroke=0)
        self.c.setFillColor(self.colors["secondary"])
        self.c.circle(self.PAGE_WIDTH/2 - 1.5*inch, 4.5*inch, 0.3*inch, fill=1, stroke=0)
        self.c.circle(self.PAGE_WIDTH/2 + 1.5*inch, 4.5*inch, 0.3*inch, fill=1, stroke=0)
        
        # Features list
        features = [
            "✓ Pen Control Practice",
            "✓ Line Tracing",
            "✓ Letter Writing (A-Z)",
            "✓ Number Writing (0-20)",
            "✓ Fun Activities & Mazes"
        ]
        
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(self.colors["text"])
        y = 3*inch
        for feature in features:
            self.c.drawString(self.MARGIN + 0.5*inch, y, feature)
            y -= 0.35*inch
        
        # Age info
        self.c.setFont("Helvetica-Bold", 16)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, 1.2*inch, f"Ages {self.level['age']}")
    
    def draw_instructions_page(self):
        """How to use this workbook"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.3*inch, "How to Use This Workbook")
        
        # Draw line under title
        self.c.setStrokeColor(self.colors["primary"])
        self.c.setLineWidth(2)
        self.c.line(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.5*inch, 
                   self.PAGE_WIDTH - self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.5*inch)
        
        instructions = [
            ("1. Start with a pencil or crayon", 
             "Use a thick pencil or washable marker that's easy for little hands to hold."),
            ("2. Follow the dotted lines", 
             "Trace over the gray dotted lines to practice your strokes."),
            ("3. Use the practice lines", 
             "After tracing, try writing on the empty lines below."),
            ("4. Take your time", 
             "There's no rush! Practice a little bit each day."),
            ("5. Have fun!", 
             "Learning to write is an adventure. Enjoy the journey!")
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1*inch
        self.c.setFont("Helvetica-Bold", 14)
        for title, desc in instructions:
            self.c.setFillColor(self.colors["accent"])
            self.c.drawString(self.MARGIN, y, title)
            y -= 0.25*inch
            
            self.c.setFont("Helvetica", 12)
            self.c.setFillColor(self.colors["text"])
            wrapped = textwrap.wrap(desc, width=70)
            for line in wrapped:
                self.c.drawString(self.MARGIN + 0.2*inch, y, line)
                y -= 0.2*inch
            y -= 0.2*inch
            self.c.setFont("Helvetica-Bold", 14)
        
        # Tip box
        self.c.setFillColor(HexColor("#FFF8DC"))
        self.c.roundRect(self.MARGIN, 2*inch, self.PAGE_WIDTH - 2*self.MARGIN, 1.5*inch, 10, fill=1, stroke=0)
        
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setFillColor(self.colors["accent"])
        self.c.drawString(self.MARGIN + 0.3*inch, 3.2*inch, "💡 Parent Tip:")
        
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(self.colors["text"])
        tip = "Praise effort over perfection! Encourage your child to try their best."
        self.c.drawString(self.MARGIN + 0.3*inch, 2.8*inch, tip)
    
    def draw_table_of_contents(self):
        """Table of contents"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.3*inch, "What's Inside")
        
        sections = [
            ("Part 1: Pen Control", "Practice lines and curves", "4"),
            ("Part 2: Shapes", "Circles, squares, and more", "8"),
            ("Part 3: Uppercase Letters", "A B C D E F G...", "14"),
            ("Part 4: Lowercase Letters", "a b c d e f g...", "40"),
            ("Part 5: Numbers", "0 1 2 3 4 5 6...", "66"),
            ("Part 6: First Words", "Write simple words", "87"),
            ("Part 7: Fun Activities", "Mazes and puzzles", "95"),
            ("Certificate", "Celebrate your progress!", "98")
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1*inch
        for title, desc, page in sections:
            # Section box
            self.c.setFillColor(self.colors["light_gray"])
            self.c.roundRect(self.MARGIN, y - 0.15*inch, self.PAGE_WIDTH - 2*self.MARGIN, 0.5*inch, 5, fill=1, stroke=0)
            
            self.c.setFont("Helvetica-Bold", 13)
            self.c.setFillColor(self.colors["text"])
            self.c.drawString(self.MARGIN + 0.2*inch, y, title)
            
            self.c.setFont("Helvetica", 11)
            self.c.setFillColor(gray)
            self.c.drawString(self.MARGIN + 0.2*inch, y - 0.2*inch, desc)
            
            self.c.setFont("Helvetica-Bold", 13)
            self.c.setFillColor(self.colors["primary"])
            page_x = self.PAGE_WIDTH - self.MARGIN - 0.5*inch
            self.c.drawString(page_x, y - 0.1*inch, f"p.{page}")
            
            y -= 0.7*inch
    
    def draw_section_header(self, title, subtitle):
        """Section divider page"""
        self.new_page()
        
        # Large colored block
        self.c.setFillColor(self.colors["primary"])
        self.c.rect(self.MARGIN - 0.25*inch, self.PAGE_HEIGHT/2 - 1*inch, 
                   self.PAGE_WIDTH - 2*self.MARGIN + 0.5*inch, 2*inch, 
                   fill=1, stroke=0)
        
        # Title
        self.c.setFont("Helvetica-Bold", 32)
        self.c.setFillColor(HexColor("#FFFFFF"))
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 32)
        x = (self.PAGE_WIDTH - title_width) / 2
        self.c.drawString(x, self.PAGE_HEIGHT/2 + 0.3*inch, title)
        
        # Subtitle
        self.c.setFont("Helvetica", 16)
        self.c.setFillColor(self.colors["text"])
        subtitle_width = self.c.stringWidth(subtitle, "Helvetica", 16)
        x = (self.PAGE_WIDTH - subtitle_width) / 2
        self.c.drawString(x, self.PAGE_HEIGHT/2 - 0.5*inch, subtitle)
    
    def draw_line_practice(self, line_type, count):
        """Practice tracing lines"""
        for _ in range(count):
            self.new_page()
            
            # Title
            line_names = {
                "straight": "Straight Lines",
                "curvy": "Curvy Lines", 
                "zigzag": "Zigzag Lines",
                "loops": "Loops and Circles"
            }
            
            self.c.setFont("Helvetica-Bold", 20)
            self.c.setFillColor(self.colors["primary"])
            self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, line_names.get(line_type, "Practice Lines"))
            
            # Draw tracing lines
            start_y = self.PAGE_HEIGHT - self.MARGIN - 1*inch
            for i in range(5):
                y = start_y - i * 1.2*inch
                self.draw_tracing_line(line_type, self.MARGIN + 0.5*inch, y, self.PAGE_WIDTH - self.MARGIN - 0.5*inch)
    
    def draw_tracing_line(self, line_type, x1, y, x2):
        """Draw a tracing line based on type"""
        width = x2 - x1
        
        if line_type == "straight":
            # Dotted straight line
            self.draw_dotted_line(x1, y, x2, y)
            
        elif line_type == "curvy":
            # Wavy line
            self.c.setDash(3, 3)
            self.c.setStrokeColor(self.colors["trace"])
            self.c.setLineWidth(3)
            
            path = self.c.beginPath()
            path.moveTo(x1, y)
            for i in range(10):
                x = x1 + (width * (i + 1) / 10)
                offset = 0.2*inch if i % 2 == 0 else -0.2*inch
                path.lineTo(x - width/20, y + offset)
            path.lineTo(x2, y)
            self.c.drawPath(path, stroke=1, fill=0)
            self.c.setDash()
            
        elif line_type == "zigzag":
            # Zigzag line
            self.c.setDash(3, 3)
            self.c.setStrokeColor(self.colors["trace"])
            self.c.setLineWidth(3)
            
            path = self.c.beginPath()
            path.moveTo(x1, y)
            for i in range(8):
                x = x1 + (width * (i + 1) / 8)
                y_offset = 0.25*inch if i % 2 == 0 else -0.25*inch
                path.lineTo(x - width/16, y + y_offset)
            path.lineTo(x2, y)
            self.c.drawPath(path, stroke=1, fill=0)
            self.c.setDash()
            
        elif line_type == "loops":
            # Loops
            self.c.setDash(3, 3)
            self.c.setStrokeColor(self.colors["trace"])
            self.c.setLineWidth(3)
            
            for i in range(6):
                cx = x1 + (width * (i + 0.5) / 6)
                self.c.circle(cx, y, 0.25*inch, fill=0, stroke=1)
            self.c.setDash()
        
        # Start and end dots
        self.c.setFillColor(self.colors["accent"])
        self.c.circle(x1, y, 4, fill=1, stroke=0)
        self.c.circle(x2, y, 4, fill=1, stroke=0)
    
    def draw_dotted_line(self, x1, y, x2, y2):
        """Draw a dotted line for tracing"""
        self.c.setDash(4, 4)
        self.c.setStrokeColor(self.colors["trace"])
        self.c.setLineWidth(3)
        self.c.line(x1, y, x2, y2)
        self.c.setDash()
    
    def draw_shape_page(self, shape):
        """Trace a shape"""
        self.new_page()
        
        # Title
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Trace the {shape.title()}")
        
        # Large shape in center for tracing
        cx = self.PAGE_WIDTH / 2
        cy = self.PAGE_HEIGHT / 2
        size = 2*inch
        
        self.c.setDash(4, 4)
        self.c.setStrokeColor(self.colors["trace"])
        self.c.setLineWidth(6)
        
        if shape == "circle":
            self.c.circle(cx, cy, size, fill=0, stroke=1)
        elif shape == "square":
            self.c.rect(cx - size, cy - size, size*2, size*2, fill=0, stroke=1)
        elif shape == "triangle":
            self.draw_triangle(cx, cy, size)
        elif shape == "star":
            self.draw_star(cx, cy, size)
        elif shape == "heart":
            self.draw_heart(cx, cy, size)
        elif shape == "diamond":
            self.draw_diamond(cx, cy, size)
        
        self.c.setDash()
        
        # Practice shapes below
        y = self.MARGIN + 1.5*inch
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(gray)
        self.c.drawString(self.MARGIN, y + 0.5*inch, "Practice drawing the shape yourself:")
        
        for i in range(3):
            x = self.MARGIN + i * 2.5*inch + 1*inch
            self.c.setStrokeColor(self.colors["light_gray"])
            self.c.setLineWidth(2)
            if shape == "circle":
                self.c.circle(x, y, 0.4*inch, fill=0, stroke=1)
            elif shape == "square":
                self.c.rect(x - 0.4*inch, y - 0.4*inch, 0.8*inch, 0.8*inch, fill=0, stroke=1)
    
    def draw_triangle(self, cx, cy, size):
        """Draw triangle path"""
        path = self.c.beginPath()
        path.moveTo(cx, cy + size)
        path.lineTo(cx - size*0.866, cy - size*0.5)
        path.lineTo(cx + size*0.866, cy - size*0.5)
        path.close()
        self.c.drawPath(path, stroke=1, fill=0)
    
    def draw_star(self, cx, cy, size):
        """Draw star shape"""
        import math
        path = self.c.beginPath()
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = size if i % 2 == 0 else size * 0.4
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.close()
        self.c.drawPath(path, stroke=1, fill=0)
    
    def draw_heart(self, cx, cy, size):
        """Simplified heart - circle approximation"""
        self.c.circle(cx - size*0.4, cy + size*0.2, size*0.5, fill=0, stroke=1)
        self.c.circle(cx + size*0.4, cy + size*0.2, size*0.5, fill=0, stroke=1)
        # Bottom point
        self.draw_triangle(cx, cy - size*0.3, size*0.6)
    
    def draw_diamond(self, cx, cy, size):
        """Draw diamond/rhombus"""
        path = self.c.beginPath()
        path.moveTo(cx, cy + size)
        path.lineTo(cx + size*0.6, cy)
        path.lineTo(cx, cy - size)
        path.lineTo(cx - size*0.6, cy)
        path.close()
        self.c.drawPath(path, stroke=1, fill=0)
    
    def draw_letter_page(self, letter):
        """Letter tracing page"""
        self.new_page()
        
        # Title
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Practice the Letter '{letter}'")
        
        # Large letter for tracing (top)
        y_large = self.PAGE_HEIGHT - self.MARGIN - 1.5*inch
        
        # Draw letter guidelines (gray)
        self.draw_guidelines(y_large)
        
        # Large traceable letter
        self.c.setFont("Helvetica-Bold", 120)
        self.c.setFillColor(self.colors["trace"])
        self.c.setDash(3, 3)
        char_width = self.c.stringWidth(letter, "Helvetica-Bold", 120)
        self.c.drawString((self.PAGE_WIDTH - char_width)/2, y_large - 0.3*inch, letter)
        self.c.setDash()
        
        # Practice letters (3 lines)
        y_start = self.PAGE_HEIGHT - self.MARGIN - 3*inch
        for row in range(3):
            y = y_start - row * 1.8*inch
            self.draw_guidelines(y)
            
            # Dotted letters to trace
            for col in range(4):
                x = self.MARGIN + 0.5*inch + col * 1.8*inch
                if row < 2 or col < 2:  # Last row has fewer trace letters
                    self.c.setFont("Helvetica-Bold", 72)
                    self.c.setFillColor(self.colors["trace"])
                    self.c.setDash(2, 3)
                    self.c.drawString(x, y - 0.2*inch, letter)
                    self.c.setDash()
    
    def draw_guidelines(self, y):
        """Draw handwriting guide lines"""
        line_color = self.colors["light_gray"]
        
        # Top line (solid)
        self.c.setStrokeColor(line_color)
        self.c.setLineWidth(1)
        self.c.line(self.MARGIN, y + 0.5*inch, self.PAGE_WIDTH - self.MARGIN, y + 0.5*inch)
        
        # Middle dashed line
        self.c.setDash(4, 4)
        self.c.line(self.MARGIN, y, self.PAGE_WIDTH - self.MARGIN, y)
        self.c.setDash()
        
        # Bottom line (solid)
        self.c.line(self.MARGIN, y - 0.5*inch, self.PAGE_WIDTH - self.MARGIN, y - 0.5*inch)
    
    def draw_number_page(self, num):
        """Number tracing page"""
        self.new_page()
        
        # Title
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Practice the Number {num}")
        
        # Large number
        y = self.PAGE_HEIGHT - self.MARGIN - 2*inch
        self.c.setFont("Helvetica-Bold", 150)
        self.c.setFillColor(self.colors["trace"])
        self.c.setDash(3, 3)
        num_str = str(num)
        num_width = self.c.stringWidth(num_str, "Helvetica-Bold", 150)
        self.c.drawString((self.PAGE_WIDTH - num_width)/2, y, num_str)
        self.c.setDash()
        
        # Counting objects
        y = self.PAGE_HEIGHT - self.MARGIN - 3.5*inch
        self.draw_counting_objects(num, self.MARGIN + 1*inch, y)
        
        # Practice numbers
        y = self.MARGIN + 2*inch
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(gray)
        self.c.drawString(self.MARGIN, y + 0.8*inch, "Trace and write the number:")
        
        for i in range(3):
            x = self.MARGIN + 0.5*inch + i * 2*inch
            self.c.setFont("Helvetica-Bold", 80)
            self.c.setFillColor(self.colors["trace"])
            self.c.setDash(2, 3)
            self.c.drawString(x, y, num_str)
            self.c.setDash()
    
    def draw_counting_objects(self, count, x, y):
        """Draw objects to count"""
        self.c.setFillColor(self.colors["accent"])
        
        # Draw circles to count
        cols = min(count, 10)
        rows = (count + 9) // 10
        
        for i in range(count):
            row = i // 10
            col = i % 10
            cx = x + col * 0.5*inch
            cy = y - row * 0.5*inch
            self.c.circle(cx, cy, 8, fill=1, stroke=0)
    
    def draw_word_page(self, word):
        """Word tracing page"""
        self.new_page()
        
        # Title
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Write the Word")
        
        # Large word with guidelines
        y = self.PAGE_HEIGHT - self.MARGIN - 1.5*inch
        self.draw_guidelines(y)
        
        self.c.setFont("Helvetica-Bold", 72)
        self.c.setFillColor(self.colors["trace"])
        self.c.setDash(3, 3)
        word_width = self.c.stringWidth(word, "Helvetica-Bold", 72)
        self.c.drawString((self.PAGE_WIDTH - word_width)/2, y - 0.15*inch, word)
        self.c.setDash()
        
        # Picture hint (simple description)
        y = self.PAGE_HEIGHT - self.MARGIN - 3*inch
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(self.colors["secondary"])
        self.c.drawString(self.MARGIN, y, f"💡 Hint: Draw a picture of a {word.lower()}!")
        
        # Practice lines
        y = self.MARGIN + 2*inch
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(gray)
        self.c.drawString(self.MARGIN, y + 0.8*inch, "Practice writing the word:")
        
        for i in range(3):
            self.draw_guidelines(y - i * 1.2*inch)
            if i < 2:
                self.c.setFont("Helvetica-Bold", 48)
                self.c.setFillColor(self.colors["trace"])
                self.c.setDash(2, 3)
                word_width = self.c.stringWidth(word, "Helvetica-Bold", 48)
                self.c.drawString((self.PAGE_WIDTH - word_width)/2, y - i * 1.2*inch - 0.1*inch, word)
                self.c.setDash()
    
    def draw_maze_page(self):
        """Simple maze activity"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Help the Bee Find the Flower!")
        
        # Simple maze drawing
        maze_x = self.PAGE_WIDTH / 2 - 2*inch
        maze_y = self.PAGE_HEIGHT / 2 - 1*inch
        cell_size = 0.5*inch
        
        # Draw grid
        self.c.setStrokeColor(self.colors["light_gray"])
        self.c.setLineWidth(2)
        
        # Simple maze walls
        walls = [
            # Outer border
            (0, 0, 4, 0), (4, 0, 4, 4), (4, 4, 0, 4), (0, 4, 0, 0),
            # Inner walls
            (1, 0, 1, 2), (2, 1, 2, 3), (3, 2, 3, 4), (1, 3, 3, 3)
        ]
        
        for x1, y1, x2, y2 in walls:
            self.c.line(maze_x + x1*cell_size, maze_y + y1*cell_size,
                       maze_x + x2*cell_size, maze_y + y2*cell_size)
        
        # Start (bee) and end (flower)
        self.c.setFont("Helvetica", 20)
        self.c.drawString(maze_x - 0.3*inch, maze_y + 0.1*inch, "🐝")
        self.c.drawString(maze_x + 3.7*inch, maze_y + 3.7*inch, "🌸")
    
    def draw_matching_page(self):
        """Matching activity"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Match the Animals!")
        
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(gray)
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.5*inch, 
                         "Draw a line from each animal to its home.")
        
        # Animals on left
        animals = [("🐶", "Dog"), ("🐟", "Fish"), ("🐦", "Bird"), ("🐰", "Rabbit")]
        # Homes on right
        homes = [("🏠", "House"), ("🌊", "Water"), ("🌳", "Tree"), ("🕳️", "Burrow")]
        
        y_start = self.PAGE_HEIGHT - self.MARGIN - 1.5*inch
        
        # Draw animals
        for i, (emoji, name) in enumerate(animals):
            y = y_start - i * 1.5*inch
            self.c.setFont("Helvetica", 30)
            self.c.drawString(self.MARGIN + 0.5*inch, y, emoji)
            self.c.setFont("Helvetica", 14)
            self.c.drawString(self.MARGIN + 1.2*inch, y + 0.1*inch, name)
            # Circle
            self.c.setStrokeColor(self.colors["light_gray"])
            self.c.circle(self.MARGIN + 0.8*inch, y + 0.15*inch, 0.4*inch, fill=0, stroke=1)
        
        # Draw homes
        for i, (emoji, name) in enumerate(homes):
            y = y_start - i * 1.5*inch
            self.c.setFont("Helvetica", 30)
            self.c.drawString(self.PAGE_WIDTH - self.MARGIN - 2*inch, y, emoji)
            self.c.setFont("Helvetica", 14)
            self.c.drawString(self.PAGE_WIDTH - self.MARGIN - 1.3*inch, y + 0.1*inch, name)
            # Circle
            self.c.setStrokeColor(self.colors["light_gray"])
            self.c.circle(self.PAGE_WIDTH - self.MARGIN - 1.5*inch, y + 0.15*inch, 0.4*inch, fill=0, stroke=1)
    
    def draw_coloring_page(self):
        """Coloring activity page"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Color the Rainbow!")
        
        # Simple rainbow outline
        cx = self.PAGE_WIDTH / 2
        cy = self.PAGE_HEIGHT / 2 + 0.5*inch
        
        colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]
        
        self.c.setLineWidth(8)
        for i, color in enumerate(colors):
            radius = 2*inch - i * 0.25*inch
            self.c.setStrokeColor(HexColor(color))
            # Draw arc (semicircle)
            import math
            path = self.c.beginPath()
            for angle in range(0, 181, 5):
                rad = math.radians(angle)
                x = cx + radius * math.cos(rad)
                y = cy + radius * math.sin(rad) * 0.5  # Flattened
                if angle == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            self.c.drawPath(path, stroke=1, fill=0)
        
        # Sun
        self.c.setStrokeColor(HexColor("#FFD700"))
        self.c.setLineWidth(4)
        sun_x = cx - 3*inch
        sun_y = cy + 1*inch
        self.c.circle(sun_x, sun_y, 0.5*inch, fill=0, stroke=1)
        # Sun rays
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            x1 = sun_x + 0.6*inch * math.cos(rad)
            y1 = sun_y + 0.6*inch * math.sin(rad)
            x2 = sun_x + 0.9*inch * math.cos(rad)
            y2 = sun_y + 0.9*inch * math.sin(rad)
            self.c.line(x1, y1, x2, y2)
        
        # Clouds
        cloud_y = cy - 1*inch
        for cloud_x in [cx - 1.5*inch, cx + 1.5*inch]:
            self.c.setStrokeColor(HexColor("#87CEEB"))
            for offset_x, offset_y, r in [(0, 0, 0.3), (-0.2, 0.1, 0.2), (0.2, 0.1, 0.2)]:
                self.c.circle(cloud_x + offset_x*inch, cloud_y + offset_y*inch, r*inch, fill=0, stroke=1)
    
    def draw_certificate(self):
        """Completion certificate"""
        self.new_page()
        
        # Border
        self.c.setStrokeColor(self.colors["accent"])
        self.c.setLineWidth(4)
        self.c.rect(self.MARGIN, self.MARGIN, 
                   self.PAGE_WIDTH - 2*self.MARGIN, 
                   self.PAGE_HEIGHT - 2*self.MARGIN, 
                   fill=0, stroke=1)
        
        # Inner border
        self.c.setLineWidth(2)
        self.c.rect(self.MARGIN + 0.2*inch, self.MARGIN + 0.2*inch, 
                   self.PAGE_WIDTH - 2*self.MARGIN - 0.4*inch, 
                   self.PAGE_HEIGHT - 2*self.MARGIN - 0.4*inch, 
                   fill=0, stroke=1)
        
        # Title
        self.c.setFont("Helvetica-Bold", 36)
        self.c.setFillColor(self.colors["primary"])
        title = "Certificate of Completion"
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 36)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - self.MARGIN - 1.5*inch, title)
        
        # Message
        self.c.setFont("Helvetica", 18)
        self.c.setFillColor(self.colors["text"])
        message = "This certifies that"
        msg_width = self.c.stringWidth(message, "Helvetica", 18)
        self.c.drawString((self.PAGE_WIDTH - msg_width)/2, self.PAGE_HEIGHT - self.MARGIN - 2.5*inch, message)
        
        # Name line
        self.c.setStrokeColor(self.colors["text"])
        self.c.setLineWidth(1)
        self.c.line(self.MARGIN + 1*inch, self.PAGE_HEIGHT - self.MARGIN - 3.5*inch,
                   self.PAGE_WIDTH - self.MARGIN - 1*inch, self.PAGE_HEIGHT - self.MARGIN - 3.5*inch)
        
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(gray)
        name_text = "(Write your name here)"
        name_width = self.c.stringWidth(name_text, "Helvetica", 14)
        self.c.drawString((self.PAGE_WIDTH - name_width)/2, self.PAGE_HEIGHT - self.MARGIN - 3.8*inch, name_text)
        
        # Achievement
        self.c.setFont("Helvetica", 16)
        self.c.setFillColor(self.colors["text"])
        achievement = f"has successfully completed the {self.title}"
        ach_width = self.c.stringWidth(achievement, "Helvetica", 16)
        self.c.drawString((self.PAGE_WIDTH - ach_width)/2, self.PAGE_HEIGHT - self.MARGIN - 4.5*inch, achievement)
        
        # Date
        self.c.setFont("Helvetica", 14)
        date_text = f"Date: _________________{datetime.now().year}"
        self.c.drawString(self.MARGIN + 1*inch, self.MARGIN + 1*inch, date_text)
        
        # Signature
        sig_text = "Parent/Teacher Signature: _________________________"
        self.c.drawString(self.MARGIN + 1*inch, self.MARGIN + 0.5*inch, sig_text)
        
        # Stars decoration
        self.c.setFillColor(self.colors["accent"])
        for x in [self.MARGIN + 0.5*inch, self.PAGE_WIDTH - self.MARGIN - 0.5*inch]:
            self.c.drawString(x, self.PAGE_HEIGHT - self.MARGIN - 0.8*inch, "⭐")


if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    if len(sys.argv) > 1:
        title = sys.argv[1]
        subtitle = sys.argv[2] if len(sys.argv) > 2 else "A Learn-to-Write Workbook"
    else:
        title = "My First Learn-to-Write Workbook"
        subtitle = "Practice for Kids with Pen Control, Line Tracing, Letters, and More!"
    
    print(f"Generating workbook: {title}")
    print("=" * 60)
    
    generator = WorkbookGenerator(title, subtitle, level="preschool")
    filename = generator.generate_workbook()
    
    print("=" * 60)
    print(f"✅ Workbook complete!")
    print(f"   File: {filename}")
    print(f"   Size: 8.5\" x 11\" (US Letter)")
    print(f"   Ready to upload to Amazon KDP!")
