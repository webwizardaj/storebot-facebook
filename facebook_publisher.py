
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_VERSION = os.getenv("META_GRAPH_VERSION", "v26.0")
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"


def publish_facebook_photo(image_url: str, caption: str) -> dict:
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    page_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

    if not page_id or not page_token:
        raise ValueError("Set Facebook credentials in your .env file")

    if not image_url.startswith("https://"):
        raise ValueError("Image URL must use HTTPS")

    response = requests.post(
        f"{GRAPH_BASE_URL}/{page_id}/photos",
        data={
            "url": image_url,
            "caption": caption,
            "access_token": page_token,
        },
        timeout=60,
    )

    result = response.json()

    if not response.ok or "error" in result:
        error = result.get("error", {})
        message = error.get("message", "Unknown Facebook API error")
        raise RuntimeError(f"Facebook publishing failed: {message}")

    return {
        "success": True,
        "photo_id": result.get("id"),
        "post_id": result.get("post_id"),
    }
