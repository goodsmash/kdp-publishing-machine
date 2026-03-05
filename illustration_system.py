#!/usr/bin/env python3
"""
KDP Illustration System
Generates AI image prompts and integrates illustrations into books
Supports: DALL-E, Midjourney, Stable Diffusion prompts
"""

import os
import json
from datetime import datetime

class IllustrationSystem:
    """Generate professional illustration prompts for children's books"""
    
    # Art style templates for consistency
    ART_STYLES = {
        "watercolor": {
            "name": "Watercolor Children's Book",
            "description": "Soft watercolor illustrations with gentle washes, perfect for bedtime and nature stories",
            "prompt_prefix": "Watercolor children's book illustration, soft pastel colors, gentle brush strokes, whimsical style, ",
            "prompt_suffix": ", white background, no text, professional children's book art",
            "negative_prompt": "photorealistic, 3d render, dark colors, scary, complex background, text, watermark"
        },
        "cartoon": {
            "name": "Cartoon Style",
            "description": "Bright, bold cartoon illustrations perfect for ages 3-7",
            "prompt_prefix": "Cartoon illustration for children, bright colors, bold outlines, cute character design, ",
            "prompt_suffix": ", simple background, cheerful, professional children's illustration",
            "negative_prompt": "realistic, scary, dark, photorealistic, complex, text"
        },
        "cut_paper": {
            "name": "Cut Paper Collage",
            "description": "Textured cut-paper style with layered elements",
            "prompt_prefix": "Cut paper collage illustration, textured paper layers, ",
            "prompt_suffix": ", craft paper texture, children's book style, clean composition",
            "negative_prompt": "digital art, smooth, photorealistic, 3d"
        },
        "pencil": {
            "name": "Colored Pencil",
            "description": "Soft colored pencil illustrations with sketchy, hand-drawn feel",
            "prompt_prefix": "Colored pencil illustration, hand-drawn style, soft shading, ",
            "prompt_suffix": ", children's book art, textured paper, gentle colors",
            "negative_prompt": "digital, vector, sharp edges, photorealistic"
        },
        "digital_paint": {
            "name": "Digital Painting",
            "description": "Clean digital paintings with rich colors",
            "prompt_prefix": "Digital painting for children's book, rich colors, clean lines, ",
            "prompt_suffix": ", professional illustration, vibrant but not overwhelming",
            "negative_prompt": "photorealistic, 3d render, dark, scary"
        }
    }
    
    def __init__(self, book_title, art_style="watercolor"):
        self.book_title = book_title
        self.style = self.ART_STYLES[art_style]
        self.illustrations = []
        os.makedirs("illustrations/prompts", exist_ok=True)
        os.makedirs("illustrations/images", exist_ok=True)
        
    def add_illustration(self, page_num, description, scene_details, characters=None, mood="cheerful"):
        """Add an illustration specification"""
        
        illustration = {
            "page": page_num,
            "description": description,
            "scene": scene_details,
            "characters": characters or [],
            "mood": mood,
            "prompts": self._generate_prompts(description, scene_details, characters, mood)
        }
        
        self.illustrations.append(illustration)
        return illustration
    
    def _generate_prompts(self, description, scene, characters, mood):
        """Generate AI prompts in different formats"""
        
        # Build character description
        char_desc = ""
        if characters:
            char_desc = " featuring " + ", ".join([f"a cute {c}" for c in characters])
        
        # Base scene description
        base_scene = f"{description}, {scene}, {mood} atmosphere"
        
        prompts = {
            "dalle": {
                "model": "DALL-E 3",
                "prompt": f"{self.style['prompt_prefix']}{base_scene}{char_desc}{self.style['prompt_suffix']}",
                "size": "1024x1024",
                "style": "vivid" if mood == "exciting" else "natural"
            },
            "midjourney": {
                "model": "Midjourney V6",
                "prompt": f"{self.style['prompt_prefix']}{base_scene}{char_desc}{self.style['prompt_suffix']} --ar 3:4 --style raw --s 250",
                "parameters": "--ar 3:4 --style raw --s 250 --no text, watermark, signature"
            },
            "stable_diffusion": {
                "model": "SDXL 1.0",
                "prompt": f"{self.style['prompt_prefix']}{base_scene}{char_desc}{self.style['prompt_suffix']}",
                "negative_prompt": self.style['negative_prompt'],
                "steps": 30,
                "cfg_scale": 7.5,
                "size": "768x1024"
            },
            "leonardo": {
                "model": "Leonardo AI",
                "prompt": f"{self.style['prompt_prefix']}{base_scene}{char_desc}{self.style['prompt_suffix']}",
                "negative_prompt": self.style['negative_prompt'],
                "style": "Children's Book Illustration",
                "alchemy": True
            }
        }
        
        return prompts
    
    def export_prompts(self, format="all"):
        """Export illustration prompts to files"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"illustrations/prompts/{self.book_title.replace(' ', '_')}_{timestamp}"
        
        files_created = []
        
        # JSON export
        json_file = f"{base_filename}.json"
        with open(json_file, 'w') as f:
            json.dump({
                "book_title": self.book_title,
                "art_style": self.style['name'],
                "illustrations": self.illustrations
            }, f, indent=2)
        files_created.append(json_file)
        
        # Text export for easy copying
        txt_file = f"{base_filename}.txt"
        with open(txt_file, 'w') as f:
            f.write(f"{'='*70}\n")
            f.write(f"ILLUSTRATION PROMPTS FOR: {self.book_title}\n")
            f.write(f"Art Style: {self.style['name']}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{'='*70}\n\n")
            
            for ill in self.illustrations:
                f.write(f"\n{'─'*70}\n")
                f.write(f"PAGE {ill['page']}: {ill['description']}\n")
                f.write(f"{'─'*70}\n\n")
                
                f.write(f"Scene: {ill['scene']}\n")
                f.write(f"Mood: {ill['mood']}\n")
                if ill['characters']:
                    f.write(f"Characters: {', '.join(ill['characters'])}\n")
                f.write(f"\n")
                
                # DALL-E
                f.write(f"🎨 DALL-E 3:\n")
                f.write(f"   {ill['prompts']['dalle']['prompt']}\n\n")
                
                # Midjourney
                f.write(f"🎨 MIDJOURNEY:\n")
                f.write(f"   {ill['prompts']['midjourney']['prompt']}\n\n")
                
                # Stable Diffusion
                f.write(f"🎨 STABLE DIFFUSION:\n")
                f.write(f"   Prompt: {ill['prompts']['stable_diffusion']['prompt']}\n")
                f.write(f"   Negative: {ill['prompts']['stable_diffusion']['negative_prompt']}\n\n")
        
        files_created.append(txt_file)
        
        # Markdown for documentation
        md_file = f"{base_filename}.md"
        with open(md_file, 'w') as f:
            f.write(f"# Illustration Prompts: {self.book_title}\n\n")
            f.write(f"**Art Style:** {self.style['name']}\n\n")
            f.write(f"**Total Illustrations:** {len(self.illustrations)}\n\n")
            
            for ill in self.illustrations:
                f.write(f"## Page {ill['page']}: {ill['description']}\n\n")
                f.write(f"**Scene:** {ill['scene']}\n\n")
                f.write(f"**Mood:** {ill['mood']}\n\n")
                
                f.write(f"### DALL-E 3\n\n")
                f.write(f"```\n{ill['prompts']['dalle']['prompt']}\n```\n\n")
                
                f.write(f"### Midjourney\n\n")
                f.write(f"```\n{ill['prompts']['midjourney']['prompt']}\n```\n\n")
                
                f.write(f"### Stable Diffusion\n\n")
                f.write(f"**Prompt:**\n")
                f.write(f"```\n{ill['prompts']['stable_diffusion']['prompt']}\n```\n\n")
                f.write(f"**Negative Prompt:**\n")
                f.write(f"```\n{ill['prompts']['stable_diffusion']['negative_prompt']}\n```\n\n")
                f.write(f"---\n\n")
        
        files_created.append(md_file)
        
        print(f"✅ Exported {len(self.illustrations)} illustration prompts:")
        for f in files_created:
            print(f"   📄 {f}")
        
        return files_created
    
    def generate_illustration_guide(self):
        """Generate a complete illustration guide for the book"""
        
        guide = {
            "book_title": self.book_title,
            "art_style": self.style['name'],
            "style_description": self.style['description'],
            "total_illustrations": len(self.illustrations),
            "specifications": {
                "resolution": "300 DPI minimum",
                "color_mode": "CMYK for print",
                "file_format": "PNG or TIFF with transparency",
                "bleed": "0.125 inches if extending to edge",
                "safe_zone": "Keep important elements 0.5 inches from trim"
            },
            "consistency_notes": [
                "Maintain same art style across all illustrations",
                "Keep character designs consistent (save reference images)",
                "Use consistent color palette throughout",
                "Ensure text areas remain clear for overlay",
            ],
            "illustrations": self.illustrations
        }
        
        guide_file = f"illustrations/{self.book_title.replace(' ', '_')}_illustration_guide.json"
        with open(guide_file, 'w') as f:
            json.dump(guide, f, indent=2)
        
        print(f"✅ Illustration guide created: {guide_file}")
        return guide_file


def create_book_illustrations(book_key, book_data, art_style="watercolor"):
    """Create complete illustration set for a book"""
    
    title = book_data['title']
    system = IllustrationSystem(title, art_style)
    
    # Parse chapters to find illustration opportunities
    page_num = 0
    for chapter in book_data['chapters']:
        if chapter['type'] == 'illustration':
            page_num += 1
            desc = chapter['desc']
            
            # Create scene details based on description
            scene_details = generate_scene_details(desc, book_data)
            characters = extract_characters(desc, book_data)
            
            system.add_illustration(
                page_num=page_num,
                description=desc.replace('_', ' ').title(),
                scene_details=scene_details,
                characters=characters,
                mood=determine_mood(desc, book_data)
            )
        elif chapter['type'] in ['title_page', 'copyright', 'dedication']:
            page_num += 1
    
    # Export everything
    system.export_prompts()
    system.generate_illustration_guide()
    
    return system


def generate_scene_details(desc, book_data):
    """Generate detailed scene description from illustration description"""
    
    # Map common illustration descriptions to detailed scenes
    scene_map = {
        "seed_on_flower": "tiny brown seed sitting on a colorful flower petal, sun shining, garden background",
        "wind_coming": "wind blowing through a garden, flowers bending, leaves swirling, dynamic movement",
        "seed_falling": "seed tumbling through the air, spinning, blue sky background, motion blur",
        "ground": "seed landing in rich brown soil, garden setting, warm earth tones",
        "waiting": "seed underground with roots beginning to form, rain drops above, patience",
        "sprout": "tiny green sprout pushing through soil, first leaves unfurling, morning light",
        "flower": "beautiful blooming flower, colorful petals open, sun shining, garden setting",
        "luna_on_branch": "cute gray owl on oak tree branch, night sky, stars beginning to appear",
        "moon_rising": "full moon rising over forest, silver glow, twilight colors",
        "owl_whispering": "owl with big eyes, tree branches, soft wind",
        "starry_sky": "night sky filled with stars, crescent moon, deep blue and purple",
        "sleeping": "owl tucked in tree hollow, peaceful sleeping pose, soft moonlight",
        "bear": "friendly brown bear in forest, curious expression",
        "tree": "tall tree with beehive, honey dripping, forest background",
        "honey": "golden honeycomb, bees flying, warm sunlight",
        "rainbow": "colorful rainbow across sky, green meadow, bright sunshine",
        "crab": "small hermit crab on sandy beach, ocean waves, seashells",
        "shell": "beautiful spiral seashell with blue and green swirls",
    }
    
    return scene_map.get(desc, desc.replace('_', ' '))


def extract_characters(desc, book_data):
    """Extract characters from illustration description"""
    
    characters = []
    
    # Check for known characters
    if 'seed' in desc or 'sprout' in desc:
        characters.append('tiny seed')
    if 'luna' in desc or 'owl' in desc:
        characters.append('little gray owl')
    if 'benny' in desc or 'bear' in desc:
        characters.append('brown bear cub')
    if 'mia' in desc or 'dog' in desc or 'puppy' in desc:
        characters.append('golden puppy')
    if 'sammy' in desc or 'crab' in desc:
        characters.append('small hermit crab')
    
    return characters


def determine_mood(desc, book_data):
    """Determine the mood of the illustration"""
    
    mood_map = {
        'sleeping': 'peaceful',
        'night': 'calm',
        'moon': 'peaceful',
        'rainbow': 'joyful',
        'honey': 'excited',
        'adventure': 'exciting',
        'falling': 'scary',
        'waiting': 'patient',
    }
    
    for key, mood in mood_map.items():
        if key in desc.lower():
            return mood
    
    return 'cheerful'


if __name__ == "__main__":
    import sys
    
    # Example usage
    if len(sys.argv) > 1:
        book = sys.argv[1]
        style = sys.argv[2] if len(sys.argv) > 2 else "watercolor"
        
        # Load book data (would need to import from publishing_machine)
        print(f"Creating illustration set for: {book}")
        print(f"Art style: {style}")
        print("\nTo use this system:")
        print("1. Import your book data from publishing_machine")
        print("2. Call create_book_illustrations(book_key, book_data, art_style)")
        print("3. Use generated prompts in DALL-E, Midjourney, or Stable Diffusion")
        print("4. Save images to illustrations/images/ folder")
        print("5. Rebuild PDF with images embedded")
    else:
        print("KDP Illustration System")
        print("\nUsage:")
        print("  python3 illustration_system.py [book_key] [art_style]")
        print("\nArt styles:")
        for key, style in IllustrationSystem.ART_STYLES.items():
            print(f"  {key}: {style['name']}")
