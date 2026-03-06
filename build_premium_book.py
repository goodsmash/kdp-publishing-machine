#!/usr/bin/env python3
"""
High-Quality Image-by-Image Book Builder
One image at a time, maximum quality, hyper-realistic for kids education
"""

import os
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
IMG_DIR = ROOT / "illustrations" / "high_quality"
OUT_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

from alibaba_model_rotator import AlibabaModelRotator


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def generate_hyper_realistic_image(rotator, word, concept):
    """Generate one hyper-realistic image with detailed prompt"""
    
    # Ultra-detailed prompt for maximum quality
    prompt = f"""Hyper-realistic 3D render of {concept}, 
    Pixar-style animation quality, 
    subsurface skin scattering, 
    volumetric lighting, 
    ray-traced reflections, 
    8K texture detail, 
    cinematic composition, 
    soft bokeh background, 
    educational children's book illustration, 
    scientifically accurate anatomy,
    vibrant natural colors,
    studio lighting setup,
    octane render quality"""
    
    print(f"\n{'='*60}")
    print(f"🎨 GENERATING: {word.upper()}")
    print(f"{'='*60}")
    print(f"Prompt: {prompt[:100]}...")
    
    # Use best available model
    result = rotator.generate_image(prompt, f"hq_{word}", size="1328*1328")
    
    if result:
        print(f"✅ SUCCESS: {result}")
        # Verify image quality
        try:
            with Image.open(result) as img:
                print(f"   Size: {img.size}")
                print(f"   Mode: {img.mode}")
        except Exception as e:
            print(f"   Warning: Could not verify image - {e}")
    else:
        print(f"❌ FAILED: {word}")
    
    return result


