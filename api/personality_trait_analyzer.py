import re

import spacy



def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)        # remove URLs
    text = re.sub(r"@\w+", "", text)           # remove mentions
    text = re.sub(r"#\w+", "", text)           # remove hashtags
    # Keep apostrophes and hyphens for contractions and hyphenated words
    text = re.sub(r"[^a-zA-Z\s\-']", "", text)    # remove emojis & symbols but keep apostrophes and hyphens
    text = re.sub(r"\s+", " ", text).strip()
    return text


nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str):
    doc = nlp(text)
    keywords = set()

    for token in doc:
        # Include NOUN, PROPN, ADJ (adjectives) and VERB (verbs for better trait detection)
        if token.pos_ in ["NOUN", "PROPN", "ADJ", "VERB"] and not token.is_stop and len(token.text) > 2:
            keywords.add(token.lemma_)
    
    # Also add some multi-word patterns that might be important
    text_lower = text.lower()
    multi_word_patterns = [
        r"indie movie", r"sustainable fashion", r"tech company", r"adventure travel",
        r"adventure", r"hiking", r"photography", r"fashion", r"travel", r"tech",
        r"practical gift", r"minimalist", r"promoted", r"birthday", r"friend"
    ]
    for pattern in multi_word_patterns:
        if re.search(pattern, text_lower):
            keywords.add(pattern.replace(" ", "_"))

    return list(keywords)
TRAIT_MAP = {
    "creative": ["design", "art", "writing", "photography", "music", "dance", "paint", "creative", "designer"],
    "analytical": ["ai", "data", "engineering", "research", "science", "math", "technical", "programmer"],
    "adventurous": ["travel", "explore", "hiking", "roadtrip", "adventure", "climbing", "adventure_travel", "wanderlust"],
    "minimalist": ["simple", "clean", "minimal", "organized", "minimalist", "practical", "practical_gift"],
    "fitness_focused": ["gym", "workout", "yoga", "health", "run", "sport", "fitness", "athletic"],
    "entrepreneurial": ["startup", "business", "founder", "leader", "entrepreneur", "promoted"],
    "bookworm": ["book", "reading", "novel", "author", "literature", "reader"],
    "musician": ["music", "guitar", "piano", "instrument", "song", "melody", "musician"],
    "foodie": ["food", "cook", "chef", "cuisine", "recipe", "restaurant", "cooking", "culinary"],
    "fashionista": ["fashion", "style", "trend", "outfit", "designer", "clothes", "sustainable_fashion", "aesthetic"],
    "dancer": ["dance", "choreography", "movement", "ballet", "hip hop", "dancer"],
    "nature_lover": ["nature", "garden", "plant", "outdoor", "environment", "hiking", "sustainable"],
    "gamer": ["gaming", "game", "esports", "online", "console", "gamer"],
    "tech_enthusiast": ["tech", "tech_company", "technology", "software", "coding"]
}

def infer_personality_traits(keywords):
    traits = set()
    
    # Normalize keywords for matching (lowercase)
    keywords_lower = [k.lower() for k in keywords]

    for trait, signals in TRAIT_MAP.items():
        # Check for direct matches and partial matches
        if any(word.lower() in keywords_lower or any(word.lower() in k for k in keywords_lower) for word in signals):
            traits.add(trait)

    return list(traits)

INTEREST_CATEGORY_MAP = {
    "travel": ["travel", "trip", "wander", "vacation", "beach", "mountain", "explore", "adventure", "adventure_travel", "wanderlust", "journey"],
    "fitness": ["gym", "fitness", "workout", "yoga", "run", "sport", "health", "athletic", "exercise"],
    "tech": ["ai", "coding", "python", "startup", "tech", "software", "gadget", "technology", "tech_company", "programmer"],
    "fashion": ["fashion", "style", "outfit", "aesthetic", "designer", "trend", "sustainable_fashion", "clothes"],
    "gaming": ["gaming", "ps5", "xbox", "esports", "online", "console", "game"],
    "books": ["books", "reading", "novel", "author", "literature", "library", "book"],
    "coffee": ["coffee", "cafe", "espresso", "latte", "brew", "beverage"],
    "music": ["music", "song", "guitar", "piano", "instrument", "concert", "musician", "melody"],
    "dance": ["dance", "choreography", "ballet", "hip hop", "movement", "dancer"],
    "food": ["food", "cook", "chef", "cuisine", "recipe", "restaurant", "culinary", "cooking", "gourmet"],
    "art": ["art", "paint", "draw", "creative", "design", "illustration", "artist"],
    "nature": ["nature", "garden", "plant", "outdoor", "hiking", "environment", "sustainable", "outdoors"],
    "photography": ["photo", "photography", "camera", "picture", "visual", "photographer"],
    "movies": ["movie", "film", "cinema", "watch", "series", "netflix", "indie movie"],
    "wellness": ["meditation", "mindfulness", "wellness", "self care", "relax", "relaxation", "mindful"]
}

