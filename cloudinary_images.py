
import os

import cloudinary
import cloudinary.api
from dotenv import load_dotenv

load_dotenv(override=True)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

PUBLISHED_TAG = "facebook_published"


def get_cloudinary_images(max_results=100):
    result = cloudinary.api.resources(
        resource_type="image",
        type="upload",
        max_results=max_results,
        direction="desc",
        tags=True,
    )

    return [
        {
            "public_id": image["public_id"],
            "url": image["secure_url"],
            "format": image.get("format"),
            "tags": image.get("tags", []),
        }
        for image in result.get("resources", [])
        if image.get("secure_url")
    ]


def mark_image_published(public_id):
    cloudinary.api.add_tag(
        PUBLISHED_TAG,
        [public_id],
    )


if __name__ == "__main__":
    images = get_cloudinary_images()

    if not images:
        print("No uploaded images found.")
    else:
        for image in images:
            status = (
                "ALREADY PUBLISHED"
                if PUBLISHED_TAG in image["tags"]
                else "Not published yet"
            )
            print(f"{image['public_id']}: {status}")
