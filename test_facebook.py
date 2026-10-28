
from facebook_publisher import publish_facebook_photo

# This is a publicly accessible sample image for testing.
image_url = "https://picsum.photos/1200/800"
caption = "StoreBot Facebook integration test. #StoreBot"

try:
    result = publish_facebook_photo(image_url, caption)
    print("Facebook publishing succeeded!")
    print("Result:", result)
except Exception as exc:
    print("Facebook publishing failed.")
    print(type(exc).__name__ + ":", exc)
