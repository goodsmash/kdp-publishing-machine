# 🚀 KDP Publishing Machine Pro

**Professional children's book generator for Amazon KDP**  
Generate unlimited books in English & Spanish with AI-powered story creation.

---

## ✅ What's Included

### Generated Books (Ready to Upload)
| Book | Language | Pages | Age | Size | Status |
|------|----------|-------|-----|------|--------|
| The Brave Little Seed | English | 36 | 4-7 | 8x10" | ✅ Ready |
| La Semillita Valiente | Spanish | 36 | 4-7 | 8x10" | ✅ Ready |

### AI Story Prompts
- **20 English prompts** in `prompts/kimi_prompts_en_20.txt`
- **20 Spanish prompts** in `prompts/kimi_prompts_es_20.txt`
- Copy → Paste into Kimi → Get unique stories

---

## 📋 Amazon KDP Best Practices Implemented

### ✅ Formatting
- [x] **Bleed support** (0.125") for full-bleed illustrations
- [x] **Proper trim sizes**: 8x10", 8.5x8.5", 7x10", 6x9", 5.5x8.5"
- [x] **Gutter margins** (0.75" inner) for binding
- [x] **300 DPI placeholder** specs for illustrations
- [x] **Copyright pages** with ISBN placeholders
- [x] **Dedication pages**
- [x] **Professional typography** (age-appropriate font sizes)

### ✅ Content
- [x] Age-specific vocabulary (2-4, 4-7, 5-7, 6-8, 8-10)
- [x] Vocabulary learning pages with definitions
- [x] Example sentences for new words
- [x] Series formatting (book numbers, consistent branding)
- [x] Back matter for series promotion

### ✅ Metadata
- [x] Auto-generated JSON metadata files
- [x] Keywords optimized for KDP
- [x] BISAC category suggestions
- [x] Age range specifications
- [x] Pricing recommendations

---

## 🚀 Quick Start

### 1. Generate Built-in Books
```bash
cd /home/goodsmash/.openclaw/workspace/kdp-publishing-machine

# English book
python3 publishing_machine.py brave_seed en 8x10

# Spanish book
python3 publishing_machine.py semilla_valiente es 8x10

# Different sizes
python3 publishing_machine.py brave_seed en 8.5x8.5
python3 publishing_machine.py brave_seed en 6x9
```

### 2. Create AI-Powered Stories with Kimi
```bash
# Generate 20 Kimi prompts
cd /home/goodsmash/.openclaw/workspace/kdp-publishing-machine
python3 story_generator.py en 20

# Open the prompts file
cat prompts/kimi_prompts_en_20.txt
```

**Workflow:**
1. Copy a prompt from the text file
2. Paste into [kimi.com](https://kimi.com)
3. Kimi generates a unique story
4. Save response to `stories/story_001.txt`
5. Convert to PDF (parser coming soon)

### 3. Batch Production
```bash
bash batch_publish.sh en 5 8x10
```

---

## 📊 Trim Size Guide

| Size | Best For | Bleed | Price Range |
|------|----------|-------|-------------|
| **8x10"** | Picture books | Yes | $9.99-$14.99 |
| **8.5x8.5"** | Square illustrations | Yes | $9.99-$13.99 |
| **7x10"** | Chapter books | Yes | $8.99-$12.99 |
| **6x9"** | Early readers | No | $6.99-$9.99 |
| **5.5x8.5"** | Pocket books | No | $5.99-$8.99 |

---

## 🎨 Color Palettes

Each book uses a professional color palette:
- **Warm**: Coral & gold tones
- **Cool**: Blues & teals
- **Pastel**: Soft pinks & creams
- **Nature**: Greens & browns
- **Bedtime**: Purples & soft grays

---

## 📝 KDP Upload Checklist

### Before Uploading:
- [ ] PDF opens correctly in Adobe Reader
- [ ] All fonts embedded (Helvetica standard)
- [ ] Images at 300 DPI (if added)
- [ ] Page count within KDP limits (24-480)
- [ ] Trim size matches PDF dimensions

### KDP Setup:
1. **kdp.amazon.com** → Create New Title
2. **Paperback** (not ebook)
3. **Language**: English or Español
4. **Book Title**: Copy from metadata JSON
5. **Series**: Enter series name if applicable
6. **Description**: Use the "description" field from metadata
7. **Keywords**: Copy from metadata "keywords" array
8. **Categories**: Select from metadata "categories"
9. **Age Range**: Set from metadata
10. **Upload PDF**: Select your generated PDF
11. **Cover Creator**: Use KDP's tool or upload custom
12. **Pricing**:
    - US: $9.99 (B&W), $12.99 (Color)
    - UK: £7.99 / £9.99
    - EU: €8.99 / €11.99

---

## 📚 Series Ideas

### English Series:
1. **Nature Friends** (animals, plants, seasons)
2. **Little Learners** (shapes, colors, numbers)
3. **Bedtime Stories** (calm, soothing tales)
4. **Adventure Kids** (exploring, trying new things)
5. **Emotion Explorers** (feelings, social skills)

### Spanish Series:
1. **Amigos de la Naturaleza**
2. **Pequeños Exploradores**
3. **Cuentos para Dormir**
4. **Aventuras Divertidas**
5. **Descubriendo Emociones**

---

## 💡 Pro Tips

### Volume Publishing:
- Publish 2-3 books per week for 3 months = 24-36 books
- Creates a "brand" on Amazon
- Cross-promote series books
- Bundle 3 books for higher price point

### Marketing:
- Use Amazon Advertising (budget $5-10/day)
- Create A+ Content for series page
- Run Kindle Countdown Deals
- Build email list with free coloring pages

### Quality:
- Add professional illustrations (hire on Fiverr/Upwork)
- Get beta readers for each age group
- Update books based on reviews
- Create hardcover editions for bestsellers

---

## 📁 File Structure

```
kdp-publishing-machine/
├── publishing_machine.py      # Main PDF generator
├── story_generator.py         # Kimi prompt generator
├── batch_publish.sh          # Batch production script
├── output/                   # Generated PDFs
│   ├── The_Brave_Little_Seed_8x10.pdf
│   ├── The_Brave_Little_Seed_metadata.json
│   └── ...
├── prompts/                  # Kimi prompts
│   ├── kimi_prompts_en_20.txt
│   └── kimi_prompts_es_20.txt
├── stories/                  # Kimi responses (you add)
└── templates/               # Future templates
```

---

## 🔧 Advanced Features

### Custom Stories
Edit `publishing_machine.py` → `STORY_LIBRARY` to add your own stories.

### New Languages
Add to `STORY_LIBRARY` with language code (fr, de, it, etc.)

### Custom Illustrations
Replace placeholder boxes with:
```python
self.c.drawImage("illustration.jpg", x, y, width, height)
```

### Series Branding
Update `PALETTES` for consistent series colors.

---

## 📈 Success Metrics

Track your books:
- **Days 1-30**: 0-5 sales (normal)
- **Days 31-90**: 5-20 sales (building)
- **Days 90+**: 20+ sales monthly (momentum)
- **Goal**: 10 books earning $50/month each = $500/month passive

---

## 🆘 Support

**Common Issues:**
- **PDF won't upload**: Check file size (< 650MB), ensure 24+ pages
- **Margins wrong**: Use correct trim size code (8x10, not 8x10")
- **Fonts missing**: Install Helvetica or use standard PDF fonts

**Next Steps:**
1. Generate 5 books this week
2. Upload to KDP
3. Order author copies (proofs)
4. Review physical books
5. Publish and promote

---

## 🎯 30-Day Challenge

**Week 1**: Generate 5 books, upload to KDP  
**Week 2**: Order proofs, review quality, publish  
**Week 3**: Create 5 more books, start ads  
**Week 4**: Analyze sales, optimize keywords  

**Goal**: 10 published books by Day 30

---

**Ready to build your publishing empire?** Start with `bash batch_publish.sh`
