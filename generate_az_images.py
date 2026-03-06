#!/usr/bin/env python3
"""
Generate all 26 A-Z animal images
Run daily until all 26 are complete
"""

from pathlib import Path
from alibaba_model_rotator import AlibabaModelRotator
import time

ROOT = Path(__file__).resolve().parent
IMG_DIR = ROOT / "illustrations" / "az_animals"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# All 26 animals with educational prompts
ANIMALS = {
    "alligator": "scientifically accurate American alligator, detailed scales, swamp habitat, educational wildlife photography style, realistic",
    "bear": "scientifically accurate grizzly bear, thick fur texture, powerful build, forest background, educational nature documentary style",
    "cheetah": "scientifically accurate cheetah, spotted coat, lean build, African savanna, educational wildlife photography",
    "dolphin": "scientifically accurate bottlenose dolphin, smooth skin, ocean water, educational marine biology style",
    "elephant": "scientifically accurate African elephant, wrinkled skin, large tusks, savanna background, educational nature style",
    "fox": "scientifically accurate red fox, bushy tail, pointed ears, forest setting, educational wildlife photography",
    "gorilla": "scientifically accurate silverback gorilla, muscular build, dark fur, jungle background, educational primate documentary",
    "hippopotamus": "scientifically accurate hippopotamus, large body, pinkish grey skin, river water, educational African wildlife",
    "iguana": "scientifically accurate green iguana, spiny crest, scaly skin, tropical tree, educational reptile photography",
    "jaguar": "scientifically accurate jaguar, rosette spots, muscular build, Amazon rainforest, educational big cat documentary",
    "kangaroo": "scientifically accurate red kangaroo, powerful hind legs, pouch, Australian outback, educational marsupial photo",
    "lion": "scientifically accurate male lion, golden mane, majestic pose, African savanna, educational wildlife photography",
    "moose": "scientifically accurate bull moose, large palmate antlers, dark fur, northern forest, educational North American wildlife",
    "newt": "scientifically accurate eastern newt, bright orange color, moist skin, forest floor, educational amphibian photography",
    "octopus": "scientifically accurate giant Pacific octopus, eight arms, textured skin, ocean floor, educational marine biology",
    "penguin": "scientifically accurate emperor penguin, black and white plumage, ice background, educational Antarctic wildlife",
    "quail": "scientifically accurate California quail, distinctive plume, ground bird, grassland setting, educational bird photography",
    "rhinoceros": "scientifically accurate white rhinoceros, two horns, thick grey skin, African grassland, educational wildlife",
    "seal": "scientifically accurate harbor seal, smooth grey fur, whiskers, rocky shore, educational marine mammal photography",
    "tiger": "scientifically accurate Bengal tiger, orange with black stripes, powerful stance, jungle background, educational big cat",
    "urchin": "scientifically accurate purple sea urchin, spherical shape, long spines, ocean floor, educational marine invertebrate",
    "vulture": "scientifically accurate turkey vulture, bald red head, large wings, soaring flight, educational bird of prey",
    "walrus": "scientifically accurate Pacific walrus, large tusks, whiskered muzzle, Arctic ice, educational marine mammal",
    "xenops": "scientifically accurate plain xenops, small brown bird, tree trunk foraging, rainforest setting, educational tropical bird",
    "yak": "scientifically accurate domestic yak, long shaggy hair, large horns, Himalayan mountains, educational livestock photography",
    "zebra": "scientifically accurate plains zebra, black and white stripes, African savanna, educational equid wildlife",
}


def main():
    rotator = AlibabaModelRotator()
    
    print("="*70)
    print("A-Z ANIMAL IMAGE GENERATION")
    print("="*70)
    
    # Check which images already exist
    existing = [f.stem.replace("az_", "") for f in IMG_DIR.glob("az_*.png")]
    print(f"\nAlready have: {len(existing)} images")
    
    remaining = {k: v for k, v in ANIMALS.items() if k not in existing}
    print(f"Need to generate: {len(remaining)} images")
    
    if not remaining:
        print("\n✅ All 26 images complete!")
        return
    
    print("\nGenerating images (will stop at daily limit)...")
    print("-" * 70)
    
    for animal, prompt in remaining.items():
        print(f"\n📸 {animal.title()}")
        
        result = rotator.generate_image(prompt, f"az_{animal}", size="1328*1328")
        
        if result:
            print(f"   ✅ {result}")
        else:
            print(f"   ❌ Failed or limit reached")
            print("\n⏹️  Stopping. Run again tomorrow to continue.")
            break
        
        time.sleep(3)
    
    # Check final count
    final_count = len(list(IMG_DIR.glob("az_*.png")))
    print(f"\n{'='*70}")
    print(f"Progress: {final_count}/26 images complete")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