def classify_interests(keywords):
    categories = set()
    
    # Normalize keywords for matching (lowercase)
    keywords_lower = [k.lower() for k in keywords]

    for category, signals in INTEREST_CATEGORY_MAP.items():
        # Check for direct matches and partial matches
        if any(word.lower() in keywords_lower or any(word.lower() in k for k in keywords_lower) for word in signals):
            categories.add(category)

    return list(categories)

GIFT_MAP = [
    # tech
    {
        "title": "Smart Desk Organizer",
        "category": "tech",
        "price": 2499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71zF5xgkfKL._SX679_.jpg",
        "link": "https://amazon.in/s?k=smart+desk+organizer",
        "tags": ["desk", "office", "gadgets"]
    },
    {
        "title": "Wireless Charging Pad",
        "category": "tech",
        "price": 1999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71XgGR-CWQL._SX679_.jpg",
        "link": "https://amazon.in/s?k=wireless+charging+pad",
        "tags": ["mobile", "wireless", "accessories"]
    },
    {
        "title": "Ergonomic Laptop Stand",
        "category": "tech",
        "price": 1499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71Ci6FY7T4L._SX679_.jpg",
        "link": "https://amazon.in/s?k=ergonomic+laptop+stand",
        "tags": ["work from home", "posture", "office"]
    },
    {
        "title": "Wireless Gaming Mouse",
        "category": "tech",
        "price": 1999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/61y1zTEhS0L._SX679_.jpg",
        "link": "https://amazon.in/s?k=wireless+gaming+mouse",
        "tags": ["gaming", "pc", "accessories"]
    },

    # Productivity
    {
        "title": "Minimalist Planner",
        "category": "productivity",
        "price": 999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71i7TyPkI2L._SX679_.jpg",
        "link": "https://amazon.in/s?k=minimalist+planner+notebook",
        "tags": ["planning", "goals", "daily routine"]
    },
    {
        "title": "Focus Timer Cube",
        "category": "productivity",
        "price": 1299,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/61Eu7iVlPHL._SX679_.jpg",
        "link": "https://amazon.in/s?k=pomodoro+timer+cube",
        "tags": ["pomodoro", "deep work", "time management"]
    },
    {
        "title": "Noise Blocking Earplugs",
        "category": "productivity",
        "price": 799,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71VLHR-UXBL._SX679_.jpg",
        "link": "https://amazon.in/s?k=noise+blocking+earplugs",
        "tags": ["focus", "study", "sleep"]
    },

    # Travel
    {
        "title": "Travel Organizer Kit",
        "category": "travel",
        "price": 1499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71uN0f5bBDL._SX679_.jpg",
        "link": "https://amazon.in/s?k=travel+organizer+kit",
        "tags": ["bags", "packing", "accessories"]
    },
    {
        "title": "Scratch World Map",
        "category": "travel",
        "price": 2199,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71DwKpT8EQL._SX679_.jpg",
        "link": "https://amazon.in/s?k=scratch+world+map",
        "tags": ["travel memories", "wall decor"]
    },
    {
        "title": "Compact Travel Backpack",
        "category": "travel",
        "price": 2499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71pL1a3CnGL._SX679_.jpg",
        "link": "https://amazon.in/s?k=compact+travel+backpack",
        "tags": ["backpack", "weekend trips", "carry-on"]
    },
    {
        "title": "Portable Neck Pillow",
        "category": "travel",
        "price": 899,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/61R2SfqKcgL._SX679_.jpg",
        "link": "https://amazon.in/s?k=portable+neck+pillow",
        "tags": ["comfort", "flights", "long journeys"]
    },
    {
        "title": "Compact Camera Drone",
        "category": "travel",
        "price": 4999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71eTjP0ZVPL._SX679_.jpg",
        "link": "https://amazon.in/s?k=compact+camera+drone",
        "tags": ["drone", "camera", "travel", "photography"]
    },
    {
        "title": "Travel Camera Phone Lens",
        "category": "travel",
        "price": 1999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71qK5N9RWZL._SX679_.jpg",
        "link": "https://amazon.in/s?k=phone+camera+lens+travel",
        "tags": ["lens", "phone", "camera", "portable"]
    },
    {
        "title": "Waterproof Action Camera",
        "category": "travel",
        "price": 8999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71WIpPQkq4L._SX679_.jpg",
        "link": "https://amazon.in/s?k=waterproof+action+camera",
        "tags": ["camera", "waterproof", "action", "adventure"]
    },
    {
        "title": "Camera Cleaning Kit Travel",
        "category": "travel",
        "price": 599,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71vCjJ3O9IL._SX679_.jpg",
        "link": "https://amazon.in/s?k=camera+cleaning+kit",
        "tags": ["cleaning", "camera", "maintenance"]
    },
    {
        "title": "Portable Camera Stabilizer",
        "category": "travel",
        "price": 2999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71cXhQXXZIL._SX679_.jpg",
        "link": "https://amazon.in/s?k=portable+camera+stabilizer+gimbal",
        "tags": ["stabilizer", "gimbal", "video", "travel"]
    },

    # Fitness
    {
        "title": "Resistance Band Set",
        "category": "fitness",
        "price": 899,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/81A-sL8tSFL._SX679_.jpg",
        "link": "https://amazon.in/s?k=resistance+band+set",
        "tags": ["home workout", "exercise"]
    },
    {
        "title": "Smart Water Bottle",
        "category": "fitness",
        "price": 1799,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71a5T8D2UrL._SX679_.jpg",
        "link": "https://amazon.in/s?k=smart+water+bottle",
        "tags": ["hydration", "health", "smart"]
    },
    {
        "title": "Yoga Mat Pro",
        "category": "fitness",
        "price": 1299,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71z9iYZNMfL._SX679_.jpg",
        "link": "https://amazon.in/s?k=yoga+mat+pro",
        "tags": ["yoga", "meditation", "stretching"]
    },

    # Lifestyle / Food
    {
        "title": "Premium Coffee Sampler",
        "category": "food",
        "price": 999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71VGcAo1CaL._SX679_.jpg",
        "link": "https://amazon.in/s?k=premium+coffee+sampler",
        "tags": ["coffee", "gourmet", "beverages"]
    },
    {
        "title": "Aromatherapy Candle Set",
        "category": "wellness",
        "price": 1199,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71LqfDCKd7L._SX679_.jpg",
        "link": "https://amazon.in/s?k=aromatherapy+candle+set",
        "tags": ["relaxation", "home decor"]
    },

    # Books
    {
        "title": "Bestselling Fiction Bundle",
        "category": "books",
        "price": 1499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71aY08t8RwL._SX679_.jpg",
        "link": "https://amazon.in/s?k=bestselling+fiction+books",
        "tags": ["books", "fiction", "reading"]
    },
    {
        "title": "Personalized Book Holder",
        "category": "books",
        "price": 899,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71SBXd7FyxL._SX679_.jpg",
        "link": "https://amazon.in/s?k=book+holder+stand",
        "tags": ["books", "organizer", "library"]
    },
    {
        "title": "Premium Reading Light",
        "category": "books",
        "price": 1299,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71TLvqQZkHL._SX679_.jpg",
        "link": "https://amazon.in/s?k=reading+light+led",
        "tags": ["reading", "led", "desk lamp"]
    },
    {
        "title": "Literary Tote Bag",
        "category": "books",
        "price": 599,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71P8K6pT5kL._SX679_.jpg",
        "link": "https://amazon.in/s?k=book+tote+bag",
        "tags": ["books", "tote", "bag"]
    },

    # Music
    {
        "title": "Wireless Bluetooth Speaker",
        "category": "music",
        "price": 2499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/61c-l9dVaIL._SX679_.jpg",
        "link": "https://amazon.in/s?k=wireless+bluetooth+speaker",
        "tags": ["music", "speaker", "audio"]
    },
    {
        "title": "Professional Studio Headphones",
        "category": "music",
        "price": 4999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71dEGGHCmrL._SX679_.jpg",
        "link": "https://amazon.in/s?k=professional+studio+headphones",
        "tags": ["headphones", "audio", "music"]
    },
    {
        "title": "Acoustic Guitar Accessory Kit",
        "category": "music",
        "price": 1599,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71E14FHcRzL._SX679_.jpg",
        "link": "https://amazon.in/s?k=guitar+accessory+kit",
        "tags": ["guitar", "instrument", "music"]
    },
    {
        "title": "Vinyl Record Holder Stand",
        "category": "music",
        "price": 1799,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71qnUHW7GaL._SX679_.jpg",
        "link": "https://amazon.in/s?k=vinyl+record+holder",
        "tags": ["vinyl", "music", "decor"]
    },

    # Dance
    {
        "title": "Professional Dance Mat",
        "category": "dance",
        "price": 2999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/81Lg+gYGw0L._SX679_.jpg",
        "link": "https://amazon.in/s?k=dance+mat+practice",
        "tags": ["dance", "practice", "floor"]
    },
    {
        "title": "Dance Practice Mirror",
        "category": "dance",
        "price": 3499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71HqJoU-BcL._SX679_.jpg",
        "link": "https://amazon.in/s?k=dance+mirror+studio",
        "tags": ["dance", "mirror", "studio"]
    },
    {
        "title": "LED Dance Shoes",
        "category": "dance",
        "price": 1999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71+g-+MpH9L._SX679_.jpg",
        "link": "https://amazon.in/s?k=led+shoes+light+up",
        "tags": ["shoes", "dance", "light up"]
    },
    {
        "title": "Portable Dance Pole",
        "category": "dance",
        "price": 2499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71B1GS1H5lL._SX679_.jpg",
        "link": "https://amazon.in/s?k=dance+pole+portable",
        "tags": ["dance", "pole", "practice"]
    },

    # Food & Cooking
    {
        "title": "Gourmet Spice Collection",
        "category": "food",
        "price": 1599,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71b3TKfJDcL._SX679_.jpg",
        "link": "https://amazon.in/s?k=gourmet+spice+collection",
        "tags": ["spices", "cooking", "gourmet"]
    },
    {
        "title": "Professional Chef Knife Set",
        "category": "food",
        "price": 3499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71X7J3c+QXL._SX679_.jpg",
        "link": "https://amazon.in/s?k=professional+chef+knife+set",
        "tags": ["kitchen", "chef", "knives"]
    },
    {
        "title": "Cast Iron Skillet",
        "category": "food",
        "price": 1999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71SEOlZHOxL._SX679_.jpg",
        "link": "https://amazon.in/s?k=cast+iron+skillet",
        "tags": ["cooking", "kitchen", "cookware"]
    },
    {
        "title": "Digital Kitchen Scale",
        "category": "food",
        "price": 899,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71b-ybT8L5L._SX679_.jpg",
        "link": "https://amazon.in/s?k=digital+kitchen+scale",
        "tags": ["kitchen", "cooking", "baking"]
    },
    {
        "title": "Artisan Chocolate Box",
        "category": "food",
        "price": 1199,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71jBP8RcJxL._SX679_.jpg",
        "link": "https://amazon.in/s?k=artisan+chocolate+gift+box",
        "tags": ["chocolate", "gourmet", "gift"]
    },

    # Fashion
    {
        "title": "Designer Sunglasses",
        "category": "fashion",
        "price": 2999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71n3SPnxBIL._SX679_.jpg",
        "link": "https://amazon.in/s?k=designer+sunglasses",
        "tags": ["fashion", "sunglasses", "accessory"]
    },
    {
        "title": "Premium Leather Wallet",
        "category": "fashion",
        "price": 1899,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71h5PzAmYqL._SX679_.jpg",
        "link": "https://amazon.in/s?k=leather+wallet+premium",
        "tags": ["leather", "wallet", "accessory"]
    },
    {
        "title": "Luxury Silk Scarf",
        "category": "fashion",
        "price": 1599,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71p+c9KNDSL._SX679_.jpg",
        "link": "https://amazon.in/s?k=silk+scarf+luxury",
        "tags": ["silk", "scarf", "fashion"]
    },
    {
        "title": "Fashion Watch",
        "category": "fashion",
        "price": 3999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71eKrNBKbHL._SX679_.jpg",
        "link": "https://amazon.in/s?k=fashion+watch",
        "tags": ["watch", "fashion", "accessory"]
    },
    {
        "title": "Wool Beanie Collection",
        "category": "fashion",
        "price": 799,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71uY9qFbvKL._SX679_.jpg",
        "link": "https://amazon.in/s?k=wool+beanie",
        "tags": ["beanie", "winter", "fashion"]
    },

    # Art
    {
        "title": "Professional Sketch Set",
        "category": "art",
        "price": 1499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71OASC3e9dL._SX679_.jpg",
        "link": "https://amazon.in/s?k=professional+sketch+set",
        "tags": ["art", "sketching", "drawing"]
    },
    {
        "title": "Oil Painting Starter Kit",
        "category": "art",
        "price": 2499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71gUr9PyKKL._SX679_.jpg",
        "link": "https://amazon.in/s?k=oil+painting+starter+kit",
        "tags": ["painting", "art", "creative"]
    },
    {
        "title": "Digital Art Tablet",
        "category": "art",
        "price": 4999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71b-rJD2PmL._SX679_.jpg",
        "link": "https://amazon.in/s?k=digital+art+tablet",
        "tags": ["digital", "tablet", "art"]
    },
    {
        "title": "Artist Canvas Bundle",
        "category": "art",
        "price": 1299,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71dW7d8BPJL._SX679_.jpg",
        "link": "https://amazon.in/s?k=canvas+painting+set",
        "tags": ["canvas", "painting", "art"]
    },

    # Nature
    {
        "title": "Indoor Plant Collection",
        "category": "nature",
        "price": 1799,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71nLMQTVWEL._SX679_.jpg",
        "link": "https://amazon.in/s?k=indoor+plants+collection",
        "tags": ["plants", "indoor", "decor"]
    },
    {
        "title": "Garden Tool Set",
        "category": "nature",
        "price": 1399,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71FhPAW3VPL._SX679_.jpg",
        "link": "https://amazon.in/s?k=garden+tool+set",
        "tags": ["gardening", "tools", "outdoor"]
    },
    {
        "title": "Binoculars for Birdwatching",
        "category": "nature",
        "price": 2999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71wR-t3jkAL._SX679_.jpg",
        "link": "https://amazon.in/s?k=binoculars+birdwatching",
        "tags": ["nature", "birdwatching", "outdoor"]
    },
    {
        "title": "Eco-Friendly Bamboo Set",
        "category": "nature",
        "price": 999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71KsYhHvbgL._SX679_.jpg",
        "link": "https://amazon.in/s?k=eco+friendly+bamboo+set",
        "tags": ["eco", "sustainable", "nature"]
    },
    {
        "title": "Wildlife Camera Trap 4K",
        "category": "nature",
        "price": 3999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71JGQMlDYaL._SX679_.jpg",
        "link": "https://amazon.in/s?k=wildlife+camera+trap+4k",
        "tags": ["camera", "wildlife", "nature", "photography"]
    },
    {
        "title": "Telephoto Camera Lens",
        "category": "nature",
        "price": 5499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71B5dKnYfEL._SX679_.jpg",
        "link": "https://amazon.in/s?k=telephoto+camera+lens",
        "tags": ["lens", "wildlife", "photography", "nature"]
    },

    # Photography
    {
        "title": "DSLR Camera Backpack",
        "category": "photography",
        "price": 2499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71YEqt3WRVL._SX679_.jpg",
        "link": "https://amazon.in/s?k=camera+backpack+dslr",
        "tags": ["camera", "photography", "bag"]
    },
    {
        "title": "Professional Tripod Stand",
        "category": "photography",
        "price": 1999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71eEKaYP5kL._SX679_.jpg",
        "link": "https://amazon.in/s?k=professional+tripod",
        "tags": ["tripod", "photography", "camera"]
    },
    {
        "title": "Ring Light Studio",
        "category": "photography",
        "price": 2499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71l3EXyUL-L._SX679_.jpg",
        "link": "https://amazon.in/s?k=ring+light+studio",
        "tags": ["lighting", "photography", "studio"]
    },
    {
        "title": "Camera Lens Filter Kit",
        "category": "photography",
        "price": 1499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71qlW8+gajL._SX679_.jpg",
        "link": "https://amazon.in/s?k=lens+filter+kit",
        "tags": ["filters", "lens", "photography"]
    },
    {
        "title": "DSLR Camera 24MP",
        "category": "photography",
        "price": 25999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71Hl2hWC-NL._SX679_.jpg",
        "link": "https://amazon.in/s?k=dslr+camera+24mp",
        "tags": ["camera", "dslr", "photography", "professional"]
    },
    {
        "title": "Mirrorless Camera 4K",
        "category": "photography",
        "price": 59999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71iKVnLkHqL._SX679_.jpg",
        "link": "https://amazon.in/s?k=mirrorless+camera+4k",
        "tags": ["camera", "mirrorless", "4k", "video"]
    },
    {
        "title": "Camera Memory Card 128GB",
        "category": "photography",
        "price": 1299,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71LY-+7EQAL._SX679_.jpg",
        "link": "https://amazon.in/s?k=camera+memory+card+128gb",
        "tags": ["memory", "storage", "sd+card"]
    },
    {
        "title": "Professional Camera Bag",
        "category": "photography",
        "price": 3499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71X5Y9P9LHL._SX679_.jpg",
        "link": "https://amazon.in/s?k=professional+camera+bag",
        "tags": ["bag", "camera", "storage"]
    },

    # Movies & Entertainment
    {
        "title": "Premium Streaming Device",
        "category": "movies",
        "price": 3499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71jy8vUNMEL._SX679_.jpg",
        "link": "https://amazon.in/s?k=streaming+device",
        "tags": ["streaming", "movies", "entertainment"]
    },
    {
        "title": "Movie Poster Collection Set",
        "category": "movies",
        "price": 899,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71f1LoMm5+L._SX679_.jpg",
        "link": "https://amazon.in/s?k=movie+posters+collection",
        "tags": ["movies", "poster", "decor"]
    },
    {
        "title": "Home Theater Sound Bar",
        "category": "movies",
        "price": 4999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71HU4ZPCDZL._SX679_.jpg",
        "link": "https://amazon.in/s?k=soundbar+home+theater",
        "tags": ["soundbar", "theater", "audio"]
    },
    {
        "title": "Cinema Snack Popcorn Kit",
        "category": "movies",
        "price": 799,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71gVLqCvbKL._SX679_.jpg",
        "link": "https://amazon.in/s?k=popcorn+maker+kit",
        "tags": ["popcorn", "snacks", "movies"]
    },

    # Wellness
    {
        "title": "Meditation Cushion",
        "category": "wellness",
        "price": 1299,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71D5dYJWYZL._SX679_.jpg",
        "link": "https://amazon.in/s?k=meditation+cushion+zafu",
        "tags": ["meditation", "wellness", "comfort"]
    },
    {
        "title": "Essential Oil Diffuser",
        "category": "wellness",
        "price": 1599,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71RNqFqk2ZL._SX679_.jpg",
        "link": "https://amazon.in/s?k=essential+oil+diffuser",
        "tags": ["wellness", "aromatic", "relax"]
    },
    {
        "title": "Weighted Blanket",
        "category": "wellness",
        "price": 3499,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71a1hLJaFbL._SX679_.jpg",
        "link": "https://amazon.in/s?k=weighted+blanket",
        "tags": ["sleep", "wellness", "comfort"]
    },
    {
        "title": "Jade Roller & Gua Sha Set",
        "category": "wellness",
        "price": 999,
        "currency": "INR",
        "image": "https://m.media-amazon.com/images/I/71-C1nWYxTL._SX679_.jpg",
        "link": "https://amazon.in/s?k=jade+roller+gua+sha",
        "tags": ["skincare", "wellness", "beauty"]
    }
]


def recommend_gifts(categories):
    recommendations = []

    for category in categories:
        matching_gifts = [gift for gift in GIFT_MAP if gift.get("category") == category]
        recommendations.extend(matching_gifts)

    return recommendations[:5]
def run_full_analysis(raw_bio: str):
    clean = clean_text(raw_bio)
    keywords = extract_keywords(clean)
    
    # Add raw text matching as fallback to catch more keywords
    raw_text_lower = raw_bio.lower()
    additional_keywords = set()
    
    # Extract additional single-word keywords from raw text
    for word in raw_bio.lower().split():
        # Clean the word
        cleaned_word = re.sub(r"[^a-zA-Z\-']", "", word)
        if len(cleaned_word) > 2 and cleaned_word not in ['the', 'and', 'for', 'with', 'that', 'this', 'from']:
            additional_keywords.add(cleaned_word)
    
    # Combine keywords
    all_keywords = list(set(keywords) | additional_keywords)
    
    traits = infer_personality_traits(all_keywords)
    interests = classify_interests(all_keywords)
    gifts = recommend_gifts(interests)

    return {
        "traits": traits,
        "interests": interests,
        "gifts": gifts
    }