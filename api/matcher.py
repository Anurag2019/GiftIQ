import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "products.json")


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_interests(text: str, interest_map: dict):
    text = text.lower()
    detected = set()

    for interest, keywords in interest_map.items():
        if any(word in text for word in keywords):
            detected.add(interest)

    return list(detected)


def match_products(interests: list, products: list):
    matched = []
    for product in products:
        if product["category"].lower() in interests:
            matched.append(product)
    return matched