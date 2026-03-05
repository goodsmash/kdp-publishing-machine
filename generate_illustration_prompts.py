#!/usr/bin/env python3
"""
Generate illustration prompts for all existing books
"""

import sys
sys.path.insert(0, '/home/goodsmash/.openclaw/workspace/kdp-publishing-machine')

from publishing_machine import STORY_LIBRARY
from illustration_system import IllustrationSystem, generate_scene_details, extract_characters, determine_mood

def generate_all_illustration_prompts():
    """Generate illustration prompts for all books in the library"""
    
    print("="*70)
    print("KDP ILLUSTRATION PROMPT GENERATOR")
    print("="*70)
    print()
    
    art_style = "watercolor"  # Best for children's books
    
    for lang in ["en", "es"]:
        if lang not in STORY_LIBRARY:
            continue
            
        print(f"\n{'='*70}")
        print(f"LANGUAGE: {lang.upper()}")
        print('='*70)
        
        for book_key, book_data in STORY_LIBRARY[lang].items():
            title = book_data['title']
            print(f"\n📚 {title}")
            print("-" * 70)
            
            # Create illustration system for this book
            system = IllustrationSystem(title, art_style)
            
            # Parse chapters to find illustration opportunities
            page_num = 0
            ill_count = 0
            
            for chapter in book_data['chapters']:
                if chapter['type'] == 'illustration':
                    page_num += 1
                    ill_count += 1
                    desc = chapter['desc']
                    
                    # Create scene details
                    scene_details = generate_scene_details(desc, book_data)
                    characters = extract_characters(desc, book_data)
                    mood = determine_mood(desc, book_data)
                    
                    system.add_illustration(
                        page_num=page_num,
                        description=desc.replace('_', ' ').title(),
                        scene_details=scene_details,
                        characters=characters,
                        mood=mood
                    )
                elif chapter['type'] in ['title_page', 'copyright', 'dedication', 'the_end']:
                    page_num += 1
                elif chapter['type'] in ['text', 'vocab']:
                    page_num += 1
            
            # Export prompts
            if ill_count > 0:
                system.export_prompts()
                system.generate_illustration_guide()
                print(f"   ✅ {ill_count} illustrations generated")
            else:
                print(f"   ℹ️ No illustrations in this book")
    
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Check illustrations/prompts/ folder for all prompts")
    print("2. Copy prompts to your AI tool:")
    print("   • ChatGPT + DALL-E")
    print("   • Midjourney on Discord")
    print("   • Leonardo.ai (free option)")
    print("   • Stable Diffusion locally")
    print("3. Save generated images to illustrations/images/")
    print("4. Run: python3 rebuild_with_images.py")


if __name__ == "__main__":
    generate_all_illustration_prompts()
