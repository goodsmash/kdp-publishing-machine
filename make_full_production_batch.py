#!/usr/bin/env python3
"""
Full Production Pipeline: Extended Workbook + Qwen Images + B&W Edition
Generates complete 80+ page books with illustrations in both Color and B&W
"""

import os
import sys
from pathlib import Path
from PIL import Image

# Add parent to path for imports
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from make_extended_workbooks import ExtendedWorkbookGenerator
from qwen_simple import SimpleQwenGenerator

OUT_DIR = ROOT / "real_books" / "output"
TMP_DIR = ROOT / "real_books" / "tmp_bw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(parents=True, exist_ok=True)


def gray_copy(src: Path) -> Path:
    """Convert image to grayscale for B&W edition"""
    dst = TMP_DIR / f"bw_{src.name}"
    with Image.open(src) as im:
        im.convert("L").save(dst)
    return dst


def build_full_book(theme, title, subtitle, age_range="3-6"):
    """Complete pipeline: images + color book + B&W book"""
    
    print(f"\n{'='*60}")
    print(f"BUILDING: {title}")
    print(f"{'='*60}\n")
    
    # Step 1: Generate Qwen images
    print("🎨 Step 1: Generating Qwen images...")
    g = SimpleQwenGenerator()
    g.request_delay_sec = int(os.getenv("QWEN_REQUEST_DELAY_SEC", "18"))
    g.max_retries = int(os.getenv("QWEN_MAX_RETRIES", "5"))
    
    # Get words for theme
    gen = ExtendedWorkbookGenerator(title, subtitle, theme, age_range)
    words = gen.words
    
    image_files = []
    for i, (word, sentence) in enumerate(words, 1):
        prompt = f"cute children's book illustration of {word}, {theme} theme, friendly characters, bright colors, simple background"
        filename = g.generate_image(prompt, f"{theme}_extended_{word}")
        if filename:
            image_files.append(filename)
            print(f"  ✅ Image {i}/{len(words)}: {word}")
        else:
            print(f"  ⚠️  Failed: {word}")
    
    print(f"\n📚 Step 2: Building COLOR edition...")
    pdf_color = gen.generate(image_files)
    print(f"  ✅ Color: {pdf_color}")
    
    print(f"\n🖤 Step 3: Building B&W edition...")
    # Convert images to B&W
    bw_images = [gray_copy(Path(f)) for f in image_files]
    
    # Generate B&W version (reuse generator with B&W images)
    gen_bw = ExtendedWorkbookGenerator(f"{title} (B&W Edition)", subtitle, theme, age_range)
    pdf_bw = gen_bw.generate([str(f) for f in bw_images])
    # Rename to indicate B&W
    bw_final = OUT_DIR / f"{title.replace(' ', '_')}_Extended_BW.pdf"
    Path(pdf_bw).rename(bw_final)
    print(f"  ✅ B&W: {bw_final}")
    
    return pdf_color, str(bw_final)


def main():
    books_to_build = [
        ("dinosaurs", "Dinosaurs Writing Skills Workbook", "Complete Handwriting Practice with Dino Friends", "3-6"),
        ("princess", "Princess Writing Skills Workbook", "Complete Handwriting Practice with Royal Friends", "3-6"),
    ]
    
    results = []
    for theme, title, subtitle, age in books_to_build:
        try:
            color_pdf, bw_pdf = build_full_book(theme, title, subtitle, age)
            results.append((title, color_pdf, bw_pdf))
        except Exception as e:
            print(f"❌ Error building {title}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("PRODUCTION COMPLETE")
    print(f"{'='*60}")
    for title, color, bw in results:
        print(f"\n📖 {title}")
        print(f"   Color: {color}")
        print(f"   B&W:   {bw}")


if __name__ == "__main__":
    main()
