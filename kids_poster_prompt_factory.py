#!/usr/bin/env python3
import json, os, random

OUT_DIR = "illustrations/prompt_factory"
os.makedirs(OUT_DIR, exist_ok=True)

BASE_STYLE = (
    "Healing-style hand-drawn children's poster, soft painterly lines, cheerful composition, "
    "clear focal subject, decorative birds and stars, vibrant but balanced palette, "
    "fresh greens and blues with pink and yellow accents, print-friendly, kid-safe, high clarity"
)

SCENES = {
    "en": [
        "three puppies playing with a ball on lush green grass",
        "two kittens flying kites in a sunny park",
        "a bunny and duckling sharing snacks on a picnic blanket",
        "three dinosaur friends dancing under rainbow clouds",
        "little astronauts playing catch on a moon playground",
        "ocean friends building a sandcastle by the shore",
        "forest animals painting together in a meadow",
        "baby dragons learning teamwork in a bright valley",
        "school friends jumping rope at recess",
        "three puppies practicing soccer in a happy field"
    ],
    "es": [
        "tres perritos jugando con una pelota sobre césped verde",
        "dos gatitos volando cometas en un parque soleado",
        "un conejito y un patito compartiendo merienda en picnic",
        "tres dinosaurios amigos bailando bajo nubes arcoíris",
        "pequeños astronautas jugando a lanzar la pelota en la luna",
        "amigos del océano construyendo un castillo de arena",
        "animales del bosque pintando juntos en un prado",
        "bebés dragón aprendiendo trabajo en equipo en un valle brillante",
        "amigos de escuela jugando a la cuerda en recreo",
        "tres perritos practicando fútbol en un campo alegre"
    ]
}

TITLES = {
    "en": [
        "Come Play Ball!",
        "Let’s Learn Together!",
        "Teamwork Time!",
        "Play, Learn, Smile!",
        "Big Fun Day!"
    ],
    "es": [
        "¡Ven a Jugar!",
        "¡Aprendamos Juntos!",
        "¡Hora de Equipo!",
        "¡Jugar, Aprender y Sonreír!",
        "¡Gran Día de Diversión!"
    ]
}

SUBTITLES = {
    "en": [
        "Show Off Your Skills!",
        "Practice Makes Progress!",
        "Friends Make Learning Fun!",
        "Try, Learn, and Grow!"
    ],
    "es": [
        "¡Muestra Tus Habilidades!",
        "¡Practicar Te Hace Mejor!",
        "¡Con Amigos se Aprende Mejor!",
        "¡Intenta, Aprende y Crece!"
    ]
}

BUBBLES = {
    "en": [
        "Hehe, watch me amaze my little friends next!",
        "I can do it—let's play together!",
        "Wow! We’re getting better every day!"
    ],
    "es": [
        "¡Jeje, ahora verán lo que puedo hacer!",
        "¡Yo puedo, juguemos juntos!",
        "¡Guau! ¡Cada día lo hacemos mejor!"
    ]
}

FOOTERS = {
    "en": [
        "We get to play ball with our friends again!",
        "Learning is more fun when we play together!",
        "Small steps, big smiles!"
    ],
    "es": [
        "¡Podemos jugar con nuestros amigos otra vez!",
        "¡Aprender es más divertido cuando jugamos juntos!",
        "¡Pasos pequeños, sonrisas grandes!"
    ]
}

NEGATIVE = "low resolution, blurry text, distorted letters, deformed anatomy, scary mood, dark palette, watermark, logo artifacts"


def make_prompt(lang, scene):
    title = random.choice(TITLES[lang])
    subtitle = random.choice(SUBTITLES[lang])
    bubble = random.choice(BUBBLES[lang])
    footer = random.choice(FOOTERS[lang])

    return {
        "lang": lang,
        "scene": scene,
        "title_text": title,
        "subtitle_text": subtitle,
        "bubble_text": bubble,
        "footer_text": footer,
        "prompt": (
            f"{BASE_STYLE}. Scene: {scene}. "
            f"Top headline text in bold blue cartoon font: '{title}'. "
            f"Subtitle in green playful font: '{subtitle}'. "
            f"Add one speech bubble saying: '{bubble}'. "
            f"Bottom supplementary text: '{footer}'. "
            "Ensure text is legible, centered layout, balanced whitespace."
        ),
        "negative_prompt": NEGATIVE
    }


def generate_batch(n_en=30, n_es=30):
    out = {"en": [], "es": []}

    for _ in range(n_en):
        out["en"].append(make_prompt("en", random.choice(SCENES["en"])))
    for _ in range(n_es):
        out["es"].append(make_prompt("es", random.choice(SCENES["es"])))

    json_path = f"{OUT_DIR}/kids_poster_prompts_en{n_en}_es{n_es}.json"
    txt_path = f"{OUT_DIR}/kids_poster_prompts_en{n_en}_es{n_es}.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("KIDS POSTER PROMPT FACTORY (EN/ES)\n\n")
        for lang in ["en", "es"]:
            f.write(f"=== {lang.upper()} ===\n")
            for i, p in enumerate(out[lang], 1):
                f.write(f"\n[{lang.upper()}-{i:03d}]\n")
                f.write(f"PROMPT: {p['prompt']}\n")
                f.write(f"NEGATIVE: {p['negative_prompt']}\n")

    print(f"✅ Generated: {json_path}")
    print(f"✅ Generated: {txt_path}")


if __name__ == "__main__":
    generate_batch(40, 40)
