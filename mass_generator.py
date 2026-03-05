#!/usr/bin/env python3
"""
MASS Book Generator - Creates multiple comprehensive books at once
Themes: Animals, Princess, Superhero, Jungle, Farm, Christmas, Halloween
"""

import subprocess
import sys

# Extended themes for mass generation
MASS_THEMES = [
    # Activity Books
    {"type": "activity", "theme": "princess", "title": "Princess Activity Book", "subtitle": "Castles, Crowns, and Royal Fun!"},
    {"type": "activity", "theme": "superhero", "title": "Superhero Activity Book", "subtitle": "Powers, Missions, and Hero Adventures!"},
    {"type": "activity", "theme": "jungle", "title": "Jungle Safari Activity Book", "subtitle": "Lions, Tigers, and Wild Animals!"},
    {"type": "activity", "theme": "farm", "title": "Farm Friends Activity Book", "subtitle": "Cows, Pigs, Chickens, and Barnyard Fun!"},
    {"type": "activity", "theme": "pets", "title": "Pets Activity Book", "subtitle": "Cats, Dogs, and Furry Friends!"},
    
    # Workbooks
    {"type": "workbook", "title": "Alphabet Tracing Workbook", "subtitle": "Learn A-Z with Fun Activities"},
    {"type": "workbook", "title": "Number Tracing Workbook", "subtitle": "Counting 1-20 Made Easy"},
    {"type": "workbook", "title": "First Grade Prep Workbook", "subtitle": "Get Ready for School Success"},
    {"type": "workbook", "title": "Toddler Learning Workbook", "subtitle": "Colors, Shapes, and Early Skills"},
    
    # Story Books
    {"type": "story", "key": "brave_seed", "lang": "en"},
    {"type": "story", "key": "luna_moon", "lang": "en"},
    {"type": "story", "key": "benny_bear", "lang": "en"},
]

def generate_mass_books():
    """Generate all mass production books"""
    
    print("="*70)
    print("MASS BOOK PRODUCTION SYSTEM")
    print("="*70)
    print(f"Total books to generate: {len(MASS_THEMES)}")
    print()
    
    generated = []
    
    for i, book in enumerate(MASS_THEMES, 1):
        print(f"\n{'─'*70}")
        print(f"BOOK {i}/{len(MASS_THEMES)}: {book.get('title', book.get('theme', book.get('key')))}")
        print('─'*70)
        
        try:
            if book["type"] == "activity":
                result = subprocess.run(
                    ["python3", "comprehensive_activity_book.py", book["theme"]],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    print(f"   ✅ Activity book created")
                    generated.append(f"activity_{book['theme']}")
                else:
                    print(f"   ❌ Error: {result.stderr[:100]}")
                    
            elif book["type"] == "workbook":
                result = subprocess.run(
                    ["python3", "workbook_generator.py", book["title"], book["subtitle"]],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    print(f"   ✅ Workbook created")
                    generated.append(f"workbook_{book['title']}")
                else:
                    print(f"   ❌ Error: {result.stderr[:100]}")
                    
            elif book["type"] == "story":
                result = subprocess.run(
                    ["python3", "publishing_machine.py", book["key"], book["lang"], "8x10"],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    print(f"   ✅ Story book created")
                    generated.append(f"story_{book['key']}")
                else:
                    print(f"   ❌ Error: {result.stderr[:100]}")
                    
        except Exception as e:
            print(f"   ❌ Exception: {str(e)[:100]}")
    
    print("\n" + "="*70)
    print("MASS PRODUCTION COMPLETE")
    print("="*70)
    print(f"Successfully generated: {len(generated)}/{len(MASS_THEMES)} books")
    
    return generated

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick mode - just show count
        print(f"Ready to generate {len(MASS_THEMES)} books")
        print("Run without --quick to generate all")
    else:
        generate_mass_books()
