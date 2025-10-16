import re

def slugify(text):
    text = text.lower().strip()  # Convert to lowercase and remove leading/trailing whitespace
    text = re.sub(r'[^\w\s-]', '', text)  # Remove non-alphanumeric characters (except spaces and hyphens)
    text = re.sub(r'[\s_-]+', '-', text)  # Replace spaces, underscores, and multiple hyphens with a single hyphen
    text = re.sub(r'^-+|-+$', '', text)  # Remove leading/trailing hyphens
    return text