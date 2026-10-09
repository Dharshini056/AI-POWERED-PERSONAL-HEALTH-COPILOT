import os
import re
import time
import math
import cv2
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from typing import Dict, Any, List, Tuple

# Import RapidOCR (PaddleOCR ONNX engine)
try:
    from rapidocr_onnxruntime import RapidOCR
    rapid_ocr = RapidOCR()
except Exception as e:
    print("Warning: RapidOCR initialization error:", e)
    rapid_ocr = None

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

    total_indic = tamil_count + hindi_count + telugu_count + malayalam_count + kannada_count

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

def preprocess_image(cv_img: np.ndarray) -> np.ndarray:
    """
    Preprocess image for optimal OCR:
    1. Resize if too small or excessively large
    2. Grayscale conversion
    3. Denoising / Bilateral filtering
    4. Contrast enhancement (CLAHE)
    5. Deskewing
    """
    if cv_img is None:
        raise ValueError("Invalid image input for preprocessing")

    # Ensure 3-channel BGR or 1-channel Grayscale
    if len(cv_img.shape) == 3:
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    else:
        gray = cv_img.copy()

    # Resize if image width is under 1200 or over 3000
    h, w = gray.shape[:2]
    if w < 1000:
        scale = 1200 / float(w)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    elif w > 3000:
        scale = 2400 / float(w)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # 1. Bilateral filter for edge-preserving denoising
    denoised = cv2.bilateralFilter(gray, d=7, sigmaColor=50, sigmaSpace=50)

    # 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # 3. Deskew
    try:
        coords = np.column_stack(np.where(enhanced < 180))
        if len(coords) > 50:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            elif angle > 45:
                angle = 90 - angle
            else:
                angle = -angle

            if abs(angle) > 0.5 and abs(angle) < 30.0:
                (nh, nw) = enhanced.shape[:2]
                center = (nw // 2, nh // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                enhanced = cv2.warpAffine(
                    enhanced, M, (nw, nh),
                    flags=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REPLICATE
                )
    except Exception as e:
        # If deskew calculation encounters edge case, continue with enhanced
        pass

    return enhanced

def extract_from_digital_pdf(pdf_path: str) -> Tuple[str, bool]:
    """
    Detect whether PDF contains selectable text.
    Returns (extracted_text, is_selectable).
    """
    try:
        doc = fitz.open(pdf_path)
        all_text = []
        for page in doc:
            text = page.get_text("text")
            if text and len(text.strip()) > 30:
                all_text.append(text.strip())
        doc.close()

        full_text = "\n\n".join(all_text)
        # If more than 50 characters extracted, treat as digital selectable PDF
        if len(full_text.strip()) > 50:
            return full_text, True
        return "", False
    except Exception as e:
        print("Error checking selectable PDF:", e)
        return "", False

def render_pdf_to_images(pdf_path: str, max_pages: int = 5) -> List[np.ndarray]:
    """
    Convert scanned PDF pages to high-resolution OpenCV images using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    images = []
    zoom = 2.0  # 144-200 DPI equivalent for crisp text
    mat = fitz.Matrix(zoom, zoom)

    for i in range(min(len(doc), max_pages)):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        # Convert pixmap to numpy array
        img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.h, pix.w, pix.n))
        if pix.n == 4:
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
        elif pix.n == 3:
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        else:
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)
        images.append(img_bgr)
    doc.close()
    return images

def run_ocr_pipeline(file_path: str) -> Dict[str, Any]:
    """
    Execute full OCR pipeline with:
    - Digital PDF detection
    - Scanned PDF rendering
    - OpenCV image preprocessing (denoise, CLAHE, deskew)
    - RapidOCR (PaddleOCR ONNX) extraction
    - Confidence scoring & language detection
    """
    start_time = time.time()
    ext = os.path.splitext(file_path)[1].lower()

    extracted_lines = []
    confidences = []
    method_used = "RapidOCR-PaddleONNX"

    if ext == ".pdf":
        digital_text, is_selectable = extract_from_digital_pdf(file_path)
        if is_selectable:
            processing_time = int((time.time() - start_time) * 1000)
            lang = detect_language(digital_text)
            return {
                "raw_text": digital_text,
                "cleaned_text": digital_text,
                "detected_language": lang,
                "confidence_score": 0.98,
                "is_low_confidence": False,
                "method": "Direct Digital PDF Text Extraction",
                "processing_time_ms": processing_time,
                "page_count": 1
            }

        # Otherwise scanned PDF: render pages to images
        images = render_pdf_to_images(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"]:
        cv_img = cv2.imread(file_path)
        if cv_img is None:
            # Fallback to PIL
            pil_img = Image.open(file_path).convert("RGB")
            cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        images = [cv_img]
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    # Process each page/image
    for idx, img in enumerate(images):
        preprocessed = preprocess_image(img)

        if rapid_ocr:
            try:
                ocr_results, _ = rapid_ocr(preprocessed)
                if ocr_results:
                    for item in ocr_results:
                        # item is [box, text, score]
                        box, text, score = item[0], item[1], float(item[2])
                        if text and text.strip():
                            extracted_lines.append(text.strip())
                            confidences.append(score)
            except Exception as e:
                print(f"RapidOCR page {idx} error: {e}")

    # If OCR didn't yield text or RapidOCR was unavailable, try fallback PyMuPDF text or basic OCR
    if not extracted_lines and ext == ".pdf":
        digital_text, _ = extract_from_digital_pdf(file_path)
        if digital_text:
            extracted_lines = digital_text.split("\n")
            confidences = [0.90]

    raw_text = "\n".join(extracted_lines)
    cleaned_text = re.sub(r'[ \t]+', ' ', raw_text).strip()

    avg_confidence = round(float(np.mean(confidences)), 2) if confidences else 0.85
    # If no text detected at all, confidence is 0.0
    if not cleaned_text:
        avg_confidence = 0.0

    detected_lang = detect_language(cleaned_text)
    is_low_confidence = avg_confidence < 0.65 or len(cleaned_text) < 15
    processing_time = int((time.time() - start_time) * 1000)

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "detected_language": detected_lang,
        "confidence_score": avg_confidence,
        "is_low_confidence": is_low_confidence,
        "method": method_used,
        "processing_time_ms": processing_time,
        "page_count": len(images) if 'images' in locals() else 1
    }
