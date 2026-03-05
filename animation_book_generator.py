#!/usr/bin/env python3
"""
Kids Animation & Flip Book Generator
Teaches children how to make simple animations and flip books
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, gray
import os

class KidsAnimationBook:
    """Generate animation teaching books for kids"""
    
    PAGE_WIDTH = 8.5 * inch
    PAGE_HEIGHT = 11 * inch
    MARGIN = 0.6 * inch
    
    ANIMATION_THEMES = {
        "flip_book": {
            "title": "My First Flip Book",
            "subtitle": "Make Your Own Animations! A Step-by-Step Guide for Kids",
            "description": "Learn to create bouncing balls, walking characters, and more!",
            "projects": [
                {"name": "Bouncing Ball", "frames": 8, "difficulty": "Easy"},
                {"name": "Smiling Face", "frames": 6, "difficulty": "Easy"},
                {"name": "Walking Stick Figure", "frames": 8, "difficulty": "Medium"},
                {"name": "Flapping Bird", "frames": 6, "difficulty": "Medium"},
                {"name": "Jumping Frog", "frames": 10, "difficulty": "Hard"}
            ]
        },
        "drawing_animations": {
            "title": "Draw Your Own Cartoons",
            "subtitle": "Learn to Draw Animated Characters Step by Step",
            "description": "From simple shapes to moving characters!",
            "projects": [
                {"name": "Bouncing Ball Character", "steps": 5},
                {"name": "Walking Dog", "steps": 6},
                {"name": "Flying Bird", "steps": 5},
                {"name": "Swimming Fish", "steps": 4},
                {"name": "Dancing Robot", "steps": 7}
            ]
        },
        "stop_motion": {
            "title": "Stop Motion for Kids",
            "subtitle": "Make Movies with Toys and Clay!",
            "description": "Create your own mini movies using household items",
            "projects": [
                "Clay Characters",
                "Toy Adventures", 
                "Paper Cutout Stories",
                "Lego Movies",
                "Food Animations"
            ]
        }
    }
    
    def __init__(self, book_type="flip_book"):
        self.book_data = self.ANIMATION_THEMES[book_type]
        self.book_type = book_type
        self.page_num = 0
        os.makedirs("animation_books/output", exist_ok=True)
        
        self.colors = {
            "primary": HexColor("#FF6B6B"),
            "secondary": HexColor("#4ECDC4"),
            "accent": HexColor("#FFE66D"),
            "text": HexColor("#2C3E50"),
            "light": HexColor("#F7F9FC"),
            "gray": HexColor("#BDC3C7")
        }
    
    def generate(self):
        """Generate animation teaching book"""
        filename = f"animation_books/output/{self.book_type}_guide.pdf"
        self.c = canvas.Canvas(filename, pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT))
        
        # Title page
        self.draw_title_page()
        
        # Welcome/Introduction
        self.draw_welcome_page()
        
        # What you need
        self.draw_supplies_page()
        
        # How animation works
        self.draw_how_it_works_page()
        
        # Practice pages
        self.draw_practice_section()
        
        # Projects
        for project in self.book_data["projects"]:
            if self.book_type == "flip_book":
                self.draw_flip_book_project(project)
            elif self.book_type == "drawing_animations":
                self.draw_drawing_project(project)
            else:
                self.draw_stop_motion_project(project)
        
        # Tips and tricks
        self.draw_tips_page()
        
        # Share your work
        self.draw_share_page()
        
        # Certificate
        self.draw_certificate()
        
        self.c.save()
        print(f"✅ Animation Book Created: {filename}")
        print(f"   Type: {self.book_type.replace('_', ' ').title()}")
        print(f"   Pages: {self.page_num}")
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
        
        # Colorful header
        self.c.setFillColor(self.colors["primary"])
        self.c.rect(0, self.PAGE_HEIGHT - 3*inch, self.PAGE_WIDTH, 3*inch, fill=1, stroke=0)
        
        # Title
        self.c.setFont("Helvetica-Bold", 38)
        self.c.setFillColor(HexColor("#FFFFFF"))
        title_width = self.c.stringWidth(self.book_data["title"], "Helvetica-Bold", 38)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - 1.8*inch,
                         self.book_data["title"])
        
        # Subtitle
        self.c.setFont("Helvetica", 16)
        self.c.setFillColor(self.colors["text"])
        subtitle_width = self.c.stringWidth(self.book_data["subtitle"], "Helvetica", 16)
        self.c.drawString((self.PAGE_WIDTH - subtitle_width)/2, self.PAGE_HEIGHT - 3.2*inch,
                         self.book_data["subtitle"])
        
        # Description
        self.c.setFont("Helvetica", 13)
        desc_width = self.c.stringWidth(self.book_data["description"], "Helvetica", 13)
        self.c.drawString((self.PAGE_WIDTH - desc_width)/2, self.PAGE_HEIGHT - 3.8*inch,
                         self.book_data["description"])
        
        # Animation icons
        icons = ["🎬", "🎨", "🎭", "✏️", "🎪"]
        self.c.setFont("Helvetica", 40)
        for i, icon in enumerate(icons):
            x = self.MARGIN + 1*inch + i * 1.3*inch
            self.c.drawString(x, 3*inch, icon)
        
        # Age info
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setFillColor(self.colors["secondary"])
        self.c.drawString(self.MARGIN, 1.5*inch, "Ages 6-12 | No Experience Needed!")
    
    def draw_welcome_page(self):
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Welcome, Young Animator!")
        
        text = [
            "Have you ever wondered how cartoons move? How does Mickey Mouse",
            "wave his hand? How do characters in your favorite shows walk, jump,",
            "and dance?",
            "",
            "The secret is ANIMATION! Animation means bringing drawings to life",
            "by showing many pictures quickly, one after another. Each picture is",
            "slightly different, and when you flip through them fast, it looks like",
            "movement!",
            "",
            "In this book, you will:",
            "• Learn how animation works",
            "• Practice drawing simple movements",
            "• Create your own flip books",
            "• Make your characters come alive!",
            "",
            "Remember: Every famous animator started just like you - with a",
            "pencil, paper, and imagination. Let's get started!"
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1*inch
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(self.colors["text"])
        for line in text:
            self.c.drawString(self.MARGIN, y, line)
            y -= 0.25*inch
    
    def draw_supplies_page(self):
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "What You'll Need")
        
        supplies = [
            ("✏️", "Pencils", "Regular #2 pencils for sketching"),
            ("🖊️", "Markers or Pens", "For outlining and adding color"),
            ("📒", "Small Notebook", "Or stack of index cards for flip books"),
            ("📎", "Stapler or Binder Clip", "To hold your flip book together"),
            ("🧼", "Eraser", "Everyone makes mistakes - that's okay!"),
            ("📱", "Phone or Tablet (Optional)", "To record your animation"),
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1.2*inch
        for emoji, name, desc in supplies:
            self.c.setFont("Helvetica", 20)
            self.c.drawString(self.MARGIN, y, emoji)
            
            self.c.setFont("Helvetica-Bold", 13)
            self.c.setFillColor(self.colors["text"])
            self.c.drawString(self.MARGIN + 0.5*inch, y, name)
            
            self.c.setFont("Helvetica", 11)
            self.c.setFillColor(gray)
            self.c.drawString(self.MARGIN + 0.5*inch, y - 0.2*inch, desc)
            
            y -= 0.7*inch
        
        # Tip box
        self.c.setFillColor(self.colors["accent"])
        self.c.roundRect(self.MARGIN, self.MARGIN + 0.5*inch,
                        self.PAGE_WIDTH - 2*self.MARGIN, 1.2*inch, 10, fill=1, stroke=0)
        
        self.c.setFont("Helvetica-Bold", 12)
        self.c.setFillColor(self.colors["text"])
        self.c.drawString(self.MARGIN + 0.3*inch, self.MARGIN + 1.3*inch, "💡 Pro Tip:")
        self.c.setFont("Helvetica", 11)
        self.c.drawString(self.MARGIN + 0.3*inch, self.MARGIN + 1*inch,
                         "You don't need expensive supplies! Start with regular paper")
        self.c.drawString(self.MARGIN + 0.3*inch, self.MARGIN + 0.8*inch,
                         "and a pencil. The magic is in your imagination!")
    
    def draw_how_it_works_page(self):
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "How Animation Works")
        
        # Simple diagram explanation
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(self.colors["text"])
        
        explanation = [
            "Animation is like a magic trick for your eyes! Here's how it works:",
            "",
            "1. DRAW: You draw a picture.",
            "2. CHANGE: You draw almost the same picture, but slightly different.",
            "3. REPEAT: You keep drawing, making small changes each time.",
            "4. FLIP: When you flip through the pages quickly, your brain sees MOVEMENT!",
            "",
            "This is called 'persistence of vision' - your eye holds onto an image",
            "for a split second after you see it. So when pictures change fast,",
            "they blend together in your brain!"
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1*inch
        for line in explanation:
            self.c.drawString(self.MARGIN, y, line)
            y -= 0.25*inch
        
        # Visual example boxes
        box_y = self.MARGIN + 2*inch
        self.c.setFont("Helvetica-Bold", 11)
        
        for i, (label, x_pos) in enumerate([("Frame 1", self.MARGIN + 0.5*inch),
                                            ("Frame 2", self.MARGIN + 2.5*inch),
                                            ("Frame 3", self.MARGIN + 4.5*inch),
                                            ("Frame 4", self.MARGIN + 6.5*inch)]):
            # Box
            self.c.setStrokeColor(black)
            self.c.setLineWidth(2)
            self.c.rect(x_pos, box_y, 1.3*inch, 1.5*inch, fill=0, stroke=1)
            
            # Ball at different heights
            ball_y = box_y + 0.3*inch + i * 0.25*inch
            self.c.setFillColor(self.colors["primary"])
            self.c.circle(x_pos + 0.65*inch, ball_y, 0.15*inch, fill=1, stroke=0)
            
            # Label
            self.c.setFillColor(self.colors["text"])
            self.c.drawString(x_pos + 0.3*inch, box_y - 0.25*inch, label)
        
        # Arrow
        self.c.setFont("Helvetica", 16)
        self.c.drawString(self.MARGIN + 1.2*inch, box_y + 1.8*inch, "➡️ FLIP FAST ➡️")
        
        # Result
        self.c.setFillColor(self.colors["secondary"])
        self.c.roundRect(self.MARGIN, self.MARGIN + 0.3*inch,
                        self.PAGE_WIDTH - 2*self.MARGIN, 0.8*inch, 10, fill=1, stroke=0)
        
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setFillColor(HexColor("#FFFFFF"))
        self.c.drawString(self.MARGIN + 1*inch, self.MARGIN + 0.7*inch,
                         "RESULT: The ball looks like it's bouncing!")
    
    def draw_practice_section(self):
        """Draw practice pages for basic shapes and movements"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Practice: Drawing the Same Thing")
        
        instructions = [
            "Before making animations, practice drawing the same shape",
            "multiple times. Try to make each drawing as close to the",
            "same as possible. This is the secret to smooth animation!"
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 0.8*inch
        self.c.setFont("Helvetica", 11)
        self.c.setFillColor(self.colors["text"])
        for line in instructions:
            self.c.drawString(self.MARGIN, y, line)
            y -= 0.22*inch
        
        # Practice circles
        self.c.setFont("Helvetica-Bold", 13)
        self.c.drawString(self.MARGIN, y - 0.3*inch, "Practice 1: Draw 6 circles the same size")
        
        for i in range(6):
            x = self.MARGIN + 0.3*inch + (i % 3) * 2.5*inch
            row_y = y - 0.8*inch - (i // 3) * 1.5*inch
            self.c.setStrokeColor(self.colors["gray"])
            self.c.circle(x + 1*inch, row_y, 0.5*inch, fill=0, stroke=1)
            self.c.setFont("Helvetica", 10)
            self.c.drawString(x + 0.8*inch, row_y - 0.7*inch, f"Circle {i+1}")
        
        # Practice lines
        self.c.setFont("Helvetica-Bold", 13)
        self.c.drawString(self.MARGIN, self.MARGIN + 2*inch, "Practice 2: Draw 4 straight lines the same length")
        
        for i in range(4):
            y = self.MARGIN + 1.2*inch
            x = self.MARGIN + 0.3*inch + i * 2*inch
            self.c.setStrokeColor(self.colors["gray"])
            self.c.line(x, y, x + 1.5*inch, y)
    
    def draw_flip_book_project(self, project):
        """Draw a complete flip book project"""
        # Title page for project
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 28)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Project: {project['name']}")
        
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(self.colors["text"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 0.5*inch,
                         f"Difficulty: {project['difficulty']} | Frames: {project['frames']}")
        
        # Instructions
        y = self.PAGE_HEIGHT - self.MARGIN - 1.2*inch
        instructions = [
            f"In this project, you will draw {project['frames']} pictures.",
            "Each picture shows the character in a slightly different position.",
            "When you flip through them quickly, it will look like animation!",
            "",
            "TIPS:",
            "• Draw lightly in pencil first",
            "• Keep the character in the same spot on each page",
            "• Make small changes between each frame",
            "• Number your pages so you don't get confused!"
        ]
        
        self.c.setFont("Helvetica", 11)
        for line in instructions:
            self.c.drawString(self.MARGIN, y, line)
            y -= 0.24*inch
        
        # Animation frames
        num_frames = min(project['frames'], 8)  # Show up to 8 frames
        frame_size = 1.2*inch
        
        self.c.setFont("Helvetica-Bold", 13)
        self.c.drawString(self.MARGIN, self.MARGIN + 3.5*inch, "Draw your animation in these boxes:")
        
        for i in range(num_frames):
            col = i % 4
            row = i // 4
            x = self.MARGIN + 0.2*inch + col * (frame_size + 0.3*inch)
            y = self.MARGIN + 1.5*inch - row * (frame_size + 0.5*inch)
            
            # Frame box
            self.c.setStrokeColor(black)
            self.c.setLineWidth(2)
            self.c.rect(x, y, frame_size, frame_size * 1.3, fill=0, stroke=1)
            
            # Frame number
            self.c.setFont("Helvetica-Bold", 10)
            self.c.setFillColor(self.colors["primary"])
            self.c.drawString(x + 0.1*inch, y + frame_size * 1.3 + 0.1*inch, f"Frame {i+1}")
            
            # Simple guide drawing in corner
            self.c.setStrokeColor(self.colors["gray"])
            self.c.setLineWidth(1)
            guide_size = 0.25*inch
            self.c.circle(x + frame_size/2, y + frame_size * 0.6, guide_size, fill=0, stroke=1)
    
    def draw_drawing_project(self, project):
        """Draw a step-by-step drawing tutorial"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 28)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Draw: {project['name']}")
        
        steps = project['steps']
        box_size = 1.8*inch
        
        for i in range(min(steps, 6)):
            col = i % 2
            row = i // 2
            x = self.MARGIN + 0.3*inch + col * (box_size + 0.8*inch)
            y = self.PAGE_HEIGHT - self.MARGIN - 1.5*inch - row * (box_size + 0.8*inch)
            
            # Step box
            self.c.setStrokeColor(self.colors["primary"])
            self.c.setLineWidth(3)
            self.c.roundRect(x, y, box_size, box_size, 10, fill=0, stroke=1)
            
            # Step number
            self.c.setFillColor(self.colors["accent"])
            self.c.circle(x + 0.3*inch, y + box_size - 0.3*inch, 0.2*inch, fill=1, stroke=0)
            self.c.setFont("Helvetica-Bold", 12)
            self.c.setFillColor(HexColor("#FFFFFF"))
            self.c.drawString(x + 0.24*inch, y + box_size - 0.36*inch, str(i+1))
    
    def draw_stop_motion_project(self, project_name):
        """Draw a stop motion project page"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, f"Project: {project_name}")
        
        # Story planning section
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setFillColor(self.colors["text"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN - 1*inch, "Plan Your Story:")
        
        # Story boxes
        self.c.setFont("Helvetica", 11)
        story_elements = [
            "What happens at the START?",
            "What happens in the MIDDLE?",
            "How does it END?"
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1.5*inch
        for element in story_elements:
            self.c.setStrokeColor(self.colors["gray"])
            self.c.setLineWidth(1)
            self.c.roundRect(self.MARGIN, y - 0.8*inch, self.PAGE_WIDTH - 2*self.MARGIN, 1*inch, 5, fill=0, stroke=1)
            self.c.setFillColor(self.colors["text"])
            self.c.drawString(self.MARGIN + 0.2*inch, y - 0.2*inch, element)
            y -= 1.3*inch
    
    def draw_tips_page(self):
        """Animation tips and tricks"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.setFillColor(self.colors["primary"])
        self.c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Pro Tips for Animators")
        
        tips = [
            ("💡", "Start Simple", "Begin with easy projects before trying complex ones."),
            ("🎯", "Keep It Small", "Small changes between frames = smooth animation."),
            ("🐌", "Slow Motion", "Animating slowly? Add more frames between movements."),
            ("⚡", "Speed Up", "For fast action, use fewer frames with bigger changes."),
            ("🔄", "Loop It", "To repeat an action, copy your frames in reverse order!"),
            ("✏️", "Light First", "Draw lightly, then darken when you're happy with it."),
            ("🎬", "Test Often", "Flip your pages frequently to see how it looks!"),
            ("🎨", "Have Fun", "There are no mistakes in animation - only happy accidents!")
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1.2*inch
        for emoji, title, tip in tips:
            # Tip box
            self.c.setFillColor(self.colors["light"])
            self.c.roundRect(self.MARGIN, y - 0.2*inch,
                           self.PAGE_WIDTH - 2*self.MARGIN, 0.7*inch, 8, fill=1, stroke=0)
            
            self.c.setFont("Helvetica", 16)
            self.c.drawString(self.MARGIN + 0.2*inch, y + 0.2*inch, emoji)
            
            self.c.setFont("Helvetica-Bold", 12)
            self.c.setFillColor(self.colors["text"])
            self.c.drawString(self.MARGIN + 0.7*inch, y + 0.2*inch, title)
            
            self.c.setFont("Helvetica", 10)
            self.c.setFillColor(gray)
            self.c.drawString(self.MARGIN + 0.7*inch, y - 0.1*inch, tip)
            
            y -= 0.9*inch
    
    def draw_share_page(self):
        """Page encouraging kids to share their work"""
        self.new_page()
        
        self.c.setFont("Helvetica-Bold", 28)
        self.c.setFillColor(self.colors["primary"])
        title = "Share Your Animation!"
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 28)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - self.MARGIN - 0.5*inch, title)
        
        text = [
            "Great job creating your animations! Now it's time to share",
            "them with family and friends!",
            "",
            "WAYS TO SHARE:",
            "• Show your flip book to your family",
            "• Perform a 'flip show' for your friends",
            "• Ask a parent to record a video of your animation",
            "• Start an animation club at school",
            "• Teach a friend how to make flip books!",
            "",
            "KEEP CREATING:",
            "• Make longer animations with more frames",
            "• Try adding color to your drawings",
            "• Create stories with multiple characters",
            "• Experiment with different speeds",
            "• Most importantly: HAVE FUN!"
        ]
        
        y = self.PAGE_HEIGHT - self.MARGIN - 1.5*inch
        self.c.setFont("Helvetica", 12)
        self.c.setFillColor(self.colors["text"])
        for line in text:
            if line.startswith("•") or line.endswith(":"):
                self.c.setFont("Helvetica-Bold", 12)
            else:
                self.c.setFont("Helvetica", 12)
            self.c.drawString(self.MARGIN + (0.3*inch if line.startswith("•") else 0), y, line)
            y -= 0.26*inch
        
        # Note box
        self.c.setFillColor(self.colors["accent"])
        self.c.roundRect(self.MARGIN, self.MARGIN + 0.5*inch,
                        self.PAGE_WIDTH - 2*self.MARGIN, 1*inch, 10, fill=1, stroke=0)
        
        self.c.setFont("Helvetica-Bold", 12)
        self.c.setFillColor(self.colors["text"])
        note = "Remember: Every professional animator started exactly where you are now."
        self.c.drawString(self.MARGIN + 0.3*inch, self.MARGIN + 1*inch, note)
        self.c.drawString(self.MARGIN + 0.3*inch, self.MARGIN + 0.7*inch, "Keep drawing, keep animating, keep dreaming!")
    
    def draw_certificate(self):
        """Completion certificate"""
        self.new_page()
        
        # Border
        self.c.setStrokeColor(self.colors["primary"])
        self.c.setLineWidth(5)
        self.c.rect(self.MARGIN, self.MARGIN,
                   self.PAGE_WIDTH - 2*self.MARGIN,
                   self.PAGE_HEIGHT - 2*self.MARGIN, fill=0, stroke=1)
        
        # Inner border
        self.c.setLineWidth(2)
        self.c.rect(self.MARGIN + 0.2*inch, self.MARGIN + 0.2*inch,
                   self.PAGE_WIDTH - 2*self.MARGIN - 0.4*inch,
                   self.PAGE_HEIGHT - 2*self.MARGIN - 0.4*inch, fill=0, stroke=1)
        
        self.c.setFont("Helvetica-Bold", 40)
        self.c.setFillColor(self.colors["primary"])
        title = "CERTIFICATE OF COMPLETION"
        title_width = self.c.stringWidth(title, "Helvetica-Bold", 40)
        self.c.drawString((self.PAGE_WIDTH - title_width)/2, self.PAGE_HEIGHT - self.MARGIN - 2*inch, title)
        
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(self.colors["text"])
        self.c.drawString((self.PAGE_WIDTH - 150)/2, self.PAGE_HEIGHT - self.MARGIN - 3*inch, "This certifies that")
        
        # Name line
        self.c.setStrokeColor(self.colors["text"])
        self.c.setLineWidth(1)
        self.c.line(self.MARGIN + 1*inch, self.PAGE_HEIGHT - self.MARGIN - 4*inch,
                   self.PAGE_WIDTH - self.MARGIN - 1*inch, self.PAGE_HEIGHT - self.MARGIN - 4*inch)
        
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(gray)
        name_text = "(Animator Name)"
        name_width = self.c.stringWidth(name_text, "Helvetica", 14)
        self.c.drawString((self.PAGE_WIDTH - name_width)/2, self.PAGE_HEIGHT - self.MARGIN - 4.3*inch, name_text)
        
        self.c.setFont("Helvetica-Bold", 18)
        self.c.setFillColor(self.colors["text"])
        achievement = f"has completed the {self.book_data['title']}"
        ach_width = self.c.stringWidth(achievement, "Helvetica-Bold", 18)
        self.c.drawString((self.PAGE_WIDTH - ach_width)/2, self.PAGE_HEIGHT - self.MARGIN - 5*inch, achievement)
        
        self.c.setFont("Helvetica", 14)
        congrats = "and is now officially a Junior Animator!"
        con_width = self.c.stringWidth(congrats, "Helvetica", 14)
        self.c.drawString((self.PAGE_WIDTH - con_width)/2, self.PAGE_HEIGHT - self.MARGIN - 5.5*inch, congrats)


if __name__ == "__main__":
    import sys
    
    book_type = sys.argv[1] if len(sys.argv) > 1 else "flip_book"
    
    print(f"Creating {book_type} animation book...")
    print("="*60)
    
    book = KidsAnimationBook(book_type)
    filename = book.generate()
    
    print("="*60)
    print(f"✅ Animation book complete!")
    print(f"   File: {filename}")
    print(f"   Ready to upload to Amazon KDP!")
