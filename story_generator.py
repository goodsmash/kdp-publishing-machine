#!/usr/bin/env python3
"""
Story Generator using Kimi API
Generates unlimited unique children's stories for KDP
"""

import os
import json
import re

# Story templates for batch generation
STORY_TEMPLATES = [
    {
        "theme": "friendship",
        "character_types": ["bunny", "squirrel", "bird", "mouse", "fox"],
        "settings": ["forest", "meadow", "garden", "park"],
        "conflicts": ["lost", "scared", "different", "shy"],
        "resolutions": ["teamwork", "kindness", "sharing", "helping"]
    },
    {
        "theme": "courage",
        "character_types": ["kitten", "puppy", "duckling", "fawn", "cub"],
        "settings": ["farm", "pond", "woods", "barn"],
        "conflicts": ["first_day", "storm", "dark", "new_place"],
        "resolutions": ["bravery", "trying", "practice", "believing"]
    },
    {
        "theme": "learning",
        "character_types": ["bear", "owl", "turtle", "elephant", "penguin"],
        "settings": ["school", "library", "home", "zoo"],
        "conflicts": ["hard_task", "mistake", "confused", "slow"],
        "resolutions": ["practice", "patience", "asking_help", "never_give_up"]
    }
]

VOCABULARY_POOLS = {
    "2-4": ["soft", "bright", "bouncy", "cozy", "giggly", "hoppy", "snuggly", "twinkly", "woozy", "zippy"],
    "5-7": ["curious", "determined", "fierce", "gentle", "mysterious", "remarkable", "splendid", "tremendous", "vivid", "whimsical"],
    "8-10": ["extraordinary", "magnificent", "perseverance", "spectacular", "treasure", "wonder", "adventure", "discovery", "imagination", "journey"]
}

SPANISH_VOCABULARY = {
    "2-4": ["suave", "brillante", "saltarín", "acogedor", "risueño", "saltón", "acurrucable", "centelleante", "mareado", "rápido"],
    "5-7": ["curioso", "determinado", "feroz", "gentil", "misterioso", "remarkable", "espléndido", "tremendo", "vívido", "caprichoso"],
    "8-10": ["extraordinario", "magnífico", "perseverancia", "espectacular", "tesoro", "maravilla", "aventura", "descubrimiento", "imaginación", "viaje"]
}

def generate_story_prompt(template, age_group, lang="en"):
    """Generate a Kimi prompt for a unique story"""
    
    character = random.choice(template["character_types"])
    setting = random.choice(template["settings"])
    conflict = random.choice(template["conflicts"])
    resolution = random.choice(template["resolutions"])
    
    if lang == "en":
        vocab_words = random.sample(VOCABULARY_POOLS[age_group], 6)
        prompt = f"""Write a children's picture book story for ages {age_group}.

Main character: A cute {character} named {generate_name('en')}
Setting: {setting}
Theme: {template['theme']}
Problem: The character is {conflict}
Solution: Learns about {resolution}

New vocabulary words to include (define each naturally in the story): {', '.join(vocab_words)}

Requirements:
- Simple, engaging sentences
- 500-800 words total
- 12-16 pages of story content
- Include dialogue
- Heartwarming ending
- Title that includes the character's name

Format as:
TITLE: [Story Title]

PAGE 1: [Text]
PAGE 2: [Text]
... etc

NEW WORDS:
word1: definition
word2: definition
..."""
    else:  # Spanish
        vocab_words = random.sample(SPANISH_VOCABULARY[age_group], 6)
        prompt = f"""Escribe un cuento infantil ilustrado para niños de {age_group} años.

Personaje principal: Un lindo {character} llamado {generate_name('es')}
Escenario: {setting}
Tema: {template['theme']}
Problema: El personaje está {conflict}
Solución: Aprende sobre {resolution}

Palabras nuevas para incluir (definir cada una naturalmente en el cuento): {', '.join(vocab_words)}

Requisitos:
- Oraciones simples y atractivas
- 500-800 palabras en total
- 12-16 páginas de contenido
- Incluir diálogo
- Final tierno y positivo
- Título que incluya el nombre del personaje

Formato:
TÍTULO: [Título del Cuento]

PÁGINA 1: [Texto]
PÁGINA 2: [Texto]
... etc

PALABRAS NUEVAS:
palabra1: definición
palabra2: definición
..."""
    
    return prompt, vocab_words

