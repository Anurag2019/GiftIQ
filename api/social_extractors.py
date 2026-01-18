import snscrape.modules.twitter as sntwitter
import instaloader


def extract_from_twitter(username: str, max_posts: int = 20):
    """
    Fetch public Twitter/X bio & posts using snscrape
    Returns status object with success/failure indicators
    """
    # Sanitize username
    username = username.strip().replace("@", "").replace(" ", "")

    tweets = []

    try:
        query = f"from:{username}"
        scraper = sntwitter.TwitterSearchScraper(query)

        for i, tweet in enumerate(scraper.get_items()):
            if i >= max_posts:
                break
            tweets.append(tweet.content)

        # Check if any tweets were fetched
        if not tweets:
            return {
                "success": False,
                "bio": "",
                "posts": [],
                "error": f"No posts found for Twitter handle '@{username}'. Please check the username or try a different source.",
                "error_type": "no_posts_found"
            }

    except Exception as e:
        # Handle scraping errors (account not found, blocked, etc.)
        return {
            "success": False,
            "bio": "",
            "posts": [],
            "error": f"Unable to access Twitter handle '@{username}'. The account may not exist or Twitter scraping is blocked.",
            "error_type": "access_error"
        }

    return {
        "success": True,
        "bio": "",
        "posts": tweets
    }


def extract_from_instagram(username: str, max_posts: int = 10):
    """
    Fetch public Instagram bio & captions using instaloader
    Checks if account exists and is public before proceeding
    Returns status object with success/failure indicators
    """
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        quiet=True
    )

    # Sanitize username
    username = username.strip().replace("@", "").replace(" ", "")

    try:
        # Try to fetch the profile
        profile = instaloader.Profile.from_username(loader.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        return {
            "success": False,
            "bio": "",
            "posts": [],
            "error": f"Instagram profile '{username}' does not exist. Please check the username and try again.",
            "error_type": "profile_not_found"
        }
    except Exception as e:
        return {
            "success": False,
            "bio": "",
            "posts": [],
            "error": f"Error accessing Instagram profile: {str(e)}",
            "error_type": "access_error"
        }

    # Check if the account is private
    if profile.is_private:
        return {
            "success": False,
            "bio": "",
            "posts": [],
            "error": f"Instagram account '@{username}' is private. We can only analyze public profiles. Please provide manual bio text instead.",
            "error_type": "private_account"
        }

    # Proceed with extraction for public accounts
    posts = []
    try:
        for i, post in enumerate(profile.get_posts()):
            if i >= max_posts:
                break
            if post.caption:
                posts.append(post.caption)
    except Exception as e:
        # If we can't get posts, still return the bio at least
        pass

    return {
        "success": True,
        "bio": profile.biography or "",
        "posts": posts
    }