import requests
import random
import string
import os
def download_from_url(url: str):
    try:
        response = requests.get(url, stream=True)  # Use stream=True for large files
        response.raise_for_status()  # Raise an exception for bad status codes
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choice(characters) for _ in range(15))
        filename = random_string.upper() + ".webp"
        with open(os.path.join("app/static/images/artikel",filename), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                f.write(chunk)
        return filename,True

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
