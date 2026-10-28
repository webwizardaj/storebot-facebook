
from cloudinary_images import get_cloudinary_images
from facebook_publisher import publish_facebook_photo


def main():
    images = get_cloudinary_images(max_results=20)

    if not images:
        print("No images found in Cloudinary.")
        return

    print("\nImages available in Cloudinary:\n")
    for index, image in enumerate(images, start=1):
        print(f"{index}. {image['public_id']} ({image.get('format', 'unknown')})")

    try:
        choice = int(input("\nEnter the image number to publish: "))
        if not 1 <= choice <= len(images):
            print("Invalid image number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    caption = input("Enter the Facebook post caption: ").strip()
    selected_image = images[choice - 1]

    confirm = input(
        f"\nPublish '{selected_image['public_id']}' to Facebook? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("Cancelled. Nothing was published.")
        return

    result = publish_facebook_photo(
        image_url=selected_image["url"],
        caption=caption,
    )

    print("\nFacebook publishing succeeded!")
    print("Selected image:", selected_image["public_id"])
    print("Result:", result)


if __name__ == "__main__":
    main()
