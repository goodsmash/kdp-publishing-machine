#!/usr/bin/env python3
"""
Educational Wildlife Book - High Quality
Realistic images, fixed layout, no overlapping text
"""

from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "real_books" / "output"
IMG_DIR = ROOT / "illustrations" / "educational"
OUT_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

from alibaba_model_rotator import AlibabaModelRotator


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def generate_educational_image(rotator, word, concept):
    """Generate scientifically accurate educational image"""
    
    prompt = f"""Scientifically accurate {concept}, 
    field guide illustration style, 
    natural history museum quality, 
    educational diagram, 
    realistic anatomy and proportions, 
    natural colors, 
    white background for clarity, 
    labeled specimen style, 
    National Geographic quality, 
    8K detail, 
    photorealistic render, 
    wildlife photography style, 
    no cartoon elements, 
    pure educational reference"""
    
    print(f"\n📸 Generating educational image: {word}")
    result = rotator.generate_image(prompt, f"edu_{word}", size="1328*1328")
    
    if result:
        print(f"✅ {word}: {result}")
    else:
        print(f"❌ {word}: Failed")
    
    return result


def build_educational_book():
    """Build North American Wildlife educational book"""
    
    animals = [
        {
            "word": "eagle",
            "sentence": "The eagle has sharp eyes.",
            "concept": "bald eagle with white head and tail, yellow beak, detailed feather texture"
        },
        {
            "word": "bear",
            "sentence": "The bear is very strong.",
            "concept": "grizzly bear standing, brown fur texture, powerful build, realistic anatomy"
        },
        {
            "word": "wolf",
            "sentence": "The wolf lives in a pack.",
            "concept": "gray wolf in profile, thick fur coat, alert posture, yellow eyes"
        },
        {
            "word": "moose",
            "sentence": "The moose has big antlers.",
            "concept": "bull moose with large palmate antlers, dark brown fur, realistic proportions"
        },
        {
            "word": "owl",
            "sentence": "The owl flies at night.",
            "concept": "great horned owl, facial disc, feather detail, yellow eyes"
        },
        {
            "word": "deer",
            "sentence": "The deer runs very fast.",
            "concept": "white-tailed deer, alert posture, brown coat, realistic anatomy"
        }
    ]
    
    print("="*60)
    print("NORTH AMERICAN WILDLIFE - Educational Edition")
    print("="*60)
    
    rotator = AlibabaModelRotator()
    images = {}
    
    # Generate educational images
    for animal in animals:
        img_path = generate_educational_image(rotator, animal["word"], animal["concept"])
        if img_path:
            images[animal["word"]] = img_path
        import time
        time.sleep(3)
    
    # Build PDF with CAREFUL LAYOUT (no overlapping)
    pdf_path = OUT_DIR / "North_American_Wildlife_Educational.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))
    
    # COVER
    c.setFillColor(HexColor("#1B4332"))  # Forest green
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#D8F3DC"))
    c.setFont("Helvetica-Bold", 40)
    c.drawString(W*0.08, H*0.70, "North American")
    c.drawString(W*0.08, H*0.60, "Wildlife")
    
    c.setFillColor(HexColor("#95D5B2"))
    c.setFont("Helvetica", 18)
    c.drawString(W*0.08, H*0.50, "Educational Writing Workbook")
    
    c.setFillColor(HexColor("#40916C"))
    c.roundRect(W*0.08, H*0.35, 200, 50, 25, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W*0.10, H*0.37, "Ages 5-8")
    
    c.setFillColor(HexColor("#D8F3DC"))
    c.setFont("Helvetica", 12)
    c.drawString(W*0.08, H*0.20, "✓ Scientifically Accurate Illustrations")
    c.drawString(W*0.08, H*0.16, "✓ Handwriting Practice")
    c.drawString(W*0.08, H*0.12, "✓ Educational Facts")
    
    c.showPage()
    
    # ANIMAL PAGES - Careful spacing to prevent overlap
    for i, animal in enumerate(animals, 1):
        word = animal["word"]
        sentence = animal["sentence"]
        img_path = images.get(word)
        
        # Section header background
        c.setFillColor(HexColor("#40916C"))
        c.rect(0, H*0.88, W, H*0.12, fill=1, stroke=0)
        
        # Page number and title
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 24)
        c.drawString(W*0.05, H*0.92, f"{i}. {word.title()}")
        
        # IMAGE SECTION - Top half, large but not too large
        if img_path and Path(img_path).exists():
            max_w, max_h = W*0.70, H*0.38
            iw, ih = fit_image(img_path, max_w, max_h)
            
            # Center the image
            x_pos = (W - iw) / 2
            y_pos = H*0.48  # Leave room below
            
            # Border
            c.setStrokeColor(HexColor("#40916C"))
            c.setLineWidth(3)
            c.roundRect(x_pos - 5, y_pos - 5, iw + 10, ih + 10, 10, fill=0, stroke=1)
            
            # Draw image
            c.drawImage(str(img_path), x_pos, y_pos, iw, ih, preserveAspectRatio=True)
        else:
            # Placeholder
            c.setFillColor(HexColor("#E8F5E9"))
            c.roundRect(W*0.15, H*0.48, W*0.70, H*0.35, 15, fill=1, stroke=0)
            c.setFillColor(HexColor("#40916C"))
            c.setFont("Helvetica", 14)
            c.drawString(W*0.35, H*0.68, f"[{word.title()}]")
        
        # CLEAR SEPARATION - White space before tracing area
        
        # TRACING AREA - Well below image
        trace_y_start = H*0.40  # Clear space from image
        
        # Tracing lines
        c.setStrokeColor(HexColor("#B7E4C7"))
        c.setLineWidth(1)
        for row in range(4):
            y = trace_y_start - row * 0.055
            c.line(W*0.10, y, W*0.90, y)
        
        # BIG WORD - Clear and centered in tracing area
        c.setFillColor(HexColor("#1B4332"))
        c.setFont("Helvetica-Bold", 48)
        word_width = c.stringWidth(word, "Helvetica-Bold", 48)
        c.drawString((W - word_width) / 2, trace_y_start - 0.03, word)
        
        # Faded traces below
        c.setFillColor(HexColor("#D8F3DC"))
        c.setFont("Helvetica", 36)
        c.drawString((W - word_width) / 2, trace_y_start - 0.09, word)
        
        # SENTENCE SECTION - Well separated at bottom
        sentence_y = H*0.18
        
        c.setFillColor(HexColor("#40916C"))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(W*0.10, sentence_y, "Complete the sentence:")
        
        # Sentence to trace
        c.setFillColor(HexColor("#1B4332"))
        c.setFont("Helvetica", 16)
        c.drawString(W*0.10, sentence_y - 0.04, sentence)
        
        # Faded copy for tracing
        c.setFillColor(HexColor("#95D5B2"))
        c.setFont("Helvetica", 14)
        c.drawString(W*0.10, sentence_y - 0.08, sentence)
        
        # Fun fact at very bottom
        c.setFillColor(HexColor("#74C69D"))
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(W*0.10, H*0.05, f"Fun fact: This {word} lives in North America!")
        
        c.showPage()
    
    # CERTIFICATE
    c.setFillColor(HexColor("#1B4332"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#D8F3DC"))
    c.setLineWidth(4)
    c.roundRect(W*0.08, H*0.15, W*0.84, H*0.70, 20, fill=0, stroke=1)
    
    c.setFillColor(HexColor("#95D5B2"))
    c.setFont("Helvetica-Bold", 36)
    tw = c.stringWidth("Wildlife Explorer Certificate", "Helvetica-Bold", 36)
    c.drawString((W-tw)/2, H*0.75, "Wildlife Explorer Certificate")
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica", 16)
    c.drawString(W*0.20, H*0.60, "This certifies that")
    
    c.setStrokeColor(HexColor("#95D5B2"))
    c.setLineWidth(2)
    c.line(W*0.20, H*0.50, W*0.80, H*0.50)
    
    c.setFont("Helvetica", 14)
    c.drawString(W*0.42, H*0.46, "(Student Name)")
    
    c.setFont("Helvetica", 16)
    c.drawString(W*0.12, H*0.35, "has learned about 6 amazing North American animals")
    c.drawString(W*0.30, H*0.30, "and practiced writing their names!")
    
    c.save()
    print(f"\n✅ EDUCATIONAL BOOK: {pdf_path}")
    return str(pdf_path)


if __name__ == "__main__":
    build_educational_book()
