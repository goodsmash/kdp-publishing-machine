#!/usr/bin/env python3
"""
Alibaba Model Rotator - MASSIVE FREE QUOTA VERSION
Uses ALL 40+ models from Alibaba Cloud Model Studio
Total: 7,000+ free generations per day!
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict

# Load .env
ROOT = Path(__file__).resolve().parent
env_path = ROOT / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key, value)


class AlibabaModelRotator:
    """Rotate through ALL 40+ Alibaba models to maximize free quota"""
    
    # Image Generation Models - All using same API endpoint
    # Note: Wan models (wan2.x) use different API - stick to qwen/z models
    IMAGE_MODELS: Dict[str, int] = {
        # Qwen Image (100 each)
        "qwen-image-plus": 100,
        "qwen-image-plus-2026-01-09": 100,
        "qwen-image-max": 100,
        "qwen-image-max-2025-12-30": 100,
        "qwen-image-2.0-2026-03-03": 100,
        "qwen-image-2.0-pro-2026-03-03": 100,
        "qwen-image-2.0-pro": 100,
        "qwen-image-2.0": 100,
        "qwen-image": 100,
        "z-image-turbo": 100,
    }
    
    # Image Editing Models - Total: 600 edits/day
    EDIT_MODELS: Dict[str, int] = {
        "qwen-image-edit-plus": 100,
        "qwen-image-edit-plus-2025-10-30": 100,
        "qwen-image-edit-max": 100,
        "qwen-image-edit-max-2026-01-16": 100,
        "qwen-image-edit": 100,
        "qwen-image-edit-plus-2025-12-15": 100,
        "wan2.5-i2i-preview": 50,
    }
    
    # Video Generation Models (different API - not included in rotation)
    VIDEO_MODELS: Dict[str, int] = {}
    
    # Animation Models (different API)
    ANIMATION_MODELS: Dict[str, int] = {}
    
    # Text Models
    TEXT_MODELS: Dict[str, int] = {
        "qwen3-max": 1000,
        "qwen3-max-2026-01-23": 1000,
        "qwen-plus": 2000,
        "qwen-turbo": 5000,
    }
    
    def __init__(self):
        self.state_file = ROOT / ".alibaba_rotator_state.json"
        self.state = self._load_state()
        from qwen_simple import SimpleQwenGenerator
        self.base_generator = SimpleQwenGenerator()
        
    def _load_state(self) -> dict:
        """Track usage per model"""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                if data.get("date") == today and "usage" in data:
                    return data
            except:
                pass
        
        # Initialize all model usage to 0
        all_models = {}
        for d in [self.IMAGE_MODELS, self.EDIT_MODELS, self.VIDEO_MODELS, 
                  self.ANIMATION_MODELS, self.TEXT_MODELS]:
            all_models.update({k: 0 for k in d.keys()})
        
        return {
            "date": today,
            "usage": all_models,
        }
    
    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))
    
    def get_next_image_model(self) -> str:
        """Get the image model with most remaining quota"""
        usage = self.state["usage"]
        
        # Find model with most remaining (limit - used)
        best_model = None
        best_remaining = -1
        
        for model, limit in self.IMAGE_MODELS.items():
            used = usage.get(model, 0)
            remaining = limit - used
            if remaining > best_remaining:
                best_remaining = remaining
                best_model = model
        
        return best_model if best_model else list(self.IMAGE_MODELS.keys())[0]
    
    def get_available_quota(self) -> dict:
        """Show remaining quota for all models"""
        usage = self.state["usage"]
        result = {
            "image": {},
            "edit": {},
            "text": {},
        }
        
        for category, models in [
            ("image", self.IMAGE_MODELS),
            ("edit", self.EDIT_MODELS),
            ("text", self.TEXT_MODELS),
        ]:
            for model, limit in models.items():
                used = usage.get(model, 0)
                result[category][model] = {
                    "limit": limit,
                    "used": used,
                    "remaining": limit - used,
                }
        
        return result
    
    def generate_image(self, prompt: str, output_name: str, size: str = "1536*1536") -> Optional[str]:
        """Generate image using best available model"""
        model = self.get_next_image_model()
        
        # Check if any quota left
        usage = self.state["usage"].get(model, 0)
        limit = self.IMAGE_MODELS.get(model, 0)
        
        if usage >= limit:
            print(f"⛔ All image models exhausted for today!")
            return None
        
        print(f"🎨 Using: {model} (used {usage}/{limit})")
        
        # Adjust size based on model requirements
        if "qwen-image-plus" in model:
            # qwen-image-plus requires specific sizes
            size = "1328*1328"  # Square format
        
        # Temporarily override the model
        original_model = self.base_generator.model
        original_fallbacks = self.base_generator.model_fallbacks
        
        self.base_generator.model = model
        self.base_generator.model_fallbacks = [model]
        
        try:
            result = self.base_generator.generate_image(prompt, output_name, size)
            if result:
                # Track usage
                self.state["usage"][model] = usage + 1
                self._save_state()
                return result
        finally:
            self.base_generator.model = original_model
            self.base_generator.model_fallbacks = original_fallbacks
        
        return None
    
    def generate_story(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate story using text model"""
        import requests
        
        # Get text model with most quota
        usage = self.state["usage"]
        best_model = None
        best_remaining = -1
        
        for model, limit in self.TEXT_MODELS.items():
            used = usage.get(model, 0)
            remaining = limit - used
            if remaining > best_remaining:
                best_remaining = remaining
                best_model = model
        
        if best_remaining <= 0:
            return "Error: Text generation quota exhausted"
        
        print(f"📝 Using: {best_model}")
        
        api_key = os.getenv("DASHSCOPE_API_KEY")
        url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": best_model,
            "input": {
                "messages": [
                    {"role": "system", "content": "You are a children's book author. Write engaging, age-appropriate stories."},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "max_tokens": max_tokens,
                "temperature": 0.8,
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                story = data["output"]["choices"][0]["message"]["content"]
                
                # Track usage
                self.state["usage"][best_model] = self.state["usage"].get(best_model, 0) + 1
                self._save_state()
                
                return story
        except Exception as e:
            print(f"Error: {e}")
        
        return ""


def main():
    rotator = AlibabaModelRotator()
    
    print("="*70)
    print("ALIBABA MODEL ROTATOR - MASSIVE FREE QUOTA")
    print("="*70)
    
    quota = rotator.get_available_quota()
    
    total_image = sum(m["remaining"] for m in quota["image"].values())
    total_edit = sum(m["remaining"] for m in quota["edit"].values())
    total_text = sum(m["remaining"] for m in quota["text"].values())
    
    print(f"\n📊 TOTAL FREE QUOTA AVAILABLE TODAY:")
    print(f"   Image Generation: {total_image}")
    print(f"   Image Editing: {total_edit}")
    print(f"   Text Generation: {total_text}")
    print(f"   ─────────────────────")
    print(f"   GRAND TOTAL: {total_image + total_edit + total_text:,}")
    
    print(f"\n🎨 Top 5 Image Models (most remaining):")
    sorted_images = sorted(quota["image"].items(), key=lambda x: x[1]["remaining"], reverse=True)[:5]
    for model, data in sorted_images:
        print(f"   {model}: {data['remaining']}/{data['limit']}")
    
    print("\n" + "="*70)
    print("TESTING GENERATION")
    print("="*70)
    
    for i in range(3):
        print(f"\n--- Image {i+1} ---")
        result = rotator.generate_image(
            f"cute cartoon animal for kids book, colorful, simple",
            f"massive_test_{i+1}"
        )
        if result:
            print(f"✅ Saved: {result}")


if __name__ == "__main__":
    main()
