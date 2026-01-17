import urllib.parse

def analyze_profile(profile_text: str):
    text = profile_text.lower()

    interests = []

    if "fitness" in text or "gym" in text:
        interests.append("fitness accessories")
    if "travel" in text:
        interests.append("travel gadgets")
    if "coffee" in text:
        interests.append("coffee gifts")
    if "coding" in text or "developer" in text:
        interests.append("programming desk accessories")
    if "music" in text:
        interests.append("music merchandise")

    if not interests:
        interests.append("unique personalized gifts")

    return interests


def generate_gift_links(interests):
    gifts = []

    for interest in interests[:5]:
        query = urllib.parse.quote_plus(interest)

        gifts.append({
            "interest": interest,
            "amazon": f"https://www.amazon.in/s?k={query}",
            "etsy": f"https://www.etsy.com/search?q={query}"
        })

    return gifts