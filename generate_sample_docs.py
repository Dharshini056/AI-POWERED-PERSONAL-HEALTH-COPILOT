import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_documents")
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "backend", "uploads")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

def create_sample_prescription_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, "1_Sample_Prescription_Metformin.pdf")
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # A4 size

    text = """APOLLO MULTISPECIALITY HOSPITALS
DEPARTMENT OF INTERNAL MEDICINE
Dr. S. Ramanathan, MD (Gen Med) | Reg No: TN-MC-48291
Date: 12 Aug 2026

PATIENT DETAILS:
Patient Name: Arun Kumar
Age: 42 Years        Gender: Male
Patient ID / UHID: AP-2026-90412

CLINICAL DIAGNOSIS:
Type 2 Diabetes Mellitus with Essential Hypertension

Rx (PRESCRIPTION):
1. Tab. Metformin 500 mg
   Dosage: 500 mg
   Frequency: Twice daily (1-0-1)
   Duration: 30 days
   Timing: After food (PC)

2. Tab. Telmisartan 40 mg
   Dosage: 40 mg
   Frequency: Once daily (1-0-0)
   Duration: 30 days
   Timing: Morning after food

3. Cap. Vitamin D3 60,000 IU
   Dosage: 60,000 IU
   Frequency: Once weekly
   Duration: 8 weeks
   Timing: After dinner with milk

ADVICE & INSTRUCTIONS:
- Restrict refined carbohydrates and dietary sodium.
- Minimum 30 mins brisk walking per day.
- Review in 1 month with Fasting Blood Sugar and HbA1c test reports.

Dr. S. Ramanathan, MD
Senior Consultant Physician"""

    page.insert_text((50, 70), text, fontsize=12, fontname="helv", color=(0.1, 0.1, 0.15))
    doc.save(pdf_path)
    doc.close()
    print("Created:", pdf_path)

def create_sample_lab_report_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, "2_Sample_Blood_Test_Report.pdf")
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    text = """METROPOLIS HEALTHCARE CLINICAL LABORATORY
ACCREDITED BY NABL & CAP
Patient Name: Arun Kumar        Age/Sex: 42 Y / Male
Referred By: Dr. S. Ramanathan  Lab Ref: MET-78401
Sample Collected: 18-Aug-2026   Report Date: 18-Aug-2026

BIOCHEMISTRY & COMPLETE BLOOD COUNT REPORT

TEST NAME                     RESULT     UNIT       REFERENCE RANGE   STATUS
-----------------------------------------------------------------------------
Hemoglobin                    10.2       g/dL       12.0 - 16.0       Below reference range
Fasting Blood Sugar           142.0      mg/dL      70.0 - 100.0      Above reference range
HbA1c Glycated Hemoglobin     7.4        %          4.0 - 5.7         Above reference range
Serum Creatinine              0.95       mg/dL      0.6 - 1.2         Normal
Total Cholesterol             186.0      mg/dL      125.0 - 200.0     Normal
WBC Count                     6800       /mcL       4000 - 11000      Normal
Platelet Count                240000     /mcL       150000 - 450000   Normal

CLINICAL OBSERVATION:
- Mild Microcytic Anemia observation (Hemoglobin: 10.2 g/dL).
- Elevated glycemic indicators (FBS: 142.0 mg/dL, HbA1c: 7.4%).
- Normal Renal function and lipid metabolism parameters.

Report Verified by:
Dr. K. Meenakshi, MD (Pathology)
Chief Clinical Pathologist"""

    page.insert_text((50, 70), text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.15))
    doc.save(pdf_path)
    doc.close()
    print("Created:", pdf_path)

