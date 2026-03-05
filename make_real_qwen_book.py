#!/usr/bin/env python3
import os
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

from qwen_simple import SimpleQwenGenerator

TITLE = "Penny the Pencil Learns to Write"
SUBTITLE = "A Beginner Handwriting Storybook"
OUT_DIR = "real_books/output"
IMG_DIR = "illustrations/qwen_images"
os.makedirs(OUT_DIR, exist_ok=True)

SCENES = [
    ("Penny the yellow pencil wakes up on a classroom desk next to a blank notebook", "Penny was a new pencil. She wanted to help kids write their first words."),
    ("Penny drawing straight lines on lined paper with a smiling child", "First, Penny practiced straight lines. Up, down, left, right."),
    ("Penny tracing curvy lines and loops on worksheet page", "Then Penny practiced curvy lines and loops. Slow and steady."),
    ("Penny tracing big uppercase letter A on worksheet", "Next came big letters. Penny traced a giant A."),
    ("Penny tracing lowercase letters a b c on notebook", "After that, Penny tried little letters: a, b, and c."),
    ("Penny writing numbers 1 2 3 with stars and smiley stickers", "Finally, Penny wrote numbers 1, 2, and 3. The page looked great!"),
    ("Penny and child celebrating with certificate and confetti in classroom", "Practice made Penny confident. The child smiled: We can write now!")
]


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def main():
    g = SimpleQwenGenerator()
    g.request_delay_sec = int(os.getenv("QWEN_REQUEST_DELAY_SEC", "18"))
    g.max_retries = int(os.getenv("QWEN_MAX_RETRIES", "5"))
    g.backoff_base_sec = int(os.getenv("QWEN_BACKOFF_BASE_SEC", "15"))

    image_files = []
    for i, (prompt, _) in enumerate(SCENES, 1):
        f = g.generate_image(prompt, f"penny_book_page{i:02d}")
        if not f:
            raise RuntimeError(f"Failed generating scene {i}")
        image_files.append(f)

    pdf_path = f"{OUT_DIR}/Penny_the_Pencil_Learns_to_Write.pdf"
    W, H = 8.5 * inch, 8.5 * inch
    c = canvas.Canvas(pdf_path, pagesize=(W, H))

    # Cover
    c.setFillColor(HexColor("#4A90E2"))
    c.rect(0, H - 2.4 * inch, W, 2.4 * inch, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 28)
    tw = c.stringWidth(TITLE, "Helvetica-Bold", 28)
    c.drawString((W - tw) / 2, H - 1.4 * inch, TITLE)
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica", 14)
    sw = c.stringWidth(SUBTITLE, "Helvetica", 14)
    c.drawString((W - sw) / 2, H - 2.8 * inch, SUBTITLE)
    c.showPage()

    # Story spreads (image + text)
    for i, img in enumerate(image_files):
        max_w, max_h = W - 1.0 * inch, H - 2.7 * inch
        iw, ih = fit_image(img, max_w, max_h)
        c.drawImage(img, (W - iw) / 2, H - ih - 0.8 * inch, iw, ih, preserveAspectRatio=True, mask='auto')

        c.setFillColor(HexColor("#111111"))
        c.setFont("Helvetica", 13)
        text = SCENES[i][1]
        c.roundRect(0.6 * inch, 0.5 * inch, W - 1.2 * inch, 1.4 * inch, 8, fill=0, stroke=1)
        c.drawString(0.85 * inch, 1.2 * inch, text)
        c.showPage()

    # Back page
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor("#4A90E2"))
    c.drawString(0.8 * inch, H - 1.4 * inch, "The End")
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#333333"))
    c.drawString(0.8 * inch, H - 1.9 * inch, "Keep practicing. You are becoming a great writer!")
    c.save()
    print(f"✅ Created real illustrated book: {pdf_path}")


if __name__ == "__main__":
    main()
