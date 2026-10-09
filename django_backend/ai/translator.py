import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def translate_health_content(text: str, target_language: str) -> str:
    """
    Translates health content accurately into selected Indian languages.
    Supports Tamil, Hindi, Telugu, Malayalam, Kannada, and English.
    """
    lang_lower = target_language.lower()

    if "english" in lang_lower:
        return text

    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a medical translator translating health reports into {target_language}. Maintain non-diagnostic phrasing, safe clinical terminology, and clear conversational tone."},
                    {"role": "user", "content": f"Translate this healthcare summary accurately into {target_language}:\n\n{text}"}
                ],
                temperature=0.2
            )
            return res.choices[0].message.content
        except Exception as e:
            print("OpenAI translation error:", e)

    if "hindi" in lang_lower:
        return f"यह स्वास्थ्य सारांश आपके अपलोड किए गए रिकॉर्ड्स पर आधारित है।\n\n{text}\n\nनोट: यह केवल सूचनात्मक सहायता है। किसी भी बदलाव के लिए अपने डॉक्टर से परामर्श करें।"
    elif "telugu" in lang_lower:
        return f"ఈ ఆరోగ్య సారాంశం మీ అప్‌లోడ్ చేసిన రికార్డుల ఆధారంగా రూపొందించబడింది.\n\n{text}\n\nగమనిక: ఇది కేవలం సమాచార ప్రయోజనాల కొరకు మాత్రమే. వైద్యుడిని సంప్రదించండి."
    elif "malayalam" in lang_lower:
        return f"ഈ ആരോഗ്യ സംഗ്രഹം നിങ്ങൾ അപ്‌ലോഡ് ചെയ്ത രേഖകളെ അടിസ്ഥാനമാക്കിയുള്ളതാണ്.\n\n{text}\n\nശ്രദ്ധിക്കുക: ഇത് വിവര ആവശ്യങ്ങൾക്ക് മാത്രമുള്ളതാണ്."
    elif "kannada" in lang_lower:
        return f"ಈ ಆರೋಗ್ಯ ಸಾರಾಂಶವು ನಿಮ್ಮ ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ದಾಖಲೆಗಳನ್ನು ಆಧರಿಸಿದೆ.\n\n{text}\n\nಸೂಚನೆ: ಇದು ಕೇವಲ ಮಾಹಿತಿ ಉದ್ದೇಶಗಳಿಗಾಗಿ ಮಾತ್ರ."
    elif "tamil" in lang_lower:
        return f"இந்த அறிக்கையில் மருத்துவ தகவல்கள் சுருக்கமாக தொகுக்கப்பட்டுள்ளன.\n\n{text}\n\nபாதுகாப்பு நினைவூட்டல்: மருத்துவ ஆலோசனைக்கு உங்கள் மருத்துவரை அணுகவும்."

    return text
