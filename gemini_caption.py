
import os
import time
from io import BytesIO

import requests
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.6-flash"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


def generate_caption(image_url: str, product_name: str) -> str:
    """Generate a Facebook marketing caption using Gemini."""

    response = requests.get(image_url, timeout=30)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content)).convert("RGB")
    image.thumbnail((1024, 1024))

    prompt = f"""
    You are a professional social media marketer for an online store.

    Product name: {product_name}

    Analyze the image and write one engaging Facebook caption.
    Keep it concise and natural. Include a call to action and up to
    three relevant hashtags. Do not invent prices, discounts, or
    product features. Return only the caption.
    """

    for attempt in range(3):
        try:
            result = client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt, image],
            )

            caption = (result.text or "").strip()
            if not caption:
                raise RuntimeError("Gemini returned an empty caption.")

            return caption

        except errors.APIError as exc:
            # Retry only temporary server errors.
            if exc.code not in (429, 500, 502, 503, 504):
                raise RuntimeError(
                    f"Gemini API error {exc.code}: {exc.message}"
                ) from exc

            if attempt == 2:
                raise RuntimeError(
                    f"Gemini remained unavailable after 3 attempts: "
                    f"{exc.message}"
                ) from exc

            wait_seconds = 2 ** (attempt + 1)
            print(
                f"Gemini returned error {exc.code}. "
                f"Retrying in {wait_seconds} seconds..."
            )
            time.sleep(wait_seconds)

    raise RuntimeError("Caption generation failed.")


if __name__ == "__main__":
    url = input("Paste Cloudinary image URL: ").strip()
    name = input("Enter product name: ").strip()

    try:
        print("\nGenerating caption...\n")
        print(generate_caption(url, name))
    except Exception as exc:
        print(f"\nError: {exc}")
