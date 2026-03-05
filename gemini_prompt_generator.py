#!/usr/bin/env python3
"""
Google Nano Banana 2 (Gemini) Prompt Generator
Optimized for Google's image generation model
"""

import os
import json
from datetime import datetime

class GeminiPromptGenerator:
    """Generate prompts optimized for Google Gemini Nano image generation"""
    
    # Gemini Nano 2 specific style guidance
    STYLE_GUIDE = {
        "base": "Children's book illustration, digital art, friendly and warm,",
        "lighting": "soft natural lighting, gentle shadows,",
        "colors": "bright cheerful colors, pastel background,",
        "characters": "cute friendly characters, big expressive eyes, simple shapes,",
        "composition": "centered subject, clear focal point, uncluttered background",
        "negative": "no scary elements, no dark colors, no realistic textures, no text, no watermarks"
    }
    
    # Scene templates for each book
    BOOK_SCENES = {
        "The Brave Little Seed": [
            {
                "page": 4,
                "scene": "tiny brown seed sitting on pink flower petal",
                "setting": "sunny garden with green leaves",
                "mood": "peaceful and safe",
                "colors": "soft pink, green, warm yellow sunlight"
            },
            {
                "page": 7,
                "scene": "wind blowing through flowers",
                "setting": "garden with bending flowers and swirling leaves",
                "mood": "gentle movement",
                "colors": "green, blue sky, white clouds"
            },
            {
                "page": 11,
                "scene": "small seed falling through blue sky",
                "setting": "blue sky with fluffy white clouds",
                "mood": "floating gently down",
                "colors": "bright blue, white clouds, brown seed"
            },
            {
                "page": 16,
                "scene": "seed resting in brown soil underground",
                "setting": "cross-section showing soil layers",
                "mood": "cozy and safe",
                "colors": "rich brown, dark earthy tones"
            },
            {
                "page": 21,
                "scene": "rain falling on soil with sun peeking through",
                "setting": "garden with raindrops and sun rays",
                "mood": "nurturing and warm",
                "colors": "blue rain, yellow sun, green plants"
            },
            {
                "page": 25,
                "scene": "tiny green sprout pushing through soil",
                "setting": "close-up of sprout emerging",
                "mood": "hopeful and new",
                "colors": "bright green, brown soil, golden light"
            },
            {
                "page": 28,
                "scene": "small plant growing taller with leaves",
                "setting": "garden with growing plant",
                "mood": "growing strong",
                "colors": "green leaves, brown stem, blue sky"
            },
            {
                "page": 32,
                "scene": "beautiful blooming flower with colorful petals",
                "setting": "garden with fully bloomed flower",
                "mood": "joyful and proud",
                "colors": "vibrant pink petals, yellow center, green leaves"
            }
        ],
        "Luna and the Moon": [
            {
                "page": 4,
                "scene": "cute gray owl sitting on tree branch",
                "setting": "tall oak tree at twilight",
                "mood": "calm and observant",
                "colors": "gray owl, brown tree, purple twilight sky"
            },
            {
                "page": 7,
                "scene": "full moon rising over forest",
                "setting": "silhouette of trees with big moon",
                "mood": "peaceful night",
                "colors": "silver moon, dark blue sky, black tree silhouettes"
            },
            {
                "page": 11,
                "scene": "owl with wind blowing through feathers",
                "setting": "tree branch with swirling leaves",
                "mood": "gentle and soft",
                "colors": "gray owl, green leaves, soft blue"
            },
            {
                "page": 16,
                "scene": "night sky filled with twinkling stars",
                "setting": "starry sky with crescent moon",
                "mood": "wonder and magic",
                "colors": "deep blue, white stars, silver moon"
            },
            {
                "page": 20,
                "scene": "owl sleeping in tree hollow",
                "setting": "cozy tree hole with soft moonlight",
                "mood": "sleepy and peaceful",
                "colors": "soft grays, gentle blue moonlight, warm browns"
            }
        ],
        "Benny Bear's First Honey": [
            {
                "page": 4,
                "scene": "small brown bear cub in cozy cave",
                "setting": "cave entrance with forest view",
                "mood": "curious and safe",
                "colors": "warm brown, green forest, golden light"
            },
            {
                "page": 7,
                "scene": "bear sniffing air with curious expression",
                "setting": "forest with flowers and trees",
                "mood": "curious and excited",
                "colors": "brown bear, green forest, colorful flowers"
            },
            {
                "page": 11,
                "scene": "tall tree with beehive and dripping honey",
                "setting": "forest with sun filtering through leaves",
                "mood": "enticing and golden",
                "colors": "golden honey, green leaves, brown tree, sun rays"
            },
            {
                "page": 16,
                "scene": "bear climbing tree with determination",
                "setting": "tree trunk with bear halfway up",
                "mood": "determined and brave",
                "colors": "brown bear, brown tree, green leaves, blue sky"
            },
            {
                "page": 20,
                "scene": "happy bear with honey on nose",
                "setting": "forest clearing with tree",
                "mood": "joyful and proud",
                "colors": "brown bear, golden honey, green grass, bright sun"
            }
        ],
        "Mia Chases the Rainbow": [
            {
                "page": 4,
                "scene": "golden puppy playing in meadow",
                "setting": "green meadow with flowers after rain",
                "mood": "playful and happy",
                "colors": "golden puppy, green grass, colorful flowers"
            },
            {
                "page": 7,
                "scene": "colorful rainbow across sky",
                "setting": "meadow with rainbow arching overhead",
                "mood": "wonderful and bright",
                "colors": "rainbow colors, blue sky, green meadow"
            },
            {
                "page": 11,
                "scene": "puppy running through tall grass",
                "setting": "meadow with rolling hills",
                "mood": "energetic and free",
                "colors": "golden puppy, green grass, blue sky"
            },
            {
                "page": 16,
                "scene": "puppy meeting another dog friend",
                "setting": "sunny field with two dogs",
                "mood": "friendly and warm",
                "colors": "two golden dogs, green grass, bright sun"
            },
            {
                "page": 20,
                "scene": "two dogs playing together under rainbow",
                "setting": "meadow with rainbow in sky",
                "mood": "friendship and joy",
                "colors": "rainbow, golden dogs, green meadow, blue sky"
            }
        ],
        "Sammy Finds His Shell": [
            {
                "page": 4,
                "scene": "small hermit crab on sandy beach",
                "setting": "beach with gentle waves and seashells",
                "mood": "searching and hopeful",
                "colors": "orange crab, tan sand, blue ocean, white shells"
            },
            {
                "page": 7,
                "scene": "plain brown shell on beach",
                "setting": "beach with various shells scattered",
                "mood": "ordinary and simple",
                "colors": "brown shell, tan sand, blue water"
            },
            {
                "page": 11,
                "scene": "sad crab looking at ocean",
                "setting": "beach with sunset colors",
                "mood": "lonely but hopeful",
                "colors": "orange crab, pink sunset, blue ocean"
            },
            {
                "page": 16,
                "scene": "sparkly shell with blue and green swirls",
                "setting": "coral reef area underwater",
                "mood": "magical and special",
                "colors": "blue and green shell, pink coral, blue water"
            },
            {
                "page": 20,
                "scene": "happy crab in beautiful shell",
                "setting": "beach with crab showing off shell",
                "mood": "proud and joyful",
                "colors": "colorful shell, orange crab, bright beach"
            }
        ],
        "La Semillita Valiente": [
            {
                "page": 4,
                "scene": "semilla marrón pequeña en pétalo rosa",
                "setting": "jardín soleado con hojas verdes",
                "mood": "pacífica y segura",
                "colors": "rosa suave, verde, luz amarilla cálida"
            },
            {
                "page": 7,
                "scene": "viento soplando flores en el jardín",
                "setting": "jardín con flores moviéndose y hojas girando",
                "mood": "movimiento gentil",
                "colors": "verde, cielo azul, nubes blancas"
            },
            {
                "page": 11,
                "scene": "semilla cayendo por el cielo azul",
                "setting": "cielo azul con nubes esponjosas",
                "mood": "flotando suavemente",
                "colors": "azul brillante, nubes blancas, semilla marrón"
            },
            {
                "page": 16,
                "scene": "semilla descansando en tierra marrón",
                "setting": "corte transversal mostrando capas de tierra",
                "mood": "acogedora y segura",
                "colors": "marrón rico, tonos tierra oscuros"
            },
            {
                "page": 21,
                "scene": "lluvia cayendo en tierra con sol asomando",
                "setting": "jardín con gotas de lluvia y rayos de sol",
                "mood": "nutritiva y cálida",
                "colors": "lluvia azul, sol amarillo, plantas verdes"
            },
            {
                "page": 25,
                "scene": "pequeño tallo verde emergiendo de la tierra",
                "setting": "primer plano de brote emergiendo",
                "mood": "esperanzadora y nueva",
                "colors": "verde brillante, tierra marrón, luz dorada"
            },
            {
                "page": 28,
                "scene": "planta pequeña creciendo con hojas",
                "setting": "jardín con planta creciendo",
                "mood": "creciendo fuerte",
                "colors": "hojas verdes, tallo marrón, cielo azul"
            },
            {
                "page": 32,
                "scene": "hermosa flor floreciendo con pétalos coloridos",
                "setting": "jardín con flor completamente abierta",
                "mood": "alegre y orgullosa",
                "colors": "pétalos rosa vibrante, centro amarillo, hojas verdes"
            }
        ]
    }
    
    def __init__(self, book_title):
        self.book_title = book_title
        self.scenes = self.BOOK_SCENES.get(book_title, [])
        os.makedirs("illustrations/gemini_prompts", exist_ok=True)
        
    def generate_gemini_prompt(self, scene_data):
        """Generate optimized prompt for Gemini Nano 2"""
        
        prompt = f"""{self.STYLE_GUIDE['base']} {scene_data['scene']}, {scene_data['setting']}, {self.STYLE_GUIDE['characters']} {self.STYLE_GUIDE['lighting']} {scene_data['colors']}, {self.STYLE_GUIDE['colors']} {self.STYLE_GUIDE['composition']}. {scene_data['mood']}."""
        
        return {
            "prompt": prompt,
            "negative_prompt": self.STYLE_GUIDE['negative'],
            "aspect_ratio": "3:4",
            "guidance": "High quality children's book illustration"
        }
    
    def generate_all_prompts(self):
        """Generate all prompts for the book"""
        
        prompts = []
        for scene in self.scenes:
            gemini_data = self.generate_gemini_prompt(scene)
            prompts.append({
                "page": scene['page'],
                "scene_description": scene['scene'],
                "gemini_prompt": gemini_data['prompt'],
                "negative_prompt": gemini_data['negative_prompt'],
                "tips": "Use high quality setting. Generate at 1024x1024."
            })
        
        return prompts
    
    def export(self):
        """Export prompts to file"""
        
        prompts = self.generate_all_prompts()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON export
        json_file = f"illustrations/gemini_prompts/{self.book_title.replace(' ', '_')}_gemini_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                "book": self.book_title,
                "model": "Google Gemini Nano 2",
                "total_images": len(prompts),
                "prompts": prompts
            }, f, indent=2)
        
        # Text export for easy copying
        txt_file = f"illustrations/gemini_prompts/{self.book_title.replace(' ', '_')}_gemini_{timestamp}.txt"
        with open(txt_file, 'w') as f:
            f.write(f"{'='*70}\n")
            f.write(f"GOOGLE GEMINI NANO 2 PROMPTS\n")
            f.write(f"Book: {self.book_title}\n")
            f.write(f"{'='*70}\n\n")
            
            f.write(f"MODEL: Google Gemini Nano 2 (Image Generation)\n")
            f.write(f"TOTAL IMAGES NEEDED: {len(prompts)}\n")
            f.write(f"RECOMMENDED SIZE: 1024x1024 pixels\n")
            f.write(f"STYLE: Children's book illustration\n\n")
            
            for i, p in enumerate(prompts, 1):
                f.write(f"\n{'─'*70}\n")
                f.write(f"IMAGE {i} of {len(prompts)} - PAGE {p['page']}\n")
                f.write(f"SCENE: {p['scene_description']}\n")
                f.write(f"{'─'*70}\n\n")
                
                f.write(f"PROMPT:\n")
                f.write(f"{p['gemini_prompt']}\n\n")
                
                f.write(f"AVOID (Negative):\n")
                f.write(f"{p['negative_prompt']}\n\n")
                
                f.write(f"TIPS: {p['tips']}\n")
        
        print(f"✅ Gemini prompts for '{self.book_title}'")
        print(f"   📄 {txt_file}")
        print(f"   📄 {json_file}")
        
        return txt_file, json_file


