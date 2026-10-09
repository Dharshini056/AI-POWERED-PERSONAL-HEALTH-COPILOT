import os
import re
import time
import cv2
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from typing import Dict, Any, List, Tuple

from .language_detector import detect_language
from .image_preprocessor import preprocess_image

# Import RapidOCR (PaddleOCR ONNX engine)
try:
    from rapidocr_onnxruntime import RapidOCR
    rapid_ocr = RapidOCR()
except Exception as e:
    print("Warning: RapidOCR initialization error:", e)
    rapid_ocr = None

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

        images = render_pdf_to_images(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"]:
        cv_img = cv2.imread(file_path)
        if cv_img is None:
            pil_img = Image.open(file_path).convert("RGB")
            cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        images = [cv_img]
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    for idx, img in enumerate(images):
        preprocessed = preprocess_image(img)

        if rapid_ocr:
            try:
                ocr_results, _ = rapid_ocr(preprocessed)
                if ocr_results:
                    for item in ocr_results:
                        text, score = item[1], float(item[2])
                        if text and text.strip():
                            extracted_lines.append(text.strip())
                            confidences.append(score)
            except Exception as e:
                print(f"RapidOCR page {idx} error: {e}")

    if not extracted_lines and ext == ".pdf":
        digital_text, _ = extract_from_digital_pdf(file_path)
        if digital_text:
            extracted_lines = digital_text.split("\n")
            confidences = [0.90]

    raw_text = "\n".join(extracted_lines)
    cleaned_text = re.sub(r'[ \t]+', ' ', raw_text).strip()

    avg_confidence = round(float(np.mean(confidences)), 2) if confidences else 0.85
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
