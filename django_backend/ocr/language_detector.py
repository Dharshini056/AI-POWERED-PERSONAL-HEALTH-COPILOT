import re

def detect_language(text: str) -> str:
    """
    Detect language based on Unicode block analysis.
    Supports English, Tamil, Hindi, Telugu, Malayalam, Kannada, and Bilingual combos.
    """
    if not text or not text.strip():
        return "English"

    tamil_count = len(re.findall(r'[\u0B80-\u0BFF]', text))
    hindi_count = len(re.findall(r'[\u0900-\u097F]', text))
    telugu_count = len(re.findall(r'[\u0C00-\u0C7F]', text))
    malayalam_count = len(re.findall(r'[\u0D00-\u0D7F]', text))
    kannada_count = len(re.findall(r'[\u0C80-\u0CFF]', text))
    english_count = len(re.findall(r'[a-zA-Z]', text))

    # Check for bilingual Tamil + English
    if tamil_count > 10 and english_count > 15:
        return "Bilingual (English + Tamil)"
    elif tamil_count > 10:
        return "Tamil"
    elif hindi_count > 10:
        return "Hindi"
    elif telugu_count > 10:
        return "Telugu"
    elif malayalam_count > 10:
        return "Malayalam"
    elif kannada_count > 10:
        return "Kannada"
    elif english_count > 0:
        return "English"
    else:
        return "English"
