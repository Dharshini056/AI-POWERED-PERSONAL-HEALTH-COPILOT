import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Curated Tamil translations and templates for safe medical communication
TAMIL_LAB_DESCRIPTIONS = {
    "Hemoglobin": {
        "concept": "ஹீமோகுளோபின் (இரத்த சிவப்பணுக்களில் உள்ள ஆக்ஸிஜன் தாங்கும் புரதம்)",
        "low": "அறிக்கையில் கொடுக்கப்பட்டுள்ள reference range-ஐ விட ஹீமோகுளோபின் அளவு குறைவாக உள்ளது. இது பொதுவாக இரும்புச்சத்து குறைபாடு அல்லது இரத்த சோகை காரணங்களால் ஏற்படலாம். இதற்கான சரியான காரணத்தை உங்கள் மருத்துவர் மற்ற பரிசோதனைகளுடன் சேர்த்து உறுதி செய்ய வேண்டும்.",
        "high": "ஹீமோகுளோபின் அளவு வழக்கமான அளவை விட அதிகமாக உள்ளது. நீரிழப்பு அல்லது பிற உடலியல் காரணங்களால் இது நிகழலாம். மருத்துவருடன் கலந்து ஆலோசிக்கவும்."
    },
    "Fasting Blood Sugar": {
        "concept": "வெறும் வயிற்றில் இரத்த சர்க்கரை அளவு (Fasting Blood Sugar)",
        "high": "இரத்த சர்க்கரை அளவு பரிந்துரைக்கப்பட்ட அளவை விட அதிகமாக பதிவாகியுள்ளது. உணவு முறை அல்லது இன்சுலின் மாற்றங்களை மருத்துவர் மூலம் மதிப்பாய்வு செய்ய பரிந்துரைக்கப்படுகிறது.",
        "low": "இரத்த சர்க்கரை அளவு குறைவாக உள்ளது (Hypoglycemia). மயக்கம் அல்லது நடுக்கம் போன்ற அறிகுறிகள் இருந்தால் மருத்துவரை அணுகவும்."
    },
    "HbA1c": {
        "concept": "HbA1c (கடந்த 3 மாத சராசரி இரத்த சர்க்கரை அளவு)",
        "high": "HbA1c அளவு நிர்ணயிக்கப்பட்ட வரம்பை விட அதிகமாக உள்ளது. நீரிழிவு கட்டுப்பாட்டை உங்கள் மருத்துவருடன் பரிசீலிக்கவும்.",
        "low": "HbA1c அளவு குறைவான வரம்பில் உள்ளது."
    },
    "Serum Creatinine": {
        "concept": "சீரம் கிரியேட்டினின் (சிறுநீரக செயல்பாட்டு குறியீடு)",
        "high": "சீரம் கிரியேட்டினின் அளவு பரிந்துரைக்கப்பட்ட வரம்பிற்கு மேல் உள்ளது. சிறுநீரகத்தின் வடிகட்டும் செயல்பாட்டை உங்கள் மருத்துவர் விரிவாக ஆய்வு செய்ய வேண்டும்.",
        "low": "கிரியேட்டினின் அளவு குறைவான வரம்பில் உள்ளது."
    },
    "Total Cholesterol": {
        "concept": "கொலஸ்ட்ரால் அளவு (இரத்த கொழுப்பு)",
        "high": "கொலஸ்ட்ரால் அளவு அனுமதிக்கப்பட்ட அளவை விட அதிகமாக உள்ளது. இதய நலன் மற்றும் உணவுமுறை மாற்றங்கள் குறித்து மருத்துவ ஆலோசனை பெறவும்.",
        "low": "கொலஸ்ட்ரால் அளவு இயல்பான குறைந்த வரம்பில் உள்ளது."
    }
}

TAMIL_DOC_TYPES = {
    "Prescription": "மருத்துவச் சீட்டு (Prescription)",
    "Laboratory Report": "ஆய்வக இரத்தப் பரிசோதனை அறிக்கை (Laboratory Report)",
    "Discharge Summary": "மருத்துவமனை வெளியேற்றச் சுருக்கம் (Discharge Summary)",
    "Diagnostic Report": "நோய் கண்டறிதல் அறிக்கை (Diagnostic Report)",
    "General Medical Record": "மருத்துவ ஆவணம்"
}

