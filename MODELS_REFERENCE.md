# Alibaba Cloud DashScope Models Reference

## Current Image Models Available

### Qwen Image Generation
| Model | Description | Best For |
|-------|-------------|----------|
| `qwen-image-2.0-pro-2026-03-03` | Latest pro version | High-quality illustrations |
| `qwen-image-2.0-pro` | Standard pro | General illustrations |
| `qwen-image-2.0` | Base version | Faster, cheaper |

### Text Models (for story generation)
| Model | Description |
|-------|-------------|
| `qwen-plus` | Strong general model |
| `qwen-max` | Most capable |
| `qwen-flash` | Fast, cost-effective |
| `qwen3.5-flash` | Latest flash model |

## When Qwen Credits Run Out - Alternatives

### 1. **OpenAI DALL-E 3** (Paid)
```python
from openai import OpenAI
client = OpenAI(api_key="your-key")

response = client.images.generate(
    model="dall-e-3",
    prompt="cute children's book illustration of a puppy",
    size="1024x1024",
    quality="standard",
    n=1,
)
```

### 2. **Stability AI (Stable Diffusion)**
```python
import requests

response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={"Authorization": "Bearer YOUR_KEY"},
    files={"none": ''},
    data={
        "prompt": "children's book style illustration of a cat",
        "output_format": "png",
    },
)
```

### 3. **Leonardo AI** (Free tier available)
```python
import requests

response = requests.post(
    "https://cloud.leonardo.ai/api/rest/v1/generations",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={
        "prompt": "cute cartoon animal for kids book",
        "modelId": "e71a1c2f-4f94-4e67-9b53-123456789",
        "width": 1024,
        "height": 1024,
    }
)
```

### 4. **Hugging Face (Free Models)**
```python
from huggingface_hub import InferenceClient

client = InferenceClient(token="YOUR_TOKEN")
image = client.text_to_image(
    "children's book illustration of a bunny",
    model="stabilityai/stable-diffusion-xl-base-1.0"
)
```

### 5. **Local Models (No API costs)**
- Stable Diffusion with AUTOMATIC1111
- FLUX models via ComfyUI
- Requires GPU but zero ongoing API costs

## Credit Management Strategy

### Daily Rotation
```python
PROVIDERS = [
    {"name": "alibaba", "credits": 50, "used": 0},
    {"name": "stability", "credits": 25, "used": 0},
    {"name": "leonardo", "credits": 150, "used": 0},
]

# Rotate when one runs out
def get_available_provider():
    for p in PROVIDERS:
        if p["used"] < p["credits"]:
            return p["name"]
    return None  # All out - use local
```

### Cost Comparison
| Provider | Cost per 1000 images | Quality | Speed |
|----------|---------------------|---------|-------|
| Alibaba/Qwen | ~$0.50 (free tier) | ★★★★★ | Fast |
| OpenAI DALL-E 3 | $40 | ★★★★★ | Medium |
| Stability AI | $10 | ★★★★☆ | Fast |
| Leonardo | $8 (or free tier) | ★★★★☆ | Medium |
| Hugging Face | Free | ★★★☆☆ | Slow |
| Local SD | $0 (GPU cost) | ★★★★☆ | Depends |

## Recommended Setup

### Tier 1 (Daily Production)
- Alibaba Qwen: 50 images/day (free tier)

### Tier 2 (Backup)
- Leonardo AI: 150 images/day (free tier)

### Tier 3 (Overflow)
- Hugging Face: Unlimited (slower)

### Tier 4 (Emergency)
- Local Stable Diffusion (requires GPU)

## Implementation

Add to your `.env`:
```bash
# Primary
DASHSCOPE_API_KEY=your-alibaba-key

# Fallbacks
LEONARDO_API_KEY=your-leonardo-key
STABILITY_API_KEY=your-stability-key
HUGGINGFACE_TOKEN=your-hf-token
OPENAI_API_KEY=your-openai-key
```
