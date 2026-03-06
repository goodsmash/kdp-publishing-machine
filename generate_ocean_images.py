#!/usr/bin/env python3
"""Generate all ocean images with proper sizes"""
import os
from pathlib import Path
from alibaba_model_rotator import AlibabaModelRotator
import time

rotator = AlibabaModelRotator()

ocean_animals = [
    ("fish", "colorful tropical fish swimming in coral reef, children's book illustration, bright colors"),
    ("shark", "friendly cartoon shark smiling, underwater scene, children's book style"),
    ("whale", "cute blue whale spouting water, ocean background, children's illustration"),
    ("turtle", "cute sea turtle with shell, underwater, children's book art"),
    ("octopus", "friendly pink octopus with tentacles, ocean floor, kids book style"),
    ("crab", "cute red crab on sandy beach, children's illustration"),
    ("starfish", "colorful starfish on ocean floor, children's book art"),
    ("seahorse", "cute yellow seahorse swimming, coral reef, kids illustration"),
]

print("="*60)
print("GENERATING OCEAN IMAGES")
print("="*60)

for word, prompt in ocean_animals:
    img_path = Path(f"illustrations/qwen_images/ocean_{word}_20260305_194257.png")
    if img_path.exists():
        print(f"✓ {word}: Already exists")
        continue
    
    print(f"\n🎨 Generating: {word}")
    result = rotator.generate_image(prompt, f"ocean_{word}", size="1328*1328")
    if result:
        print(f"✅ {word}: {result}")
    else:
        print(f"❌ {word}: Failed")
    time.sleep(2)

print("\n✅ Done!")