def generate_health_summary(structured_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates plain-language medical summary and abnormal lab explanations
    strictly obeying non-diagnostic safe medical communication rules.
    Outputs both English and Tamil summaries.
    """
    patient = structured_data.get("patient", {})
    doc_meta = structured_data.get("document", {})
    medications = structured_data.get("medications", [])
    lab_results = structured_data.get("lab_results", [])
    diagnoses = structured_data.get("diagnoses", [])

    doc_type = doc_meta.get("type", "Medical Document")
    doc_date = doc_meta.get("date", "recent date")
    patient_name = patient.get("name") or "the patient"

    # 1. Abnormal Lab Explanations
    abnormal_labs = [lab for lab in lab_results if lab.get("status") in ["Below reference range", "Above reference range", "High", "Low", "Critical"]]

    abnormal_explanations_en = []
    abnormal_explanations_ta = []

    for lab in abnormal_labs:
        name = lab.get("test_name", "Test")
        val = lab.get("value", "")
        unit = lab.get("unit", "")
        ref = lab.get("reference_range", "")
        status = lab.get("status", "")

        en_expl = f"• {name} ({val} {unit}): This value is outside the reference range shown in the report ({ref}). There can be several reasons for this result, and a healthcare professional should interpret it in context."
        abnormal_explanations_en.append(en_expl)

        # Tamil version
        ta_info = TAMIL_LAB_DESCRIPTIONS.get(name)
        if ta_info:
            if "below" in status.lower() or "low" in status.lower():
                ta_expl = f"• {ta_info['concept']}: மதிப்பு {val} {unit}. {ta_info['low']}"
            else:
                ta_expl = f"• {ta_info['concept']}: மதிப்பு {val} {unit}. {ta_info['high']}"
        else:
            ta_expl = f"• {name}: இந்த மதிப்பு ({val} {unit}) அறிக்கையில் குறிப்பிடப்பட்டுள்ள reference range ({ref})-ஐ விட வேறுபட்டுள்ளது. இதற்கான காரணத்தை மருத்துவர் உங்கள் மற்ற மருத்துவ தகவல்களுடன் சேர்த்து மதிப்பீடு செய்ய வேண்டும்."
        abnormal_explanations_ta.append(ta_expl)

    # 2. English Overall Summary
    en_paragraphs = []
    en_paragraphs.append(f"This document is a {doc_type} dated {doc_date} for {patient_name}.")

    if diagnoses:
        diag_list = ", ".join([d["name"] for d in diagnoses])
        en_paragraphs.append(f"Documented clinical conditions or impressions include: {diag_list}.")

    if medications:
        med_summary_parts = [f"{m['name']} ({m.get('dose', '')} {m.get('frequency', '')})".strip() for m in medications]
        en_paragraphs.append(f"It lists {len(medications)} medication(s): {', '.join(med_summary_parts)}.")

    if lab_results:
        en_paragraphs.append(f"A total of {len(lab_results)} laboratory parameters were recorded, of which {len(abnormal_labs)} are outside normal reference thresholds.")

    if abnormal_explanations_en:
        en_paragraphs.append("\nAbnormal Value Observations:\n" + "\n".join(abnormal_explanations_en))

    en_paragraphs.append("\nImportant Safety Note: This summary provides personal informational support only and does not formulate a medical diagnosis or change treatment plans. Please consult your physician for clinical interpretation.")
    summary_en = "\n\n".join(en_paragraphs)

    # 3. Tamil Overall Summary
    doc_type_ta = TAMIL_DOC_TYPES.get(doc_type, doc_type)
    ta_paragraphs = []
    ta_paragraphs.append(f"இந்த ஆவணம் {patient_name} என்பவருக்கான {doc_type_ta} ஆகும் (தேதி: {doc_date}).")

    if diagnoses:
        diag_list_ta = ", ".join([d["name"] for d in diagnoses])
        ta_paragraphs.append(f"ஆவணத்தில் குறிப்பிடப்பட்டுள்ள மருத்துவக் குறிப்புகள்: {diag_list_ta}.")

    if medications:
        med_list_ta = ", ".join([f"{m['name']} ({m.get('dose', '')})" for m in medications])
        ta_paragraphs.append(f"இதில் {len(medications)} மருந்துகள் பரிந்துரைக்கப்பட்டுள்ளன: {med_list_ta}.")

    if lab_results:
        ta_paragraphs.append(f"மொத்தம் {len(lab_results)} ஆய்வகப் பரிசோதனை முடிவுகள் கண்டறியப்பட்டுள்ளன, இதில் {len(abnormal_labs)} அளவீடுகள் நிர்ணயிக்கப்பட்ட வரம்பிற்கு வெளியே உள்ளன.")

    if abnormal_explanations_ta:
        ta_paragraphs.append("\nமுக்கிய ஆய்வக முடிவுகள் (Abnormal Values):\n" + "\n".join(abnormal_explanations_ta))

    ta_paragraphs.append("\nபாதுகாப்பு நினைவூட்டல்: இந்த AI சுருக்கம் தகவல் நோக்கங்களுக்காக மட்டுமே. மருந்துகளையோ சிகிச்சையையோ மாற்றுவதற்கு முன் உங்கள் மருத்துவரை அணுகவும்.")
    summary_ta = "\n\n".join(ta_paragraphs)

    return {
        "summary_en": summary_en,
        "summary_ta": summary_ta,
        "abnormal_findings_count": len(abnormal_labs),
        "abnormal_explanations_en": abnormal_explanations_en,
        "abnormal_explanations_ta": abnormal_explanations_ta
    }
