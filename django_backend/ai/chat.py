import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

DISCLAIMER_TEXT = "This AI Personal Health Copilot provides informational support and does not replace professional medical advice, clinical diagnosis, or treatment decisions. Always consult your qualified healthcare provider."

def generate_chat_reply(
    user_query: str,
    patient_context: Dict[str, Any],
    session_history: List[Dict[str, str]] = None,
    language: str = "English"
) -> Dict[str, Any]:
    """
    Context-grounded chat responder strictly adhering to uploaded records.
    """
    q_lower = user_query.lower()
    medications = patient_context.get("medications", [])
    lab_results = patient_context.get("lab_results", [])
    diagnoses = patient_context.get("diagnoses", [])
    events = patient_context.get("medical_events", [])
    patient = patient_context.get("patient", {})

    sources = []

    # If OpenAI API is available, invoke with grounded clinical context
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)

            system_instruction = f"""You are the 'AI Personal Health Copilot'.
You assist patients in understanding their own uploaded medical records.

STRICT SAFETY & GROUNDING RULES:
1. ONLY answer document-specific questions using the provided Structured Health Records.
2. If the user asks about an event, drug, condition, or test that is NOT in the records, explicitly respond:
   "I couldn't find that information in your uploaded records."
3. NEVER diagnose diseases, prescribe medicines, or advise changing, stopping, or starting medications.
4. For lab values, discuss them purely relative to the recorded reference ranges in simple educational terms.
5. If the user asks what to ask their doctor, provide helpful, clarifying questions they can bring to their next appointment.
6. Support Tamil responses if the user asks in Tamil or requests Tamil translation.
7. Always maintain an empathetic, objective, and supportive tone.

UPLOADED PATIENT RECORD CONTEXT:
Patient: {patient.get('name', 'Arun Kumar')}, Age: {patient.get('age', 42)}, Gender: {patient.get('gender', 'Male')}
Diagnoses: {[d.get('name') for d in diagnoses]}
Medications: {[{'name': m.get('name'), 'dose': m.get('dose'), 'freq': m.get('frequency'), 'timing': m.get('instructions')} for m in medications]}
Lab Results: {[{'test': l.get('test_name'), 'val': l.get('value'), 'unit': l.get('unit'), 'range': l.get('reference_range'), 'status': l.get('status')} for l in lab_results]}
Recent Medical Events: {[{'title': e.get('title'), 'date': e.get('event_date'), 'doc': e.get('doctor_name')} for e in events]}
"""
            messages = [{"role": "system", "content": system_instruction}]
            if session_history:
                for h in session_history[-4:]:
                    messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
            messages.append({"role": "user", "content": user_query})

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.2
            )
            reply = completion.choices[0].message.content
            return {
                "reply": reply,
                "sources": [e.get("title", "Clinical Document") for e in events] or ["Uploaded Medical Records"],
                "disclaimer": DISCLAIMER_TEXT
            }
        except Exception as e:
            print("OpenAI Chat fallback triggered:", e)

    # Deterministic grounded responses for high-reliability demo
    if any(k in q_lower for k in ["medicine", "medication", "drug", "tablet", "pill", "மருந்து"]):
        if not medications:
            reply = "I couldn't find any medications in your uploaded records. Please upload a prescription or discharge summary to track medications."
        else:
            lines = ["Here are the medications recorded in your uploaded documents:"]
            for m in medications:
                lines.append(f"• **{m.get('name')}** — {m.get('dose', '')} | {m.get('frequency', 'As directed')} | Duration: {m.get('duration', 'N/A')} ({m.get('instructions', 'As prescribed')})")
            lines.append("\n⚠️ **Safety Reminder:** Verify medication name, dose, and instructions against your original prescription before taking or changing any medication. Never adjust dosages without your doctor's guidance.")
            reply = "\n".join(lines)
            sources = ["Prescription Records"]

    elif any(k in q_lower for k in ["abnormal", "out of range", "lab value", "test value", "high", "low", "blood test", "blood report", "ஹீமோகுளோபின்"]):
        abnormals = [l for l in lab_results if l.get("status") in ["Below reference range", "Above reference range", "High", "Low", "Critical"]]
        if not abnormals:
            reply = "All laboratory tests in your uploaded reports are currently within their documented normal reference ranges."
        else:
            lines = ["Here are the laboratory values outside their reference ranges from your uploaded reports:"]
            for l in abnormals:
                lines.append(f"• **{l.get('test_name')}**: Measured at **{l.get('value')} {l.get('unit', '')}** (Reference Range: {l.get('reference_range')}) — **{l.get('status')}**")
                if l.get("explanation"):
                    lines.append(f"  *What this means:* {l.get('explanation')}")
            lines.append("\n💡 *Please Note:* A value outside the reference range can occur for many benign or clinical reasons and does not constitute an automatic diagnosis. Please discuss these numbers with your doctor.")
            reply = "\n".join(lines)
            sources = ["Laboratory Reports"]

    elif any(k in q_lower for k in ["history", "timeline", "past visit", "hospital visit", "recent", "events"]):
        if not events and not diagnoses:
            reply = "I couldn't find past medical visits or history recorded in your uploaded files yet."
        else:
            lines = ["Here is a summary of your documented medical history:"]
            if diagnoses:
                lines.append("**Diagnoses & Conditions:**")
                for d in diagnoses:
                    lines.append(f"• {d.get('name')} (Date: {d.get('date', 'N/A')})")
            if events:
                lines.append("\n**Recent Healthcare Encounters:**")
                for ev in events:
                    lines.append(f"• {ev.get('event_date', '')} — **{ev.get('title')}** at {ev.get('facility_name', 'Clinic')} ({ev.get('doctor_name', 'Attending Physician')})")
            reply = "\n".join(lines)
            sources = ["Clinical Records & Timeline"]

    elif any(k in q_lower for k in ["ask doctor", "questions for doctor", "ask my doctor", "physician question"]):
        abnormals = [l for l in lab_results if l.get("status") in ["Below reference range", "Above reference range", "High", "Low"]]
        lines = [
            "Here are recommended questions you can ask your healthcare provider based on your uploaded records:",
            "1. *Regarding Lab Findings:* 'My report shows my " + (abnormals[0]['test_name'] if abnormals else 'values') + " was outside the standard reference range. Does this need repeat testing or specific lifestyle/dietary adjustments?'",
            "2. *Regarding Medications:* 'Are there any potential interactions between my current medications, and what signs should I watch for?'",
            "3. *Regarding Monitoring:* 'When should I schedule my next follow-up examination or routine blood test?'",
            "4. *Regarding Symptoms:* 'Are there any warning symptoms that would require immediate clinical attention?'"
        ]
        reply = "\n".join(lines)
        sources = ["Clinical Best Practices & Record Insights"]

    elif any(k in q_lower for k in ["tamil", "தமிழ்", "மொழிபெயர்ப்பு"]):
        reply = ("உங்கள் மருத்துவ ஆவணங்களின் சுருக்கம் (Tamil):\n\n"
                 "• நோயாளி பெயர்: " + (patient.get('name') or 'அருண் குமார்') + "\n"
                 "• கண்டறியப்பட்ட மருந்துகள்: " + (", ".join([m.get('name') for m in medications]) or "இல்லை") + "\n"
                 "• ஆய்வகப் பரிசோதனை: இரத்தப் பரிசோதனை மற்றும் மருந்துச் சீட்டு விவரங்கள் வெற்றிகரமாக பதிவு செய்யப்பட்டுள்ளன.\n\n"
                 "குறிப்பு: இந்தத் தகவல்கள் உங்கள் மருத்துவ ஆவணங்களிலிருந்து மட்டுமே பெறப்பட்டவை. மருத்துவ முடிவுகளுக்கு உங்கள் மருத்துவரை அணுகவும்.")
        sources = ["Uploaded Medical Records (Tamil View)"]

    else:
        reply = (
            f"I have reviewed your uploaded medical records for {patient.get('name', 'the patient')}. "
            f"You have {len(medications)} medication(s) and {len(lab_results)} lab parameter(s) documented. "
            "You can ask me to list your medications, explain abnormal lab results, summarize your recent medical history, or suggest questions to bring to your doctor's appointment!"
        )
        sources = ["Health Copilot Knowledge Index"]

    return {
        "reply": reply,
        "sources": sources,
        "disclaimer": DISCLAIMER_TEXT
    }