def generate_name(lang):
    """Generate a cute character name"""
    if lang == "en":
        names = ["Biscuit", "Coco", "Daisy", "Finn", "Hazel", "Jasper", "Luna", "Milo", 
                "Oliver", "Piper", "Rosie", "Sunny", "Teddy", "Willow", "Ziggy"]
    else:
        names = ["Cielo", "Estrella", "Luz", "Mar", "Nube", "Sol", "Viento", "Aurora",
                "Brisa", "Cascada", "Dulce", "Esperanza", "Flor", "Gloria", "Hope"]
    return random.choice(names)

def save_kimi_prompts(count=10, lang="en"):
    """Generate multiple Kimi prompts for batch story creation"""
    
    os.makedirs("prompts", exist_ok=True)
    
    age_groups = ["2-4", "5-7", "8-10"]
    
    prompts = []
    for i in range(count):
        template = random.choice(STORY_TEMPLATES)
        age = random.choice(age_groups)
        prompt, vocab = generate_story_prompt(template, age, lang)
        
        story_data = {
            "id": f"story_{i+1:03d}",
            "lang": lang,
            "age": age,
            "theme": template["theme"],
            "prompt": prompt,
            "expected_vocab": vocab
        }
        prompts.append(story_data)
    
    # Save prompts file
    filename = f"prompts/kimi_prompts_{lang}_{count}.json"
    with open(filename, 'w') as f:
        json.dump(prompts, f, indent=2)
    
    # Also save as text for easy copying
    txt_filename = f"prompts/kimi_prompts_{lang}_{count}.txt"
    with open(txt_filename, 'w') as f:
        for p in prompts:
            f.write(f"\n{'='*60}\n")
            f.write(f"STORY {p['id']} | {p['lang'].upper()} | Ages {p['age']} | Theme: {p['theme']}\n")
            f.write(f"{'='*60}\n\n")
            f.write(p['prompt'])
            f.write("\n\n")
    
    print(f"Generated {count} Kimi prompts:")
    print(f"  JSON: {filename}")
    print(f"  TXT:  {txt_filename}")
    
    return prompts

def parse_kimi_response(response_text, lang="en"):
    """Parse Kimi's story output into structured format"""
    
    lines = response_text.strip().split('\n')
    
    # Extract title
    title = "Untitled Story"
    if lang == "en":
        for line in lines:
            if line.startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
                break
    else:
        for line in lines:
            if line.startswith("TÍTULO:"):
                title = line.replace("TÍTULO:", "").strip()
                break
    
    # Extract pages
    pages = []
    current_page = None
    
    for line in lines:
        if lang == "en":
            if line.startswith("PAGE"):
                if current_page:
                    pages.append(current_page)
                page_num = re.search(r'PAGE\s*(\d+)', line)
                content = re.sub(r'PAGE\s*\d+[:\.]\s*', '', line).strip()
                current_page = {"page": int(page_num.group(1)) if page_num else 0, "content": content}
            elif current_page and line.strip():
                current_page["content"] += " " + line.strip()
        else:
            if line.startswith("PÁGINA"):
                if current_page:
                    pages.append(current_page)
                page_num = re.search(r'PÁGINA\s*(\d+)', line)
                content = re.sub(r'PÁGINA\s*\d+[:\.]\s*', '', line).strip()
                current_page = {"page": int(page_num.group(1)) if page_num else 0, "content": content}
            elif current_page and line.strip():
                current_page["content"] += " " + line.strip()
    
    if current_page:
        pages.append(current_page)
    
    # Extract vocabulary
    vocab = {}
    in_vocab_section = False
    
    for line in lines:
        if "NEW WORDS:" in line or "PALABRAS NUEVAS:" in line:
            in_vocab_section = True
            continue
        
        if in_vocab_section and ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                word = parts[0].strip()
                definition = parts[1].strip()
                vocab[word] = definition
    
    return {
        "title": title,
        "pages": pages,
        "vocabulary": vocab
    }

if __name__ == "__main__":
    import random
    import sys
    
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"Generating {count} Kimi prompts in {lang.upper()}...")
    save_kimi_prompts(count, lang)
    print("\n✅ Done! Copy prompts from prompts/kimi_prompts_*.txt")
    print("Paste into Kimi, then save responses to stories/ folder")