def generate_all_gemini_prompts():
    """Generate Gemini prompts for all books"""
    
    print("="*70)
    print("GOOGLE GEMINI NANO 2 PROMPT GENERATOR")
    print("="*70)
    print()
    
    books = [
        "The Brave Little Seed",
        "Luna and the Moon", 
        "Benny Bear's First Honey",
        "Mia Chases the Rainbow",
        "Sammy Finds His Shell",
        "La Semillita Valiente"
    ]
    
    all_files = []
    
    for book in books:
        print(f"\n📚 {book}")
        print("-" * 70)
        
        gen = GeminiPromptGenerator(book)
        if gen.scenes:
            txt, json = gen.export()
            all_files.append(txt)
            print(f"   {len(gen.scenes)} illustration prompts generated")
        else:
            print(f"   No scenes found for this book")
    
    print("\n" + "="*70)
    print("ALL PROMPTS GENERATED!")
    print("="*70)
    print(f"\nTotal: {len(all_files)} prompt files")
    print("\nHow to use with Google Gemini:")
    print("1. Open gemini.google.com")
    print("2. Enable image generation")
    print("3. Copy prompt from .txt file")
    print("4. Paste and generate")
    print("5. Download images at highest resolution")
    print("6. Save to illustrations/images/[book_name]/")
    
    return all_files


if __name__ == "__main__":
    generate_all_gemini_prompts()
