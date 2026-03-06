#!/usr/bin/env python3
from pathlib import Path
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image

ROOT = Path(__file__).resolve().parent
IMG_DIR = ROOT / "illustrations" / "qwen_images"
OUT_DIR = ROOT / "real_books" / "output"
TMP_DIR = ROOT / "real_books" / "tmp_bw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(parents=True, exist_ok=True)


def fit_image(path, max_w, max_h):
    with Image.open(path) as im:
        w, h = im.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def gray_copy(src: Path) -> Path:
    dst = TMP_DIR / f"bw_{src.name}"
    with Image.open(src) as im:
        im.convert("L").save(dst)
    return dst


def draw_trace_line(c, x, y, text, copies=3):
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(HexColor("#111111"))
    c.drawString(x, y, text)
    c.setFont("Helvetica", 20)
    c.setFillColor(HexColor("#9A9A9A"))
    for i in range(copies):
        c.drawString(x + 170 * (i + 1), y, text)


def build_bw_book(title, subtitle, words_sentences, image_prefix):
    imgs = sorted(IMG_DIR.glob(f"{image_prefix}_page*.png"))
    if len(imgs) < len(words_sentences):
        raise RuntimeError(f"Need {len(words_sentences)} images for {image_prefix}, found {len(imgs)}")

    bw_imgs = [gray_copy(p) for p in imgs[:len(words_sentences)]]

    pdf = OUT_DIR / f"{title.replace(' ', '_')}_BW_Edition.pdf"
    W, H = 8.5 * inch, 11 * inch
    c = canvas.Canvas(str(pdf), pagesize=(W, H))

    c.setFillColor(HexColor("#444444"))
    c.rect(0, H - 2.7 * inch, W, 2.7 * inch, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 28)
    tw = c.stringWidth(title, "Helvetica-Bold", 28)
    c.drawString((W - tw) / 2, H - 1.6 * inch, title)
    c.setFont("Helvetica", 14)
    sw = c.stringWidth(subtitle, "Helvetica", 14)
    c.drawString((W - sw) / 2, H - 2.2 * inch, subtitle)
    c.setFillColor(HexColor("#222222"))
    c.drawString(0.8 * inch, H - 3.3 * inch, "Black & White Edition | Lower printing cost")
    c.showPage()

    for i, ws in enumerate(words_sentences):
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(HexColor("#222222"))
        c.drawString(0.6 * inch, H - 0.8 * inch, f"Word {i+1}: {ws['word']}")

        max_w, max_h = W - 1.2 * inch, 4.6 * inch
        iw, ih = fit_image(bw_imgs[i], max_w, max_h)
        c.drawImage(str(bw_imgs[i]), (W - iw) / 2, H - ih - 1.0 * inch, iw, ih, preserveAspectRatio=True, mask='auto')

        c.setStrokeColor(HexColor("#B5B5B5"))
        c.setLineWidth(1)
        for row in range(7):
            yline = 3.7 * inch - row * 0.45 * inch
            c.line(0.6 * inch, yline, W - 0.6 * inch, yline)

        draw_trace_line(c, 0.75 * inch, 3.45 * inch, ws["word"], copies=3)

        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(HexColor("#222222"))
        c.drawString(0.75 * inch, 2.35 * inch, "Trace the sentence:")
        c.setFont("Helvetica", 16)
        c.setFillColor(HexColor("#444444"))
        c.drawString(0.75 * inch, 1.95 * inch, ws["sentence"])
        c.setFillColor(HexColor("#999999"))
        c.drawString(0.75 * inch, 1.50 * inch, ws["sentence"])
        c.drawString(0.75 * inch, 1.10 * inch, ws["sentence"])
        c.showPage()

    c.save()
    print(f"✅ Created: {pdf}")


if __name__ == "__main__":
    farm = [
        {"word": "cow", "sentence": "The cow is on the farm."},
        {"word": "pig", "sentence": "The pig is pink."},
        {"word": "hen", "sentence": "The hen lays eggs."},
        {"word": "goat", "sentence": "The goat can jump."},
        {"word": "barn", "sentence": "The barn is big."},
        {"word": "hay", "sentence": "The hay is dry."},
    ]
    space = [
        {"word": "sun", "sentence": "The sun is bright."},
        {"word": "moon", "sentence": "The moon is round."},
        {"word": "star", "sentence": "A star can shine."},
        {"word": "rocket", "sentence": "The rocket can fly."},
        {"word": "planet", "sentence": "A planet can spin."},
        {"word": "alien", "sentence": "The alien is friendly."},
    ]

    build_bw_book(
        "Farm Writing Skills Workbook",
        "Trace Words and Sentences with Picture Prompts",
        farm,
        "farm_writing_skills_full",
    )
    build_bw_book(
        "Space Writing Skills Workbook",
        "Trace Words and Sentences with Picture Prompts",
        space,
        "space_writing_skills_full",
    )
