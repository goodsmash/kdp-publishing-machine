#!/usr/bin/env python3
"""
Alibaba Model Rotator
Cycles through ALL available Alibaba models to maximize free tier usage
4x more images per day by rotating qwen-image-plus, qwen-image-2.0, wanx2.1-t2i-plus
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

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
    """Rotate through all Alibaba image models for maximum free credits"""
    
    # All available image models on Alibaba Cloud
    IMAGE_MODELS = [
        "qwen-image-plus",                    # NEW - Best quality, 1000 token prompts
        "qwen-image-2.0-pro-2026-03-03",      # Current pro
        "qwen-image-2.0-pro",                 # Standard pro
        "qwen-image-2.0",                     # Base model
        "wanx2.1-t2i-plus",                   # Alternative (Tongyi Wanx)
        "qwen-image-edit",                    # For editing existing images
    ]
    
    # Text models for story generation
    TEXT_MODELS = [
        "qwen3-max",                          # Best for stories
        "qwen3-max-2026-01-23",               # Latest
        "qwen-plus",                          # Good balance
        "qwen-turbo",                         # Fast/cheap
    ]
    
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
                if data.get("date") == today:
                    return data
            except:
                pass
        return {
            "date": today,
            "image_usage": {model: 0 for model in self.IMAGE_MODELS},
            "text_usage": {model: 0 for model in self.TEXT_MODELS},
        }
    
    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))
    
    def get_next_image_model(self) -> str:
        """Get the least-used image model"""
        usage = self.state["image_usage"]
        # Find model with lowest usage
        return min(self.IMAGE_MODELS, key=lambda m: usage.get(m, 0))
    
    def get_next_text_model(self) -> str:
        """Get the least-used text model"""
        usage = self.state["text_usage"]
        return min(self.TEXT_MODELS, key=lambda m: usage.get(m, 0))
    
    def generate_image(self, prompt: str, output_name: str, size: str = "1536*1536") -> Optional[str]:
        """Generate image using rotated model"""
        model = self.get_next_image_model()
        print(f"🎨 Using model: {model}")
        
        # Temporarily override the model
        original_model = self.base_generator.model
        self.base_generator.model = model
        
        try:
            result = self.base_generator.generate_image(prompt, output_name, size)
            if result:
                # Track usage
                self.state["image_usage"][model] = self.state["image_usage"].get(model, 0) + 1
                self._save_state()
            return result
        finally:
            self.base_generator.model = original_model
    
    def generate_story(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate story using rotated text model"""
        import requests
        
        model = self.get_next_text_model()
        print(f"📝 Using text model: {model}")
        
        api_key = os.getenv("DASHSCOPE_API_KEY")
        url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
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
                self.state["text_usage"][model] = self.state["text_usage"].get(model, 0) + 1
                self._save_state()
                
                return story
        except Exception as e:
            print(f"Error: {e}")
        
        return ""
    
    def get_status(self) -> dict:
        """Show usage across all models"""
        return {
            "date": self.state["date"],
            "image_models": self.state["image_usage"],
            "text_models": self.state["text_usage"],
            "total_images": sum(self.state["image_usage"].values()),
            "total_text": sum(self.state["text_usage"].values()),
        }


def main():
    rotator = AlibabaModelRotator()
    
    print("="*60)
    print("ALIBABA MODEL ROTATOR STATUS")
    print("="*60)
    
    status = rotator.get_status()
    print(f"\nDate: {status['date']}")
    print(f"\nImage Models Used:")
    for model, count in status["image_models"].items():
        print(f"  {model}: {count}")
    print(f"\nTotal Images Today: {status['total_images']}")
    
    print(f"\nText Models Used:")
    for model, count in status["text_models"].items():
        print(f"  {model}: {count}")
    print(f"\nTotal Text Gen Today: {status['total_text']}")
    
    # Test generation
    print("\n" + "="*60)
    print("TESTING ROTATION")
    print("="*60)
    
    # Generate 3 images to show rotation
    for i in range(3):
        print(f"\n--- Image {i+1} ---")
        result = rotator.generate_image(
            f"cute cartoon animal for kids book, colorful, simple",
            f"test_rotation_{i+1}"
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
