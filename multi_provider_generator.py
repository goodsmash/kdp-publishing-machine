#!/usr/bin/env python3
"""
Multi-Provider Image Generator
Automatically falls back when one provider runs out of credits
Supports: Alibaba/Qwen, Leonardo AI, Stability AI, Hugging Face
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List

ROOT = Path(__file__).resolve().parent
PROVIDER_STATE_FILE = ROOT / ".provider_state.json"

# Load .env file
env_path = ROOT / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key, value)


@dataclass
class Provider:
    name: str
    generator_func: callable
    daily_limit: int
    priority: int = 1


class MultiProviderImageGenerator:
    """Smart image generator with automatic fallback"""
    
    def __init__(self):
        self.ledger_path = ROOT / "program" / "api_ledger.jsonl"
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
        self.providers = self._init_providers()
        
    def _load_state(self) -> dict:
        """Load daily usage state"""
        today = datetime.now().strftime("%Y-%m-%d")
        if PROVIDER_STATE_FILE.exists():
            try:
                data = json.loads(PROVIDER_STATE_FILE.read_text())
                if data.get("date") == today:
                    return data
            except:
                pass
        return {"date": today, "usage": {}}
    
    def _save_state(self):
        PROVIDER_STATE_FILE.write_text(json.dumps(self.state, indent=2))
    
    def _init_providers(self) -> List[Provider]:
        """Initialize available providers"""
        providers = []
        
        # Alibaba Qwen (Primary)
        if os.getenv("DASHSCOPE_API_KEY"):
            from qwen_simple import SimpleQwenGenerator
            qwen = SimpleQwenGenerator()
            providers.append(Provider(
                name="alibaba_qwen",
                generator_func=lambda prompt, name: qwen.generate_image(prompt, name),
                daily_limit=50,  # Free tier safe limit
                priority=1
            ))
        
        # Leonardo AI (Fallback 1)
        if os.getenv("LEONARDO_API_KEY"):
            providers.append(Provider(
                name="leonardo",
                generator_func=self._generate_leonardo,
                daily_limit=150,  # Free tier
                priority=2
            ))
        
        # Hugging Face (Fallback 2 - Free but slower)
        if os.getenv("HUGGINGFACE_TOKEN"):
            providers.append(Provider(
                name="huggingface",
                generator_func=self._generate_hf,
                daily_limit=9999,  # Effectively unlimited
                priority=3
            ))
        
        # Sort by priority
        providers.sort(key=lambda p: p.priority)
        return providers
    
    def _generate_leonardo(self, prompt: str, output_name: str) -> Optional[str]:
        """Generate using Leonardo AI"""
        import requests
        
        api_key = os.getenv("LEONARDO_API_KEY")
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "modelId": "e71a1c2f-4f94-4e67-9b53-123456789",  # Leonardo Kino
            "width": 1024,
            "height": 1024,
            "num_images": 1,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            if response.status_code == 200:
                data = response.json()
                generation_id = data["sdGenerationJob"]["generationId"]
                
                # Poll for result
                for _ in range(30):
                    time.sleep(2)
                    check = requests.get(f"{url}/{generation_id}", headers=headers)
                    if check.status_code == 200:
                        result = check.json()
                        if result.get("generations_by_pk", {}).get("status") == "COMPLETE":
                            image_url = result["generations_by_pk"]["generated_images"][0]["url"]
                            # Download image
                            img_response = requests.get(image_url, timeout=60)
                            if img_response.status_code == 200:
                                output_dir = ROOT / "illustrations" / "leonardo_images"
                                output_dir.mkdir(parents=True, exist_ok=True)
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = output_dir / f"{output_name}_{timestamp}.png"
                                filename.write_bytes(img_response.content)
                                return str(filename)
            return None
        except Exception as e:
            print(f"Leonardo error: {e}")
            return None
    
    def _generate_hf(self, prompt: str, output_name: str) -> Optional[str]:
        """Generate using Hugging Face Inference API"""
        from huggingface_hub import InferenceClient
        
        try:
            client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
            image = client.text_to_image(
                prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0"
            )
            
            output_dir = ROOT / "illustrations" / "hf_images"
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = output_dir / f"{output_name}_{timestamp}.png"
            image.save(filename)
            return str(filename)
        except Exception as e:
            print(f"HF error: {e}")
            return None
    
    def generate_image(self, prompt: str, output_name: str, size: str = "1024x1024") -> Optional[str]:
        """Generate image using best available provider"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        if self.state.get("date") != today:
            self.state = {"date": today, "usage": {}}
        
        # Try each provider in priority order
        for provider in self.providers:
            usage = self.state["usage"].get(provider.name, 0)
            
            if usage >= provider.daily_limit:
                print(f"⏭️  {provider.name}: limit reached ({usage}/{provider.daily_limit})")
                continue
            
            print(f"🎨 Trying {provider.name}...")
            result = provider.generator_func(prompt, output_name)
            
            if result:
                # Log success
                self.state["usage"][provider.name] = usage + 1
                self._save_state()
                self._log_success(provider.name, prompt, output_name, result)
                print(f"✅ Success with {provider.name}")
                return result
            else:
                print(f"❌ {provider.name} failed, trying next...")
        
        print("⛔ All providers exhausted!")
        return None
    
    def _log_success(self, provider: str, prompt: str, output_name: str, result: str):
        """Log to ledger"""
        entry = {
            "ts": datetime.now().isoformat(),
            "provider": provider,
            "event": "success",
            "prompt": prompt[:50],
            "output_name": output_name,
            "file": result
        }
        with self.ledger_path.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_status(self) -> dict:
        """Get current provider status"""
        status = {
            "date": self.state.get("date"),
            "providers": []
        }
        for provider in self.providers:
            usage = self.state["usage"].get(provider.name, 0)
            status["providers"].append({
                "name": provider.name,
                "used": usage,
                "limit": provider.daily_limit,
                "remaining": provider.daily_limit - usage,
                "available": usage < provider.daily_limit
            })
        return status


if __name__ == "__main__":
    gen = MultiProviderImageGenerator()
    print("Multi-Provider Image Generator Status:")
    print("=" * 50)
    status = gen.get_status()
    for p in status["providers"]:
        print(f"{p['name']}: {p['used']}/{p['limit']} ({p['remaining']} remaining)")
    
    # Test generation
    print("\nTesting image generation...")
    result = gen.generate_image(
        "cute cartoon elephant for children's book, bright colors, simple background",
        "test_elephant"
    )
    print(f"Result: {result}")
