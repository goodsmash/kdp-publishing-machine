#!/usr/bin/env python3
"""
One Image At A Time - Premium Quality
Generate images one by one with full quality control
"""

from pathlib import Path
from alibaba_model_rotator import AlibabaModelRotator

rotator = AlibabaModelRotator()

# African Safari Animals - one at a time
animals = [
    {
        "word": "elephant", 
        "prompt": "Hyper-realistic 3D render of African elephant with large tusks, wrinkled grey skin at watering hole, Pixar quality, subsurface skin scattering, volumetric lighting, ray-traced reflections, 8K texture detail, cinematic composition, educational children's book style"
    },
    {
        "word": "giraffe",
        "prompt": "Hyper-realistic 3D render of tall giraffe with spotted pattern reaching for acacia tree leaves, African savanna background, Pixar animation quality, volumetric lighting, ray-traced reflections, 8K detail, cinematic composition, educational children's book illustration"
    },
    {
        "word": "zebra",
        "prompt": "Hyper-realistic 3D render of plains zebra with distinctive black and white stripe pattern, grassland background, Pixar quality, subsurface scattering, volumetric lighting, 8K detail, cinematic composition, educational children's book style"
    },
    {
        "word": "rhino",
        "prompt": "Hyper-realistic 3D render of white rhinoceros with two horns, thick armored skin, dust bath, African plains, Pixar animation quality, volumetric lighting, ray-traced reflections, 8K texture detail, cinematic composition, educational children's book illustration"
    },
    {
        "word": "hippo",
        "prompt": "Hyper-realistic 3D render of hippopotamus partially submerged in river, pinkish grey skin, water reflections, Pixar quality, subsurface scattering, volumetric lighting, 8K detail, cinematic composition, educational children's book style"
    },
]

print("="*70)
print("PREMIUM IMAGE GENERATION - ONE AT A TIME")
print("="*70)

for i, animal in enumerate(animals, 1):
    word = animal["word"]
    prompt = animal["prompt"]
    
    print(f"\n{'='*70}")
    print(f"IMAGE {i}/{len(animals)}: {word.upper()}")
    print(f"{'='*70}")
    print(f"Prompt:\n{prompt}\n")
    
    result = rotator.generate_image(prompt, f"premium_{word}")
    
    if result:
        print(f"✅ SUCCESS: {result}")
    else:
        print(f"❌ FAILED")
    
    print(f"\n{'='*70}")
    import time
    time.sleep(3)  # Auto-continue after 3 seconds

print("\n✅ All images generated!")
