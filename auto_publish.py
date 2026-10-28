
from cloudinary_images import (
    get_cloudinary_images,
    mark_image_published,
    PUBLISHED_TAG,
)
from gemini_caption import generate_caption
from facebook_publisher import publish_facebook_photo


def main():
    images = get_cloudinary_images(max_results=100)

    # Select the newest image that has not been published.
    image = next(
        (
            item
            for item in images
            if PUBLISHED_TAG not in item.get("tags", [])
        ),
        None,
    )

    if image is None:
        raise RuntimeError(
            "No unpublished images found among the latest "
            "100 Cloudinary images."
        )

    public_id = image["public_id"]
    product_name = public_id.split("/")[-1].replace("_", " ")

    print(f"Selected image: {public_id}")
    print("Generating caption with Gemini...")

    caption = generate_caption(
        image_url=image["url"],
        product_name=product_name,
    )

    print(f"Generated caption: {caption}")
    print("Publishing to Facebook...")

    result = publish_facebook_photo(
        image_url=image["url"],
        caption=caption,
    )

    if not result or not result.get("success"):
        raise RuntimeError("Facebook publishing did not succeed.")

    print("Facebook publishing succeeded!")

    # Record the image only after Facebook confirms success.
    try:
        mark_image_published(public_id)
        print(f"Marked {public_id} as published in Cloudinary.")
    except Exception:
        # Facebook may already have published the image.
        # Do not pretend the duplicate protection was saved.
        print(
            "WARNING: Facebook published successfully, but "
            "Cloudinary could not record the published tag. "
            "This image may be selected again."
        )

    return {
        "success": True,
        "public_id": public_id,
        "caption": caption,
        "facebook_post_id": result.get("post_id"),
        "facebook_photo_id": result.get("photo_id"),
        "duplicate_protection_saved": True,
    }


if __name__ == "__main__":
    main()
