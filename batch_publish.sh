#!/bin/bash
# KDP Publishing Machine - Batch Production Script
# Generates multiple books for Amazon KDP

set -e

MACHINE_DIR="/home/goodsmash/.openclaw/workspace/kdp-publishing-machine"
cd "$MACHINE_DIR"

echo "=========================================="
echo "  KDP PUBLISHING MACHINE - BATCH MODE"
echo "=========================================="
echo ""

# Check arguments
LANG=${1:-"en"}
COUNT=${2:-5}
SIZE=${3:-"8x10"}

echo "Configuration:"
echo "  Language: $LANG"
echo "  Books to generate: $COUNT"
echo "  Trim size: $SIZE"
echo ""

# Create directories
mkdir -p output stories prompts

# Step 1: Generate Kimi prompts
echo "📋 Step 1: Generating Kimi prompts..."
python3 story_generator.py "$LANG" "$COUNT"

echo ""
echo "📝 NEXT STEPS:"
echo "   1. Open prompts/kimi_prompts_${LANG}_${COUNT}.txt"
echo "   2. Copy each prompt into Kimi (kimi.com)"
echo "   3. Save Kimi's responses to stories/ folder"
echo "   4. Run: bash batch_publish.sh process"
echo ""

# If process argument given, convert stories to PDFs
if [ "$4" == "process" ]; then
    echo "📚 Step 2: Converting stories to KDP-ready PDFs..."
    
    for story_file in stories/*.txt; do
        if [ -f "$story_file" ]; then
            echo "Processing: $story_file"
            # TODO: Add parser to convert Kimi output to PDF
            # For now, use built-in templates
        fi
    done
    
    echo ""
    echo "✅ Batch complete! Check output/ folder"
fi

# Quick mode: Generate from built-in templates
echo ""
echo "🚀 QUICK MODE: Generating from built-in templates..."
python3 publishing_machine.py brave_seed "$LANG" "$SIZE"

if [ "$LANG" == "es" ]; then
    python3 publishing_machine.py semilla_valiente "$LANG" "$SIZE"
fi

echo ""
echo "=========================================="
echo "  PRODUCTION SUMMARY"
echo "=========================================="
echo "Output location: $MACHINE_DIR/output/"
ls -lh output/*.pdf 2>/dev/null || echo "No PDFs generated yet"
echo ""
echo "📤 UPLOAD TO KDP:"
echo "   1. Go to kdp.amazon.com"
echo "   2. Create New Title → Paperback"
echo "   3. Upload PDF from output/ folder"
echo "   4. Use metadata JSON for description/keywords"
echo "   5. Price: $8.99-$12.99 (color), $6.99-$9.99 (B&W)"
echo ""