def create_sample_discharge_summary_pdf():
    pdf_path = os.path.join(OUTPUT_DIR, "3_Sample_Discharge_Summary.pdf")
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    text = """CITY HEALTH MULTISPECIALITY HOSPITAL
DAY CARE DISCHARGE SUMMARY
Admission Date: 03-Sep-2026 (08:30 AM)
Discharge Date: 03-Sep-2026 (05:00 PM)

Patient Name: Arun Kumar        Age: 42 Y    Sex: Male
Consultant: Dr. V. Sundaram, MS, MCh (Surgical Gastroenterology)
IP No: IP-2026-44189

DIAGNOSIS AT DISCHARGE:
Symptomatic Cholelithiasis (Gallbladder calculus)

PROCEDURE PERFORMED:
Diagnostic Ultrasound & Elective Pre-op Evaluation
Date of Procedure: 03-Sep-2026
Facility: City Health Multispeciality Hospital

SUMMARY OF CLINICAL COURSE:
Patient admitted for routine day-care abdominal evaluation. Vital parameters stable.
ECG and chest radiography within normal physiological limits.
Discharged in clinically stable status.

DISCHARGE MEDICATIONS:
1. Tab. Pantoprazole 40 mg — Once daily (1-0-0) before breakfast for 14 days.
2. Tab. Paracetamol 650 mg — As needed (SOS) for mild abdominal discomfort.

FOLLOW-UP ADVICE:
Follow up in Surgical OPD on 15-Sep-2026.

Dr. V. Sundaram, MS, MCh
Consultant Surgeon"""

    page.insert_text((50, 70), text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.15))
    doc.save(pdf_path)
    doc.close()
    print("Created:", pdf_path)

def create_sample_tamil_prescription_image():
    img_path = os.path.join(OUTPUT_DIR, "4_Sample_Tamil_English_Prescription.png")
    # Create white canvas
    w, h = 900, 1100
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw header lines
    draw.rectangle([(30, 30), (w - 30, h - 30)], outline=(180, 200, 220), width=2)
    draw.rectangle([(40, 40), (w - 40, 150)], fill=(240, 248, 255), outline=(200, 225, 245), width=1)

    # Try default or standard font
    font = ImageFont.load_default()

    lines = [
        "SANTHI HEALTH CLINIC - சாந்தி நல்வாழ்வு மையம்",
        "Dr. R. Karthik, MBBS, MD | டாக்டர். ஆர். கார்த்திக், MD",
        "Reg: TN-MC-61920 | Date: 12-Sep-2026",
        "------------------------------------------------------------------",
        "PATIENT DETAILS / நோயாளி விவரங்கள்:",
        "Name / பெயர்: Arun Kumar (அருண் குமார்)",
        "Age / வயது: 42 Years (ஆண்டுகள்)     Sex / பாலினம்: Male (ஆண்)",
        "UHID: SHC-2026-118",
        "------------------------------------------------------------------",
        "DIAGNOSIS / மருத்துவக் குறிப்பு:",
        "Type 2 Diabetes & Hypertension (நீரிழிவு நோய் மற்றும் இரத்த அழுத்தம்)",
        "------------------------------------------------------------------",
        "Rx - PRESCRIPTION / மருந்து விவரங்கள்:",
        "",
        "1. மருந்து: Metformin 500 mg",
        "   அளவு: 500 mg",
        "   மாத்திரை உட்கொள்ளும் முறை: Twice daily (1-0-1) - இரண்டு முறை",
        "   கால அளவு: 30 நாட்கள் (30 days)",
        "   குறிப்பு: உணவுக்குப் பின் (After food)",
        "",
        "2. மருந்து: Atorvastatin 10 mg",
        "   அளவு: 10 mg",
        "   மாத்திரை உட்கொள்ளும் முறை: Once daily at night (0-0-1)",
        "   கால அளவு: 30 நாட்கள் (30 days)",
        "   குறிப்பு: உணவுக்குப் பின் (After dinner)",
        "",
        "3. மருந்து: Pantoprazole 40 mg",
        "   அளவு: 40 mg",
        "   மாத்திரை உட்கொள்ளும் முறை: Once daily morning (1-0-0)",
        "   கால அளவு: 15 நாட்கள் (15 days)",
        "   குறிப்பு: உணவுக்கு முன் (Before food)",
        "",
        "------------------------------------------------------------------",
        "Doctor Signature: Dr. R. Karthik, MD"
    ]

    y = 55
    for line in lines:
        draw.text((60, y), line, fill=(20, 30, 40), font=font)
        y += 30

    img.save(img_path)
    print("Created:", img_path)

if __name__ == "__main__":
    create_sample_prescription_pdf()
    create_sample_lab_report_pdf()
    create_sample_discharge_summary_pdf()
    create_sample_tamil_prescription_image()
