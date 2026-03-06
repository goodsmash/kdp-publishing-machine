#!/usr/bin/env python3
"""
KDP Program Manager
Unified control plane for the KDP publishing workflow.

Features:
- Portfolio status report (what exists now)
- Planned pipeline queue (CSV)
- New book package scaffolding for production
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
PROGRAM_DIR = ROOT / "program"
BOOKS_DIR = PROGRAM_DIR / "books"
QUEUE_CSV = PROGRAM_DIR / "pipeline_queue.csv"
STATUS_JSON = PROGRAM_DIR / "portfolio_status.json"
LEDGER_PATH = PROGRAM_DIR / "api_ledger.jsonl"


@dataclass
class BookPlan:
    slug: str
    title: str
    language: str
    age_range: str
    trim_size: str
    category: str
    status: str = "planned"  # planned|drafting|interior_ready|cover_ready|uploaded|live
    created_at: str = ""


def ensure_dirs() -> None:
    PROGRAM_DIR.mkdir(parents=True, exist_ok=True)
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)


def get_generated_books() -> List[dict]:
    books = []
    if not OUTPUT_DIR.exists():
        return books

    for pdf in sorted(OUTPUT_DIR.glob("*.pdf")):
        metadata_path = OUTPUT_DIR / f"{pdf.stem.rsplit('_', 1)[0]}_metadata.json"
        metadata = {}
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text())
            except Exception:
                metadata = {"_error": "invalid metadata json"}

        books.append(
            {
                "pdf": str(pdf.relative_to(ROOT)),
                "pdf_size_bytes": pdf.stat().st_size,
                "metadata_file": str(metadata_path.relative_to(ROOT)) if metadata_path.exists() else None,
                "title": metadata.get("title"),
                "language": metadata.get("language"),
                "age_range": metadata.get("age_range"),
                "trim_size": metadata.get("trim_size"),
                "ready": True,
            }
        )

    return books


def write_status_report() -> dict:
    ensure_dirs()
    generated = get_generated_books()

    queue_items = []
    if QUEUE_CSV.exists():
        with QUEUE_CSV.open(newline="", encoding="utf-8") as f:
            queue_items = list(csv.DictReader(f))

    status = {
        "generated_count": len(generated),
        "generated_books": generated,
        "pipeline_count": len(queue_items),
        "pipeline": queue_items,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }

    STATUS_JSON.write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def init_queue() -> None:
    ensure_dirs()
    if QUEUE_CSV.exists():
        return

    defaults = [
        BookPlan("letter-tracing-farm", "Letter Tracing Farm Friends", "en", "3-5", "8.5x8.5", "activity"),
        BookPlan("number-tracing-space", "Number Tracing Space Adventure", "en", "3-5", "8.5x8.5", "activity"),
        BookPlan("my-first-scissor-skills", "My First Scissor Skills Workbook", "en", "4-6", "8.5x11", "activity"),
        BookPlan("cuentos-animales-valientes", "Cuentos de Animales Valientes", "es", "4-7", "8x10", "story"),
        BookPlan("kindness-coloring-book", "Kindness Coloring Book for Kids", "en", "4-8", "8.5x11", "coloring"),
    ]

    with QUEUE_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(asdict(defaults[0]).keys()),
        )
        writer.writeheader()
        for item in defaults:
            item.created_at = datetime.now().isoformat(timespec="seconds")
            writer.writerow(asdict(item))


def add_queue_item(item: BookPlan) -> None:
    ensure_dirs()
    exists = QUEUE_CSV.exists()
    with QUEUE_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(item).keys()))
        if not exists:
            writer.writeheader()
        if not item.created_at:
            item.created_at = datetime.now().isoformat(timespec="seconds")
        writer.writerow(asdict(item))


def scaffold_book(slug: str) -> Path:
    ensure_dirs()
    d = BOOKS_DIR / slug
    d.mkdir(parents=True, exist_ok=True)

    for sub in ["interior", "cover", "metadata", "assets", "notes"]:
        (d / sub).mkdir(exist_ok=True)

    brief = d / "notes" / "BRIEF.md"
    if not brief.exists():
        brief.write_text(
            "# Book Brief\n\n"
            "- Title:\n"
            "- Audience:\n"
            "- Promise (what child learns/gets):\n"
            "- Interior style:\n"
            "- Cover angle:\n"
            "- KDP keywords:\n"
            "- BISAC categories:\n"
            "- Completion checklist:\n"
            "  - [ ] Interior PDF\n"
            "  - [ ] Cover PDF\n"
            "  - [ ] Metadata JSON\n"
            "  - [ ] Upload package\n",
            encoding="utf-8",
        )

    return d


def cmd_status(_: argparse.Namespace) -> None:
    status = write_status_report()
    print(f"Generated books: {status['generated_count']}")
    print(f"Pipeline queue: {status['pipeline_count']}")
    print(f"Status file: {STATUS_JSON}")


def cmd_init(_: argparse.Namespace) -> None:
    init_queue()
    status = write_status_report()
    print(f"✅ Queue initialized. Pipeline items: {status['pipeline_count']}")


def cmd_add(args: argparse.Namespace) -> None:
    item = BookPlan(
        slug=args.slug,
        title=args.title,
        language=args.language,
        age_range=args.age,
        trim_size=args.trim,
        category=args.category,
    )
    add_queue_item(item)
    print(f"✅ Added: {args.slug}")


def cmd_scaffold(args: argparse.Namespace) -> None:
    d = scaffold_book(args.slug)
    print(f"✅ Scaffolded: {d}")


def _read_ledger_today() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    today = datetime.now().strftime("%Y-%m-%d")
    rows = []
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            ts = str(obj.get("ts", ""))
            if ts.startswith(today):
                rows.append(obj)
    return rows


def _count_new_files_today() -> dict:
    today = datetime.now().date()
    roots = [
        ROOT / "output",
        ROOT / "workbooks" / "output",
        ROOT / "activity_books" / "output",
        ROOT / "interactive_books" / "output",
        ROOT / "interactive_books" / "premium",
        ROOT / "real_books" / "output",
    ]
    files = []
    for r in roots:
        if not r.exists():
            continue
        for p in r.glob("*.pdf"):
            m = datetime.fromtimestamp(p.stat().st_mtime).date()
            if m == today:
                files.append(str(p.relative_to(ROOT)))
    return {"count": len(files), "files": sorted(files)}


def cmd_dashboard(_: argparse.Namespace) -> None:
    ensure_dirs()
    today_events = _read_ledger_today()
    events_by_type = {}
    success = 0
    failures = 0

    for e in today_events:
        k = e.get("event", "unknown")
        events_by_type[k] = events_by_type.get(k, 0) + 1
        if k == "success":
            success += 1
        if k in {"api_error", "exception_fail", "failed_all_models", "unexpected_response"}:
            failures += 1

    images_generated = success
    files_today = _count_new_files_today()

    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "api_calls_today": len(today_events),
        "api_success_today": success,
        "api_failures_today": failures,
        "images_generated_today": images_generated,
        "events_by_type": events_by_type,
        "new_kdp_files_today": files_today,
    }

    out = PROGRAM_DIR / "dashboard_today.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Date: {report['date']}")
    print(f"API calls today: {report['api_calls_today']}")
    print(f"API success today: {report['api_success_today']}")
    print(f"API failures today: {report['api_failures_today']}")
    print(f"Images generated today: {report['images_generated_today']}")
    print(f"New KDP files today: {files_today['count']}")
    print(f"Dashboard file: {out}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="KDP Program Manager")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Write/read portfolio status")
    s.set_defaults(func=cmd_status)

    i = sub.add_parser("init", help="Initialize default production queue")
    i.set_defaults(func=cmd_init)

    a = sub.add_parser("add", help="Add book to pipeline queue")
    a.add_argument("slug")
    a.add_argument("title")
    a.add_argument("--language", default="en")
    a.add_argument("--age", default="4-7")
    a.add_argument("--trim", default="8x10")
    a.add_argument("--category", default="story")
    a.set_defaults(func=cmd_add)

    b = sub.add_parser("scaffold", help="Create book production folder scaffold")
    b.add_argument("slug")
    b.set_defaults(func=cmd_scaffold)

    d = sub.add_parser("dashboard", help="Summarize today's API + production activity")
    d.set_defaults(func=cmd_dashboard)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
