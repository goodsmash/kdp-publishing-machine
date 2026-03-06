# Alibaba Cloud Model Studio - All Available Models

## 🎨 Image Generation Models

### Current (What We Use)
| Model | Type | Best For |
|-------|------|----------|
| `qwen-image-2.0-pro-2026-03-03` | Image Gen | Highest quality illustrations |
| `qwen-image-2.0-pro` | Image Gen | Professional illustrations |
| `qwen-image-2.0` | Image Gen | Fast generation |

### NEW - Even Better Models
| Model | Type | Best For |
|-------|------|----------|
| `qwen-image-plus` | Image Gen | Complex text rendering, 1000-token prompts |
| `qwen-image-edit` | Image Edit | Edit existing images, add/remove objects |
| `wanx2.1-t2i-plus` | Image Gen | Tongyi Wanx series (Alibaba's DALL-E) |

## 📝 Text/Story Generation Models

| Model | Type | Best For |
|-------|------|----------|
| `qwen3-max` | Text | Best for story writing |
| `qwen3-max-2026-01-23` | Text | Latest version |
| `qwen-plus` | Text | General purpose |
| `qwen-turbo` | Text | Fast, cheaper |
| `qwen3-coder-plus` | Code | If we build tools |

## 🎬 Multimodal (NEW!)

| Model | Type | Best For |
|-------|------|----------|
| `qwen3-omni` | Multimodal | Text + Image + Audio + Video |
| `qwen-vl-plus` | Vision | Image understanding |

## 🎯 Recommended Setup for KDP Books

### For Illustrations (Priority Order):
```python
IMAGE_MODELS = [
    "qwen-image-plus",           # NEW - Best quality
    "qwen-image-2.0-pro-2026-03-03",  # Current
    "qwen-image-2.0-pro",        # Fallback
    "wanx2.1-t2i-plus",          # Alternative
]
```

### For Story Text:
```python
STORY_MODELS = [
    "qwen3-max",                 # Best stories
    "qwen-plus",                 # Good balance
    "qwen-turbo",                # Fast/cheap
]
```

## 💰 Credit Usage Strategy

All these models SHARE the same Alibaba Cloud credit pool!

**Daily Free Tier (approximate):**
- Image generation: ~50-100 images
- Text generation: ~1000-2000 requests
- Total combined usage matters

**To Maximize:**
1. Use `qwen-turbo` for quick drafts
2. Use `qwen3-max` for final story polish
3. Use `qwen-image-plus` for premium illustrations
4. Use `qwen-image-edit` to modify existing images instead of regenerating

## 🔧 Updated Code

Change in `qwen_simple.py`:
```python
MODEL_FALLBACKS = [
    "qwen-image-plus",                    # Try this first!
    "qwen-image-2.0-pro-2026-03-03",      # Then this
    "qwen-image-2.0-pro",
    "wanx2.1-t2i-plus",                   # Alternative model
]
```

## 📚 Model-Specific Use Cases

### qwen-image-plus
- **Better at:** Text in images, complex scenes
- **Prompt length:** Up to 1000 tokens
- **Use for:** Book covers with titles

### qwen-image-edit
- **Input:** Existing image + text prompt
- **Use for:** Modifying illustrations, adding characters

### wanx2.1-t2i-plus
- **Style:** More artistic/DALL-E like
- **Use for:** Different illustration styles

### qwen3-max (text)
- **Best for:** Writing complete stories
- **Context:** Longer stories, better coherence

## ⚡ Smart Rotation

Rotate through ALL models to maximize free credits:

```python
ALIBABA_MODELS = {
    "image": [
        "qwen-image-plus",
        "qwen-image-2.0-pro-2026-03-03", 
        "qwen-image-2.0-pro",
        "wanx2.1-t2i-plus",
    ],
    "text": [
        "qwen3-max",
        "qwen-plus",
        "qwen-turbo",
    ],
    "edit": [
        "qwen-image-edit",
    ]
}
```

This gives you 4x more image generations per day!
