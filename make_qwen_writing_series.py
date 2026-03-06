#!/usr/bin/env python3
import os
from pathlib import Path

# Load .env before importing qwen_simple
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key, value)

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

from qwen_simple import SimpleQwenGenerator

OUT_DIR = Path("real_books/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def draw_trace_line(c, x, y, text, copies=3):
    # model text
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(HexColor("#222222"))
    c.drawString(x, y, text)

    # tracing lines (light gray repeated text)
    c.setFont("Helvetica", 20)
    c.setFillColor(HexColor("#B8B8B8"))
    for i in range(copies):
        c.drawString(x + 170 * (i + 1), y, text)


def build_writing_book(book_slug, title, subtitle, scene_specs):
    g = SimpleQwenGenerator()
    g.request_delay_sec = int(os.getenv("QWEN_REQUEST_DELAY_SEC", "18"))
    g.max_retries = int(os.getenv("QWEN_MAX_RETRIES", "5"))
    g.backoff_base_sec = int(os.getenv("QWEN_BACKOFF_BASE_SEC", "12"))

    images = []
    for i, s in enumerate(scene_specs, 1):
        filename = g.generate_image(s["prompt"], f"{book_slug}_page{i:02d}", size="1536*1536")
        if not filename:
            raise RuntimeError(f"Failed generating image for page {i}: {s['word']}")
        images.append(filename)

    pdf_path = OUT_DIR / f"{title.replace(' ', '_')}.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H))

    # Cover
    c.setFillColor(HexColor("#3A86FF"))
    c.rect(0, H - 3.0 * inch, W, 3.0 * inch, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 30)
    tw = c.stringWidth(title, "Helvetica-Bold", 30)
    c.drawString((W - tw) / 2, H - 1.6 * inch, title)
    c.setFillColor(HexColor("#222222"))
    c.setFont("Helvetica", 15)
    sw = c.stringWidth(subtitle, "Helvetica", 15)
    c.drawString((W - sw) / 2, H - 3.4 * inch, subtitle)
    c.setFont("Helvetica", 12)
    c.drawString(0.9 * inch, H - 4.0 * inch, "Ages 3-6 | Handwriting Skills | Trace Words + Sentences")
    c.showPage()

    # Intro
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(HexColor("#222222"))
    c.drawString(0.8 * inch, H - 1.2 * inch, "How to Use This Workbook")
    c.setFont("Helvetica", 14)
    lines = [
        "1) Trace the big word first.",
        "2) Trace the faded copies.",
        "3) Trace the sentence.",
        "4) Say the sounds out loud while writing.",
    ]
    y = H - 1.9 * inch
    for line in lines:
        c.drawString(1.0 * inch, y, line)
        y -= 0.45 * inch
    c.showPage()

    # Skill pages
    for i, spec in enumerate(scene_specs):
        img = images[i]

        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(HexColor("#3A86FF"))
        c.drawString(0.6 * inch, H - 0.8 * inch, f"Word {i+1}: {spec['word']}")

        max_w, max_h = W - 1.2 * inch, 4.6 * inch
        iw, ih = fit_image(img, max_w, max_h)
        c.drawImage(img, (W - iw) / 2, H - ih - 1.0 * inch, iw, ih, preserveAspectRatio=True, mask='auto')

        c.setStrokeColor(HexColor("#BBBBBB"))
        c.setLineWidth(1)
        for row in range(7):
            yline = 3.7 * inch - row * 0.45 * inch
            c.line(0.6 * inch, yline, W - 0.6 * inch, yline)

        draw_trace_line(c, 0.75 * inch, 3.45 * inch, spec["word"], copies=3)

        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(HexColor("#222222"))
        c.drawString(0.75 * inch, 2.35 * inch, "Trace the sentence:")
        c.setFont("Helvetica", 16)
        c.setFillColor(HexColor("#444444"))
        c.drawString(0.75 * inch, 1.95 * inch, spec["sentence"])
        c.setFillColor(HexColor("#B8B8B8"))
        c.drawString(0.75 * inch, 1.50 * inch, spec["sentence"])
        c.drawString(0.75 * inch, 1.10 * inch, spec["sentence"])

        c.showPage()

    # Completion page
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(HexColor("#3A86FF"))
    c.drawString(1.5 * inch, H - 2.2 * inch, "Great Writing Work!")
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#222222"))
    c.drawString(1.1 * inch, H - 2.8 * inch, "You finished this handwriting skills workbook.")
    c.drawString(1.1 * inch, H - 3.2 * inch, "Keep practicing every day to write faster and neater.")
    c.save()

    return str(pdf_path)


def main():
    farm_specs = [
        {"word": "cow", "sentence": "The cow is on the farm.", "prompt": "cute farm cow standing in a green field, children's workbook style"},
        {"word": "pig", "sentence": "The pig is pink.", "prompt": "friendly pink pig near a red barn, bright daytime, children's workbook style"},
        {"word": "hen", "sentence": "The hen lays eggs.", "prompt": "cute hen beside straw nest with eggs, simple background, children's workbook style"},
        {"word": "goat", "sentence": "The goat can jump.", "prompt": "playful goat hopping near wooden fence, children's workbook style"},
        {"word": "barn", "sentence": "The barn is big.", "prompt": "bright red barn on farm with clear sky, children's workbook style"},
        {"word": "hay", "sentence": "The hay is dry.", "prompt": "stacked hay bales in sunny farmyard, children's workbook style"},
    ]

    space_specs = [
        {"word": "sun", "sentence": "The sun is bright.", "prompt": "friendly smiling sun in space with stars, children's workbook style"},
        {"word": "moon", "sentence": "The moon is round.", "prompt": "cute full moon with stars and soft glow, children's workbook style"},
        {"word": "star", "sentence": "A star can shine.", "prompt": "golden star sparkling in dark blue sky, children's workbook style"},
        {"word": "rocket", "sentence": "The rocket can fly.", "prompt": "colorful rocket launching through space, children's workbook style"},
        {"word": "planet", "sentence": "A planet can spin.", "prompt": "cartoon planet with rings floating in space, children's workbook style"},
        {"word": "alien", "sentence": "The alien is friendly.", "prompt": "cute friendly green alien waving on small planet, children's workbook style"},
    ]

    p1 = build_writing_book(
        "farm_writing_skills_full",
        "Farm Writing Skills Workbook",
        "Trace Words and Sentences with Picture Prompts",
        farm_specs,
    )
    print(f"✅ Created: {p1}")

    p2 = build_writing_book(
        "space_writing_skills_full",
        "Space Writing Skills Workbook",
        "Trace Words and Sentences with Picture Prompts",
        space_specs,
    )
    print(f"✅ Created: {p2}")


if __name__ == "__main__":
    main()
