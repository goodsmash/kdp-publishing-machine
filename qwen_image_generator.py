#!/usr/bin/env python3
"""
Alibaba Qwen Image Generator for KDP Books
Uses Qwen-image-2.0-pro to generate illustrations automatically
"""

import os
import json
import base64
from datetime import datetime

# API Configuration
API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
MODEL = "qwen-image-2.0-pro-2026-03-03"

try:
    from alibabacloud_bailian20231229.client import Client
    from alibabacloud_bailian20231229.models import *
    from alibabacloud_tea_openapi.models import Config
    HAS_SDK = True
except ImportError:
    HAS_SDK = False
    print("⚠️  Alibaba SDK not installed. Install with: pip install alibabacloud-bailian20231229")

class QwenImageGenerator:
    """Generate illustrations using Alibaba Qwen API"""
    
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.model = MODEL
        self.output_dir = "illustrations/qwen_generated"
        os.makedirs(self.output_dir, exist_ok=True)
        
        if HAS_SDK:
            # Initialize client
            config = Config(
                access_key_id=api_key,
                access_key_secret=api_key,
                endpoint="bailian.aliyuncs.com"
            )
            self.client = Client(config)
        else:
            self.client = None
            print("SDK not available - will use prompts only mode")
    
    def generate_image(self, prompt, book_name, page_num, size="1024x1024"):
        """Generate a single image using Qwen API"""
        
        if not HAS_SDK or not self.client:
            print(f"⚠️  Cannot generate image - SDK not available")
            print(f"   Prompt: {prompt[:60]}...")
            return None
        
        try:
            # Enhance prompt for children's book style
            enhanced_prompt = f"Children's book illustration, digital art, friendly and warm, {prompt}, cute characters, bright colors, simple background, professional children's book art style, no text"
            
            # Prepare request
            request = {
                "model": self.model,
                "input": {
                    "prompt": enhanced_prompt,
                    "size": size,
                    "n": 1
                }
            }
            
            print(f"🎨 Generating image for {book_name} page {page_num}...")
            print(f"   Prompt: {enhanced_prompt[:80]}...")
            
            # Call API
            response = self.client.generate_image(request)
            
            if response and response.body and response.body.images:
                # Save image
                image_data = response.body.images[0].base64
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/{book_name.replace(' ', '_')}_page{page_num:02d}_{timestamp}.png"
                
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(image_data))
                
                print(f"   ✅ Saved: {filename}")
                return filename
            else:
                print(f"   ❌ No image in response")
                return None
                
        except Exception as e:
            print(f"   ❌ Error generating image: {e}")
            return None
    
    def generate_book_illustrations(self, book_key, book_data):
        """Generate all illustrations for a book"""
        
        print(f"\n{'='*60}")
        print(f"GENERATING ILLUSTRATIONS FOR: {book_data['title']}")
        print(f"{'='*60}\n")
        
        illustrations = []
        page_num = 0
        ill_count = 0
        
        for chapter in book_data['chapters']:
            if chapter['type'] == 'illustration':
                page_num += 1
                ill_count += 1
                
                # Get scene description
                desc = chapter['desc']
                scene = self.get_scene_description(desc, book_data)
                
                # Generate prompt
                prompt = f"{scene}, children's book illustration, cute, colorful"
                
                # Generate image
                image_path = self.generate_image(
                    prompt=prompt,
                    book_name=book_data['title'],
                    page_num=page_num
                )
                
                if image_path:
                    illustrations.append({
                        "page": page_num,
                        "description": desc,
                        "prompt": prompt,
                        "image_path": image_path
                    })
            elif chapter['type'] in ['title_page', 'copyright', 'dedication', 'the_end']:
                page_num += 1
            elif chapter['type'] in ['text', 'vocab']:
                page_num += 1
        
        # Save manifest
        manifest_file = f"{self.output_dir}/{book_data['title'].replace(' ', '_')}_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump({
                "book_title": book_data['title'],
                "total_illustrations": len(illustrations),
                "generated_at": datetime.now().isoformat(),
                "illustrations": illustrations
            }, f, indent=2)
        
        print(f"\n✅ Generated {len(illustrations)} illustrations")
        print(f"   Manifest: {manifest_file}")
        
        return illustrations
    
    def get_scene_description(self, desc, book_data):
        """Convert illustration description to detailed scene"""
        
        scene_map = {
            "seed_on_flower": "tiny brown seed sitting on a colorful flower petal, sun shining, garden background",
            "wind_coming": "wind blowing through a garden, flowers bending, leaves swirling",
            "seed_falling": "seed tumbling through the air, spinning, blue sky background",
            "ground": "seed landing in rich brown soil, garden setting",
            "waiting": "seed underground with roots beginning, rain drops above",
            "sprout": "tiny green sprout pushing through soil, first leaves unfurling",
            "flower": "beautiful blooming flower, colorful petals open, sun shining",
            "luna_on_branch": "cute gray owl on oak tree branch, night sky, stars",
            "moon_rising": "full moon rising over forest, silver glow, twilight",
            "owl_whispering": "owl with big eyes, tree branches, soft wind",
            "starry_sky": "night sky filled with stars, crescent moon, deep blue",
            "sleeping": "owl tucked in tree hollow, peaceful sleeping, moonlight",
            "bear": "friendly brown bear in forest, curious expression",
            "tree": "tall tree with beehive, honey dripping, forest background",
            "honey": "golden honeycomb, bees flying, warm sunlight",
            "rainbow": "colorful rainbow across sky, green meadow, sunshine",
            "crab": "small hermit crab on sandy beach, ocean waves, seashells",
            "shell": "beautiful spiral seashell with blue and green swirls",
        }
        
        return scene_map.get(desc, desc.replace('_', ' '))


def generate_all_illustrations():
    """Generate illustrations for all books"""
    
    print("="*60)
    print("ALIBABA QWEN IMAGE GENERATOR")
    print("="*60)
    print(f"Model: {MODEL}")
    print(f"Output: illustrations/qwen_generated/")
    print("="*60)
    
    if not HAS_SDK:
        print("\n⚠️  SDK not installed!")
        print("Install with: pip install alibabacloud-bailian20231229")
        return
    
    # Import book data
    try:
        from publishing_machine import STORY_LIBRARY
    except ImportError:
        print("\n❌ Cannot load book data")
        return
    
    generator = QwenImageGenerator()
    
    # Generate for all books
    for lang in ["en"]:
        if lang not in STORY_LIBRARY:
            continue
        
        for book_key, book_data in STORY_LIBRARY[lang].items():
            # Skip if already has illustrations
            manifest_file = f"illustrations/qwen_generated/{book_data['title'].replace(' ', '_')}_manifest.json"
            if os.path.exists(manifest_file):
                print(f"\n⏭️  Skipping {book_data['title']} - already generated")
                continue
            
            generator.generate_book_illustrations(book_key, book_data)
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test with a single prompt
        print("Testing Qwen image generation...")
        generator = QwenImageGenerator()
        
        if HAS_SDK:
            result = generator.generate_image(
                prompt="cute brown teddy bear sitting in a sunny meadow with flowers",
                book_name="Test",
                page_num=1
            )
            if result:
                print(f"✅ Test successful! Image saved to: {result}")
            else:
                print("❌ Test failed")
        else:
            print("SDK not available for testing")
    else:
        generate_all_illustrations()
