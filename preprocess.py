import re

def preprocess_input(text):
    if not text:
        return ""
    # Strip whitespace
    text = text.strip()
    # Remove special characters (keep punctuation for context)
    text = re.sub(r'[^a-zA-Z0-9\s.,;:!?()-]', '', text)
    # Fix spacing
    text = re.sub(r'\s+', ' ', text)
    return text
