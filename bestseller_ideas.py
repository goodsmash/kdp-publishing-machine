#!/usr/bin/env python3
"""
Bestseller Book Ideas Generator
High-demand KDP niches with proven sales potential
"""

BESTSELLER_IDEAS = {
    "educational_workbooks": {
        "category": "Educational Workbooks",
        "market_size": "Massive - parents always buying",
        "price_range": "$6.99 - $12.99",
        "target_audience": "Parents of kids ages 2-8",
        "books": [
            {
                "title": "My First Learn-to-Write Workbook",
                "subtitle": "Practice for Kids with Pen Control, Line Tracing, Letters, and More!",
                "ages": "3-5",
                "pages": "100-120",
                "competitor_price": "$8.99",
                "monthly_sales_estimate": "500-2000",
                "keywords": ["handwriting", "preschool", "tracing", "letters", "practice"]
            },
            {
                "title": "Preschool Math Workbook",
                "subtitle": "Counting, Addition, and Number Recognition for Ages 3-5",
                "ages": "3-5",
                "pages": "80-100",
                "competitor_price": "$7.99",
                "monthly_sales_estimate": "300-1500",
                "keywords": ["math", "counting", "numbers", "preschool", "addition"]
            },
            {
                "title": "Sight Words Practice Book",
                "subtitle": "100 High-Frequency Words for Beginning Readers",
                "ages": "4-7",
                "pages": "120-150",
                "competitor_price": "$9.99",
                "monthly_sales_estimate": "400-1800",
                "keywords": ["sight words", "reading", "kindergarten", "phonics"]
            },
            {
                "title": "My Big Kindergarten Workbook",
                "subtitle": "All-in-One Learning: Letters, Numbers, Shapes, and More!",
                "ages": "5-6",
                "pages": "150-200",
                "competitor_price": "$12.99",
                "monthly_sales_estimate": "600-2500",
                "keywords": ["kindergarten", "workbook", "curriculum", "prep"]
            },
            {
                "title": "Cursive Handwriting Workbook",
                "subtitle": "Learn Beautiful Cursive Writing: Letters, Words, and Sentences",
                "ages": "7-10",
                "pages": "100-120",
                "competitor_price": "$8.99",
                "monthly_sales_estimate": "200-1000",
                "keywords": ["cursive", "handwriting", "writing", "school"]
            },
            {
                "title": "Spanish for Kids Workbook",
                "subtitle": "First Words, Numbers, Colors - Beginner Spanish Practice",
                "ages": "4-8",
                "pages": "100-120",
                "competitor_price": "$9.99",
                "monthly_sales_estimate": "150-800",
                "keywords": ["spanish", "bilingual", "language learning", "espanol"]
            }
        ]
    },
    
    "activity_books": {
        "category": "Activity & Puzzle Books",
        "market_size": "Very Large - entertainment + education",
        "price_range": "$5.99 - $9.99",
        "target_audience": "Parents seeking screen-free activities",
        "books": [
            {
                "title": "My First Mazes Book",
                "subtitle": "50 Fun Mazes for Kids Ages 4-6",
                "ages": "4-6",
                "pages": "60-80",
                "competitor_price": "$6.99",
                "monthly_sales_estimate": "400-1500",
                "keywords": ["mazes", "puzzles", "problem solving", "fun"]
            },
            {
                "title": "Dot-to-Dot for Kids",
                "subtitle": "Connect the Dots and Discover Fun Pictures!",
                "ages": "4-8",
                "pages": "80-100",
                "competitor_price": "$7.99",
                "monthly_sales_estimate": "300-1200",
                "keywords": ["dot to dot", "connect", "drawing", "numbers"]
            },
            {
                "title": "I Spy Everything!",
                "subtitle": "A Fun Guessing Game for Kids 2-5",
                "ages": "2-5",
                "pages": "40-60",
                "competitor_price": "$6.99",
                "monthly_sales_estimate": "800-3000",
                "keywords": ["i spy", "search and find", "guessing game"]
            },
            {
                "title": "Hidden Pictures Puzzle Book",
                "subtitle": "Can You Find All the Objects?",
                "ages": "5-8",
                "pages": "60-80",
                "competitor_price": "$7.99",
                "monthly_sales_estimate": "300-1200",
                "keywords": ["hidden pictures", "search", "find it", "puzzles"]
            },
            {
                "title": "Scratch and Sniff Stickers Activity Book",
                "subtitle": "Fun with Smelly Stickers! (Note: Requires sticker sheets)",
                "ages": "3-7",
                "pages": "40-50",
                "competitor_price": "$8.99",
                "monthly_sales_estimate": "200-800",
                "keywords": ["stickers", "activity", "scratch and sniff"]
            }
        ]
    },
    
    "coloring_books": {
        "category": "Coloring Books",
        "market_size": "Huge - evergreen niche",
        "price_range": "$4.99 - $7.99",
        "target_audience": "Kids 2-10 and parents looking for creative activities",
        "books": [
            {
                "title": "Cute Animals Coloring Book",
                "subtitle": "50 Adorable Animals to Color for Kids Ages 2-4",
                "ages": "2-4",
                "pages": "50-60",
                "competitor_price": "$5.99",
                "monthly_sales_estimate": "1000-5000",
                "keywords": ["coloring", "animals", "cute", "toddlers"]
            },
            {
                "title": "Dinosaur Coloring Book for Kids",
                "subtitle": "50 Fun Dinosaur Pages for Boys and Girls",
                "ages": "3-8",
                "pages": "50-60",
                "competitor_price": "$5.99",
                "monthly_sales_estimate": "800-3500",
                "keywords": ["dinosaurs", "coloring", "boys", "kids"]
            },
            {
                "title": "Princess Coloring Book",
                "subtitle": "Fairy Tales, Castles, and Magic for Little Girls",
                "ages": "3-7",
                "pages": "50-60",
                "competitor_price": "$5.99",
                "monthly_sales_estimate": "600-2500",
                "keywords": ["princess", "coloring", "girls", "fairy tales"]
            },
            {
                "title": "Space Coloring Book",
                "subtitle": "Rockets, Planets, and Astronauts",
                "ages": "4-8",
                "pages": "50-60",
                "competitor_price": "$5.99",
                "monthly_sales_estimate": "400-1800",
                "keywords": ["space", "rockets", "planets", "astronauts"]
            },
            {
                "title": "Construction Vehicles Coloring Book",
                "subtitle": "Trucks, Excavators, and Bulldozers for Kids",
                "ages": "2-6",
                "pages": "50-60",
                "competitor_price": "$5.99",
                "monthly_sales_estimate": "500-2000",
                "keywords": ["trucks", "construction", "vehicles", "boys"]
            }
        ]
    },
    
    "journals_and_trackers": {
        "category": "Journals & Trackers",
        "market_size": "Growing - mindfulness and routine building",
        "price_range": "$7.99 - $14.99",
        "target_audience": "Parents wanting to build habits",
        "books": [
            {
                "title": "My Daily Routine Chart",
                "subtitle": "A Visual Schedule for Kids: Morning, School, and Bedtime",
                "ages": "3-8",
                "pages": "30-40",
                "competitor_price": "$8.99",
                "monthly_sales_estimate": "200-800",
                "keywords": ["routine", "schedule", "visual chart", "autism", "adhd"]
            },
            {
                "title": "Reading Log for Kids",
                "subtitle": "Track Books, Rate Stories, and Draw Your Favorites!",
                "ages": "5-10",
                "pages": "80-100",
                "competitor_price": "$7.99",
                "monthly_sales_estimate": "150-600",
                "keywords": ["reading log", "book tracker", "reading tracker"]
            },
            {
                "title": "Reward Chart for Good Behavior",
                "subtitle": "Stickers and Stars: Positive Reinforcement System",
                "ages": "3-8",
                "pages": "30-40",
                "competitor_price": "$7.99",
                "monthly_sales_estimate": "300-1200",
                "keywords": ["reward chart", "behavior chart", "positive reinforcement"]
            },
            {
                "title": "Gratitude Journal for Kids",
                "subtitle": "Daily Prompts to Build Thankfulness and Positivity",
                "ages": "6-12",
                "pages": "100-120",
                "competitor_price": "$9.99",
                "monthly_sales_estimate": "100-500",
                "keywords": ["gratitude", "journal", "mindfulness", "positive"]
            }
        ]
    },
    
    "storybooks_with_purpose": {
        "category": "Storybooks with Life Lessons",
        "market_size": "Large - parents buy books with values",
        "price_range": "$8.99 - $12.99",
        "target_audience": "Parents seeking meaningful stories",
        "books": [
            {
                "title": "I Can Handle My Big Feelings",
                "subtitle": "A Book About Managing Emotions for Kids",
                "ages": "3-7",
                "pages": "24-32",
                "competitor_price": "$10.99",
                "monthly_sales_estimate": "200-1000",
                "keywords": ["emotions", "feelings", "social emotional learning", "SEL"]
            },
            {
                "title": "Everyone Is Special",
                "subtitle": "A Story About Diversity, Inclusion, and Being Yourself",
                "ages": "3-7",
                "pages": "24-32",
                "competitor_price": "$10.99",
                "monthly_sales_estimate": "150-800",
                "keywords": ["diversity", "inclusion", "acceptance", "self esteem"]
            },
            {
                "title": "When Grandma/Grandpa Got Sick",
                "subtitle": "Explaining Illness and Loss to Young Children",
                "ages": "4-8",
                "pages": "28-36",
                "competitor_price": "$11.99",
                "monthly_sales_estimate": "100-500",
                "keywords": ["grief", "loss", "illness", "difficult conversations"]
            },
            {
                "title": "My New Baby Brother/Sister",
                "subtitle": "A Book for Soon-to-Be Big Brothers and Sisters",
                "ages": "2-6",
                "pages": "24-32",
                "competitor_price": "$10.99",
                "monthly_sales_estimate": "200-900",
                "keywords": ["new baby", "sibling", "big brother", "big sister"]
            },
            {
                "title": "I Can Use the Potty!",
                "subtitle": "A Positive Potty Training Story",
                "ages": "2-4",
                "pages": "20-28",
                "competitor_price": "$9.99",
                "monthly_sales_estimate": "400-1800",
                "keywords": ["potty training", "toilet training", "bathroom"]
            }
        ]
    }
}

