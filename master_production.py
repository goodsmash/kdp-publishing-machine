#!/usr/bin/env python3
"""
KDP Publishing Machine - Master Production Script
Generates complete book packages (interior + cover + metadata) for KDP
"""

import os
import subprocess
import sys
from datetime import datetime

# Book production queue - add new books here
PRODUCTION_QUEUE = [
    # (story_key, language, size, cover_bg, cover_icon)
    ("brave_seed", "en", "8x10", "forest", "seed"),
    ("semilla_valiente", "es", "8x10", "forest", "seed"),
    ("luna_moon", "en", "8x10", "night", "moon"),
    ("benny_bear", "en", "8x10", "candy", "honey"),
    ("mia_rainbow", "en", "8x10", "spring", "rainbow"),
    ("sammy_shell", "en", "8x10", "ocean", "shell"),
]

def run_production_batch():
    """Run the full production pipeline"""
    
    print("=" * 60)
    print("  KDP PUBLISHING MACHINE - FULL PRODUCTION")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Books in queue: {len(PRODUCTION_QUEUE)}")
    print("=" * 60)
    
    success_count = 0
    
    for i, (story, lang, size, bg, icon) in enumerate(PRODUCTION_QUEUE, 1):
        print(f"\n{'─' * 60}")
        print(f"BOOK {i}/{len(PRODUCTION_QUEUE)}: {story} ({lang.upper()})")
        print('─' * 60)
        
        # Generate interior PDF
        print("\n📄 Generating interior PDF...")
        result = subprocess.run(
            ["python3", "publishing_machine.py", story, lang, size],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Error generating interior: {result.stderr}")
            continue
        
        print(result.stdout)
        
        # Get title from output (hacky but works)
        title_line = [line for line in result.stdout.split('\n') if 'Generated:' in line]
        if title_line:
            book_file = title_line[0].replace('Generated:', '').strip()
        else:
            book_file = f"output/{story.replace('_', ' ').title().replace(' ', '_')}_{size}.pdf"
        
        # Generate cover
        print("\n🎨 Generating cover...")
        
        # Extract title from story key for cover
        title_map = {
            "brave_seed": "The Brave Little Seed",
            "semilla_valiente": "La Semillita Valiente",
            "luna_moon": "Luna and the Moon",
            "benny_bear": "Benny Bear's First Honey",
            "mia_rainbow": "Mia Chases the Rainbow",
            "sammy_shell": "Sammy Finds His Shell",
        }
        
        subtitle_map = {
            "brave_seed": "A Story About Growing",
            "semilla_valiente": "Una Historia Sobre Crecer",
            "luna_moon": "A Bedtime Story",
            "benny_bear": "A Story About Trying New Things",
            "mia_rainbow": "A Story About Colors",
            "sammy_shell": "A Story About Being Yourself",
        }
        
        title = title_map.get(story, story.replace('_', ' ').title())
        subtitle = subtitle_map.get(story, "")
        
        cover_result = subprocess.run(
            ["python3", "cover_generator.py", title, subtitle, bg, icon],
            capture_output=True,
            text=True
        )
        
        if cover_result.returncode != 0:
            print(f"❌ Error generating cover: {cover_result.stderr}")
        else:
            print(cover_result.stdout)
        
        success_count += 1
        print(f"\n✅ Book {i} complete!")
    
    # Summary
    print("\n" + "=" * 60)
    print("  PRODUCTION SUMMARY")
    print("=" * 60)
    print(f"Books generated: {success_count}/{len(PRODUCTION_QUEUE)}")
    print(f"\nOutput files:")
    print(f"  📁 output/ - Interior PDFs + metadata JSON")
    print(f"  📁 covers/ - Cover PDFs")
    print("\nNext steps:")
    print("  1. Review all PDFs in output/ and covers/")
    print("  2. Upload interiors to KDP (Paperback content)")
    print("  3. Upload covers to KDP (Cover Creator)")
    print("  4. Order proof copies")
    print("  5. Publish!")
    print("=" * 60)


def generate_kimi_batch():
    """Generate prompts for AI story creation"""
    print("=" * 60)
    print("  GENERATING KIMI AI PROMPTS")
    print("=" * 60)
    
    # Generate 20 prompts for each language
    for lang in ["en", "es"]:
        print(f"\nGenerating 20 prompts in {lang.upper()}...")
        result = subprocess.run(
            ["python3", "story_generator.py", lang, "20"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    
    print("\n✅ Prompts saved to prompts/ folder")
    print("Copy these to kimi.com to generate unique stories!")


def show_stats():
    """Show current production stats"""
    print("=" * 60)
    print("  KDP PUBLISHING MACHINE - STATS")
    print("=" * 60)
    
    # Count files in each directory
    dirs = {
        "Interior PDFs": "output",
        "Covers": "covers", 
        "Kimi Prompts": "prompts",
        "Story Templates": "."
    }
    
    for name, path in dirs.items():
        if os.path.exists(path):
            if path == ".":
                py_files = len([f for f in os.listdir() if f.endswith('.py')])
                print(f"{name}: {py_files} files")
            else:
                files = os.listdir(path)
                count = len(files)
                print(f"{name}: {count} files")
                # Show PDFs specifically
                pdfs = [f for f in files if f.endswith('.pdf')]
                if pdfs:
                    for pdf in pdfs[:5]:  # Show first 5
                        size = os.path.getsize(os.path.join(path, pdf)) / 1024
                        print(f"  • {pdf} ({size:.1f} KB)")
                    if len(pdfs) > 5:
                        print(f"  ... and {len(pdfs) - 5} more")
        else:
            print(f"{name}: Not created yet")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("KDP Publishing Machine - Master Control")
        print("\nUsage:")
        print("  python3 master_production.py build    - Build all books in queue")
        print("  python3 master_production.py kimi     - Generate AI story prompts")
        print("  python3 master_production.py stats    - Show production stats")
        print("  python3 master_production.py all      - Build + Generate prompts")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "build":
        run_production_batch()
    elif command == "kimi":
        generate_kimi_batch()
    elif command == "stats":
        show_stats()
    elif command == "all":
        run_production_batch()
        print("\n")
        generate_kimi_batch()
    else:
        print(f"Unknown command: {command}")
        print("Use: build, kimi, stats, or all")
