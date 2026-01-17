import snscrape.modules.twitter as sntwitter
import instaloader


def extract_from_twitter(username: str, max_posts: int = 20):
    # sanitize
    username = username.strip().replace("@", "").replace(" ", "")

    tweets = []

    try:
        query = f"from:{username}"
        scraper = sntwitter.TwitterSearchScraper(query)

        for i, tweet in enumerate(scraper.get_items()):
            if i >= max_posts:
                break
            tweets.append(tweet.content)

        if not tweets:
            raise RuntimeError("No tweets fetched")

    except Exception:
        # 🔁 graceful fallback
        return {
            "bio": "",
            "posts": [],
            "warning": "Twitter scraping blocked or username invalid"
        }

    return {
        "bio": "",
        "posts": tweets
    }


def extract_from_instagram(username: str, max_posts: int = 10):
    """
    Fetch public Instagram bio & captions using instaloader
    """
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        quiet=True
    )

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
    except Exception as e:
        raise RuntimeError(f"Instagram profile not accessible: {e}")

    posts = []
    for i, post in enumerate(profile.get_posts()):
        if i >= max_posts:
            break
        if post.caption:
            posts.append(post.caption)

    return {
        "bio": profile.biography or "",
        "posts": posts
    }