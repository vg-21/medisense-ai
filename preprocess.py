import re

def clean_input(text: str) -> str:
    """
    Basic preprocessing for user input.
    """
    if not text:
        return ""
    # Lowercase the text
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-z0-9\s.,;:!?\-]', '', text)
    # Fix spacing
    text = re.sub(r'\s+', ' ', text)
    # Strip unnecessary whitespace
    return text.strip()

def format_output(text: str) -> str:
    """
    Basic formatting for the model output.
    """
    if not text:
        return ""
    return text.strip()