def print_bestseller_report():
    """Print comprehensive bestseller report"""
    
    print("="*80)
    print("  KDP BESTSELLER BOOK IDEAS - MARKET RESEARCH REPORT")
    print("="*80)
    print()
    
    total_books = sum(len(cat["books"]) for cat in BESTSELLER_IDEAS.values())
    print(f"Total Book Ideas: {total_books}")
    print(f"Categories: {len(BESTSELLER_IDEAS)}")
    print()
    
    for category_key, category_data in BESTSELLER_IDEAS.items():
        print("="*80)
        print(f"📚 {category_data['category'].upper()}")
        print("="*80)
        print(f"Market Size: {category_data['market_size']}")
        print(f"Price Range: {category_data['price_range']}")
        print(f"Target: {category_data['target_audience']}")
        print()
        
        for i, book in enumerate(category_data['books'], 1):
            print(f"  {i}. {book['title']}")
            print(f"     Subtitle: {book['subtitle']}")
            print(f"     Ages: {book['ages']} | Pages: {book['pages']}")
            print(f"     Competitor Price: {book['competitor_price']}")
            print(f"     Est. Monthly Sales: {book['monthly_sales_estimate']} units")
            print(f"     Keywords: {', '.join(book['keywords'])}")
            print()
    
    print("="*80)
    print("STRATEGY RECOMMENDATIONS")
    print("="*80)
    print()
    print("🎯 START WITH:")
    print("   1. My First Learn-to-Write Workbook (HUGE demand)")
    print("   2. Cute Animals Coloring Book (Easy to create)")
    print("   3. I Spy Everything! (Proven bestseller format)")
    print()
    print("📈 SCALE TO:")
    print("   4. Sight Words Practice Book (Education niche)")
    print("   5. My Big Kindergarten Workbook (Higher price point)")
    print("   6. Dinosaur Coloring Book (Popular theme)")
    print()
    print("💰 PREMIUM OPPORTUNITIES:")
    print("   7. Bilingual Spanish/English books")
    print("   8. Special needs / Autism-friendly books")
    print("   9. Holiday-themed seasonal books")
    print("  10. Personalized name books (higher margin)")
    print()
    print("="*80)

if __name__ == "__main__":
    print_bestseller_report()