def build_premium_book():
    """Build one premium book with hyper-realistic images"""
    
    # Book theme: AFRICAN SAFARI ANIMALS
    book_title = "African Safari Animals"
    subtitle = "Learn to Write with Real Animals"
    
    animals = [
        {
            "word": "lion",
            "sentence": "The lion is the king of the jungle.",
            "concept": "majestic male lion with golden mane, African savanna at golden hour"
        },
        {
            "word": "elephant", 
            "sentence": "The elephant has a long trunk.",
            "concept": "African elephant with large tusks, wrinkled grey skin, watering hole"
        },
        {
            "word": "giraffe",
            "sentence": "The giraffe has a long neck.", 
            "concept": "tall giraffe with spotted pattern, reaching for acacia tree leaves"
        },
        {
            "word": "zebra",
            "sentence": "The zebra has black and white stripes.",
            "concept": "plains zebra with distinctive stripe pattern, grassland background"
        },
        {
            "word": "rhino",
            "sentence": "The rhino has a big horn.",
            "concept": "white rhinoceros with two horns, thick armored skin, dust bath"
        },
        {
            "word": "hippo",
            "sentence": "The hippo loves water.",
            "concept": "hippopotamus partially submerged in river, pinkish grey skin"
        }
    ]
    
    print("\n" + "="*70)
    print(f"📚 BUILDING: {book_title}")
    print(f"   {subtitle}")
    print("="*70)
    
    rotator = AlibabaModelRotator()
    images = {}
    
    # Generate images ONE BY ONE with quality check
    for i, animal in enumerate(animals, 1):
        print(f"\n\n>>> IMAGE {i}/{len(animals)} <<<")
        
        img_path = generate_hyper_realistic_image(
            rotator, 
            animal["word"], 
            animal["concept"]
        )
        
        if img_path:
            images[animal["word"]] = img_path
            
            # Ask for user confirmation (simulated - in real use would pause)
            print(f"   ✓ Image {i} complete. Moving to next...")
        else:
            print(f"   ⚠️  Image {i} failed. Will use placeholder.")
        
        # Small delay between generations
        import time
        time.sleep(2)
    
    # Build the PDF with all collected images
    print("\n\n" + "="*70)
    print("📖 ASSEMBLING BOOK...")
    print("="*70)
    
    pdf_path = OUT_DIR / f"{book_title.replace(' ', '_')}_Premium.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
    
    # Premium Cover
    c.setFillColor(HexColor("#2C1810"))  # Dark safari brown
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Golden accent
    c.setFillColor(HexColor("#D4AF37"))
    c.roundRect(W*0.05, H*0.75, W*0.9, 80, 40, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 42)
    c.drawString(W*0.08, H*0.78, book_title)
    
    c.setFont("Helvetica", 18)
    c.drawString(W*0.08, H*0.68, subtitle)
    
    c.setFillColor(HexColor("#D4AF37"))
    c.roundRect(W*0.08, H*0.55, 200, 50, 25, fill=1, stroke=0)
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(W*0.10, H*0.57, "Premium Edition")
    
    c.showPage()
    
    # Content pages
    for i, animal in enumerate(animals, 1):
        word = animal["word"]
        sentence = animal["sentence"]
        img_path = images.get(word)
        
        # Header
        c.setFillColor(HexColor("#2C1810"))
        c.setFont("Helvetica-Bold", 26)
        c.drawString(W*0.06, H*0.92, f"{i}. {word.title()}")
        
        # Image area
        if img_path and Path(img_path).exists():
            max_w, max_h = W*0.6, H*0.4
            iw, ih = fit_image(img_path, max_w, max_h)
            
            # Image border
            c.setStrokeColor(HexColor("#D4AF37"))
            c.setLineWidth(4)
            c.roundRect((W-iw)/2 - 5, H*0.50 - 5, iw + 10, ih + 10, 15, fill=0, stroke=1)
            
            # Draw image
            c.drawImage(str(img_path), (W-iw)/2, H*0.50, iw, ih, preserveAspectRatio=True)
            
            print(f"   ✓ Added image for {word}")
        else:
            c.setFillColor(HexColor("#F5F5DC"))
            c.roundRect(W*0.2, H*0.50, W*0.6, H*0.32, 15, fill=1, stroke=0)
            c.setFillColor(HexColor("#999999"))
            c.setFont("Helvetica", 14)
            c.drawString(W*0.35, H*0.68, f"[{word} - High Quality Image]")
        
        # Tracing area
        c.setStrokeColor(HexColor("#D4AF37"))
        c.setLineWidth(2)
        for row in range(5):
            y = H*0.38 - row*0.065
            c.line(W*0.08, y, W*0.92, y)
        
        # Big word
        c.setFillColor(HexColor("#2C1810"))
        c.setFont("Helvetica-Bold", 44)
        c.drawString(W*0.10, H*0.35, word)
        
        # Tracing copies
        c.setFillColor(HexColor("#CCCCCC"))
        c.setFont("Helvetica", 36)
        c.drawString(W*0.10 + 180, H*0.35, word)
        c.drawString(W*0.10 + 340, H*0.35, word)
        
        # Sentence section
        c.setFillColor(HexColor("#8B4513"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(W*0.08, H*0.18, "Read and trace:")
        
        c.setFillColor(HexColor("#2C1810"))
        c.setFont("Helvetica", 18)
        c.drawString(W*0.08, H*0.13, sentence)
        
        c.setFillColor(HexColor("#AAAAAA"))
        c.drawString(W*0.08, H*0.08, sentence)
        
        c.showPage()
    
    # Premium Certificate
    c.setFillColor(HexColor("#2C1810"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#D4AF37"))
    c.setLineWidth(5)
    c.roundRect(W*0.08, H*0.15, W*0.84, H*0.70, 30, fill=0, stroke=1)
    
    c.setFillColor(HexColor("#D4AF37"))
    c.setFont("Helvetica-Bold", 38)
    tw = c.stringWidth("Safari Explorer Certificate", "Helvetica-Bold", 38)
    c.drawString((W-tw)/2, H*0.72, "Safari Explorer Certificate")
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica", 16)
    c.drawString(W*0.20, H*0.60, "This certifies that")
    
    c.setStrokeColor(HexColor("#D4AF37"))
    c.setLineWidth(2)
    c.line(W*0.20, H*0.50, W*0.80, H*0.50)
    
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#AAAAAA"))
    c.drawString(W*0.42, H*0.46, "(Student Name)")
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica", 16)
    c.drawString(W*0.12, H*0.38, "has successfully completed the African Safari Animals")
    c.drawString(W*0.25, H*0.33, "writing workbook and learned about 6 amazing animals!")
    
    # Gold seal
    c.setFillColor(HexColor("#D4AF37"))
    c.circle(W*0.5, H*0.20, 50, fill=1, stroke=0)
    c.setFillColor(HexColor("#2C1810"))
    c.setFont("Helvetica-Bold", 30)
    c.drawString(W*0.47, H*0.22, "★")
    
    c.save()
    
    print("\n" + "="*70)
    print(f"✅ PREMIUM BOOK COMPLETE!")
    print(f"   File: {pdf_path}")
    print(f"   Images: {len(images)}/{len(animals)}")
    print("="*70)
    
    return str(pdf_path)


if __name__ == "__main__":
    build_premium_book()
