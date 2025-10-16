from PIL import Image
import os


def convert_to_webp(input_path, filename, quality=80):
    """
    Converts an image to WebP format with specified quality.

    Args:
        input_path (str): Path to the input image file (e.g., .jpg, .png).
        filename (str): Path to save the output WebP file.
        quality (int): Compression quality (0-100, higher means less compression).
    """
    try:
        img = Image.open(input_path)
        # Convert to RGB if the image has an alpha channel (e.g., PNG)
        # as some older WebP encoders might not handle RGBA directly.
        if img.mode == "RGBA":
            img = img.convert("RGB")
        img.save(os.path.join("app/static/images/artikel",filename), "webp", quality=quality)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
