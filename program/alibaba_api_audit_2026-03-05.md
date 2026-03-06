# Alibaba / Qwen API Audit (2026-03-05)

## Config Detected
- Provider endpoint: `dashscope-intl.aliyuncs.com`
- Key env var: `DASHSCOPE_API_KEY`
- Model env var: `QWEN_IMAGE_MODEL`
- Generator scripts:
  - `qwen_simple.py` (HTTP API)
  - `qwen_image_generator.py` (Alibaba SDK path)
  - `make_real_qwen_book.py` (book build with Qwen images)

## API Usage Evidence Found
No centralized request log file found.

Usage reconstructed from manifests:
- `illustrations/qwen_images/Luna_and_the_Moon_manifest.json` → 5 images
- `illustrations/qwen_images/The_Brave_Little_Seed_manifest.json` → 8 images

**Total confirmed generated via manifests:** 13 images

## Credit Guard Status
- Credit guard file expected at `.credits_state.json`
- File currently not present (no persisted daily usage state found)

## Operational Notes
- `qwen_simple.py` has built-in throttling/retry and optional credit guard.
- It currently logs to stdout only; no durable request ledger yet.

## Recommendation
Add a persistent API ledger next:
- request timestamp
- model
- prompt hash
- response status
- output file path
- error text (if any)

This will make spend tracking and production analytics reliable.
