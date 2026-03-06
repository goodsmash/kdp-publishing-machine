#!/usr/bin/env python3
"""
Simple Qwen Image Generator using HTTP API
Direct API calls to Alibaba Cloud for image generation
"""

import requests
import json
import base64
import os
import time
import hashlib
from datetime import datetime
from pathlib import Path
from credit_guard import CreditGuard

# API Configuration
API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
API_URL = os.getenv("DASHSCOPE_API_URL", "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation")
MODEL = os.getenv("QWEN_IMAGE_MODEL", "qwen-image-2.0-pro-2026-03-03")

class SimpleQwenGenerator:
    """Simple HTTP-based Qwen image generator"""
    
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.model = MODEL
        self.model_fallbacks = [
            os.getenv("QWEN_IMAGE_MODEL", "qwen-image-2.0-pro-2026-03-03"),
            os.getenv("QWEN_IMAGE_FALLBACK_1", "qwen-image-2.0-pro"),
            os.getenv("QWEN_IMAGE_FALLBACK_2", "qwen-image-2.0")
        ]
        self.output_dir = "illustrations/qwen_images"
        os.makedirs(self.output_dir, exist_ok=True)

        # Persistent API ledger for auditing/analytics
        self.ledger_path = Path(os.getenv("QWEN_API_LEDGER", "program/api_ledger.jsonl"))
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

        # Rate control (safe defaults)
        self.request_delay_sec = int(os.getenv("QWEN_REQUEST_DELAY_SEC", "20"))
        self.max_retries = int(os.getenv("QWEN_MAX_RETRIES", "4"))
        self.backoff_base_sec = int(os.getenv("QWEN_BACKOFF_BASE_SEC", "12"))
        
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.credit_guard = CreditGuard()

    def _log_ledger(self, event: dict):
        """Append one JSON line to API ledger."""
        base = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "provider": "alibaba_dashscope",
        }
        base.update(event)
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(base, ensure_ascii=False) + "\n")
    
    def generate_image(self, prompt, output_name, size=None):
        """Generate image using HTTP API"""

        if size is None:
            size = os.getenv("QWEN_IMAGE_SIZE", "1536*1536")

        style_anchor = os.getenv("QWEN_STYLE_ANCHOR", "consistent children's picture book style, soft painterly digital illustration, clean composition, expressive faces")

        # Enhance prompt for higher-quality children's books
        enhanced_prompt = (
            f"{style_anchor}, {prompt}, "
            f"high detail, cohesive character design, storybook lighting, rich but balanced color palette, "
            f"print-friendly composition, no text"
        )
        prompt_hash = hashlib.sha256(enhanced_prompt.encode("utf-8")).hexdigest()[:16]
        
        if not self.credit_guard.can_spend(1):
            s = self.credit_guard.summary()
            print(f"⛔ Credit guard stop: used {s['used']}/{s['cap']} images today (50% cap).")
            self._log_ledger({
                "event": "blocked_credit_guard",
                "output_name": output_name,
                "prompt_hash": prompt_hash,
                "credit_used": s["used"],
                "credit_cap": s["cap"],
            })
            return None

        print(f"🎨 Generating: {output_name}")
        print(f"   Prompt: {enhanced_prompt[:70]}...")

        for model_name in self.model_fallbacks:
            payload = {
                "model": model_name,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"text": enhanced_prompt}
                            ]
                        }
                    ]
                },
                "parameters": {
                    "negative_prompt": "low resolution, low quality, deformed anatomy, muddy colors, chaotic composition, blurry text, distorted text, watermark, extra limbs, duplicate face",
                    "prompt_extend": True,
                    "watermark": False,
                    "size": size,
                    "n": 1,
                    "seed": 123456
                }
            }
            print(f"   Model: {model_name}")
            for attempt in range(1, self.max_retries + 1):
                try:
                    self._log_ledger({
                        "event": "request",
                        "output_name": output_name,
                        "prompt_hash": prompt_hash,
                        "model": model_name,
                        "attempt": attempt,
                        "size": size,
                    })
                    response = requests.post(API_URL, headers=self.headers, json=payload, timeout=120)

                    if response.status_code == 200:
                        data = response.json()

                        # Check for image URL in response (new format)
                        if "output" in data and "choices" in data["output"]:
                            for choice in data["output"]["choices"]:
                                content = choice.get("message", {}).get("content", [])
                                for item in content:
                                    image_url = item.get("image")
                                    if image_url:
                                        img_response = requests.get(image_url, timeout=60)
                                        if img_response.status_code == 200:
                                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                            filename = f"{self.output_dir}/{output_name}_{timestamp}.png"
                                            with open(filename, "wb") as f:
                                                f.write(img_response.content)
                                            print(f"   ✅ Saved: {filename}")
                                            self.credit_guard.spend(1)
                                            s = self.credit_guard.summary()
                                            self._log_ledger({
                                                "event": "success",
                                                "output_name": output_name,
                                                "prompt_hash": prompt_hash,
                                                "model": model_name,
                                                "attempt": attempt,
                                                "status_code": response.status_code,
                                                "file": filename,
                                                "credit_used": s["used"],
                                                "credit_cap": s["cap"],
                                            })
                                            print(f"   Credit usage: {s['used']}/{s['cap']} (remaining {s['remaining']})")
                                            time.sleep(self.request_delay_sec)
                                            return filename

                        print(f"   ⚠️  Response format: {json.dumps(data, indent=2)[:200]}")
                        self._log_ledger({
                            "event": "unexpected_response",
                            "output_name": output_name,
                            "prompt_hash": prompt_hash,
                            "model": model_name,
                            "attempt": attempt,
                            "status_code": response.status_code,
                        })
                        time.sleep(self.request_delay_sec)
                        break

                    # Throttle handling
                    if response.status_code == 429:
                        wait = self.backoff_base_sec * attempt
                        print(f"   ⏳ Rate-limited (429). Retry {attempt}/{self.max_retries} in {wait}s...")
                        self._log_ledger({
                            "event": "rate_limited",
                            "output_name": output_name,
                            "prompt_hash": prompt_hash,
                            "model": model_name,
                            "attempt": attempt,
                            "status_code": 429,
                            "wait_sec": wait,
                        })
                        time.sleep(wait)
                        continue

                    print(f"   ❌ API Error: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    self._log_ledger({
                        "event": "api_error",
                        "output_name": output_name,
                        "prompt_hash": prompt_hash,
                        "model": model_name,
                        "attempt": attempt,
                        "status_code": response.status_code,
                        "error": response.text[:300],
                    })
                    time.sleep(self.request_delay_sec)
                    break

                except Exception as e:
                    if attempt < self.max_retries:
                        wait = self.backoff_base_sec * attempt
                        print(f"   ⚠️  Error: {e}. Retry {attempt}/{self.max_retries} in {wait}s...")
                        self._log_ledger({
                            "event": "exception_retry",
                            "output_name": output_name,
                            "prompt_hash": prompt_hash,
                            "model": model_name,
                            "attempt": attempt,
                            "wait_sec": wait,
                            "error": str(e)[:300],
                        })
                        time.sleep(wait)
                        continue
                    print(f"   ❌ Error: {e}")
                    self._log_ledger({
                        "event": "exception_fail",
                        "output_name": output_name,
                        "prompt_hash": prompt_hash,
                        "model": model_name,
                        "attempt": attempt,
                        "error": str(e)[:300],
                    })
                    break

        self._log_ledger({
            "event": "failed_all_models",
            "output_name": output_name,
            "prompt_hash": prompt_hash,
            "models_tried": self.model_fallbacks,
        })
        return None
    
    def test_generation(self):
        """Test with a simple prompt"""
        print("="*60)
        print("TESTING QWEN IMAGE GENERATION")
        print("="*60)
        
        test_prompts = [
            ("cute teddy bear sitting in a meadow with flowers", "test_bear"),
            ("little gray owl on a tree branch at night", "test_owl"),
            ("small brown seed sprouting into a green plant", "test_seed"),
        ]
        
        for prompt, name in test_prompts:
            result = self.generate_image(prompt, name)
            if result:
                print(f"✅ Success: {result}\n")
            else:
                print(f"❌ Failed\n")
    
    def generate_for_book(self, book_title, scenes):
        """Generate illustrations for a book"""
        print(f"\n{'='*60}")
        print(f"GENERATING: {book_title}")
        print(f"{'='*60}\n")
        
        generated = []
        for i, scene in enumerate(scenes, 1):
            result = self.generate_image(scene, f"{book_title.replace(' ', '_')}_page{i:02d}")
            if result:
                generated.append({
                    "page": i,
                    "scene": scene,
                    "file": result
                })
        
        # Save manifest
        manifest = {
            "book": book_title,
            "generated": datetime.now().isoformat(),
            "images": generated
        }
        
        manifest_file = f"{self.output_dir}/{book_title.replace(' ', '_')}_manifest.json"
        with open(manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n✅ Generated {len(generated)}/{len(scenes)} images")
        print(f"   Manifest: {manifest_file}")
        
        return generated


# Book scenes for generation
BOOK_SCENES = {
    "The Brave Little Seed": [
        "tiny brown seed sitting on a colorful flower petal, sun shining, garden background",
        "wind blowing through a garden, flowers bending, leaves swirling",
        "seed tumbling through the blue sky, spinning, fluffy white clouds",
        "seed resting in rich brown soil underground, cross section view",
        "rain falling on garden soil with sun peeking through clouds",
        "tiny green sprout pushing through soil, first leaves unfurling",
        "small plant growing taller with green leaves in sunny garden",
        "beautiful blooming flower with pink petals open wide in garden"
    ],
    "Luna and the Moon": [
        "cute gray owl sitting on oak tree branch, night sky beginning",
        "full moon rising over forest silhouette, silver glow, twilight",
        "owl with wind blowing through feathers, tree branches",
        "night sky filled with twinkling stars and crescent moon",
        "owl sleeping peacefully in cozy tree hollow, soft moonlight"
    ],
    "Benny Bear's First Honey": [
        "small brown bear cub in cozy cave, forest view",
        "bear sniffing air with curious expression in forest",
        "tall tree with beehive, golden honey dripping, forest",
        "bear climbing tree with determination",
        "happy bear with honey on nose, proud expression"
    ]
}

if __name__ == "__main__":
    import sys
    
    generator = SimpleQwenGenerator()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            generator.test_generation()
        elif sys.argv[1] == "book" and len(sys.argv) > 2:
            book_name = sys.argv[2]
            if book_name in BOOK_SCENES:
                generator.generate_for_book(book_name, BOOK_SCENES[book_name])
            else:
                print(f"Unknown book: {book_name}")
                print(f"Available: {list(BOOK_SCENES.keys())}")
        elif sys.argv[1] == "all":
            for book, scenes in BOOK_SCENES.items():
                generator.generate_for_book(book, scenes)
    else:
        print("Qwen Image Generator")
        print("\nUsage:")
        print("  python3 qwen_simple.py test        - Test with sample prompts")
        print("  python3 qwen_simple.py book NAME   - Generate for specific book")
        print("  python3 qwen_simple.py all         - Generate for all books")
        print(f"\nAvailable books: {', '.join(BOOK_SCENES.keys())}")
