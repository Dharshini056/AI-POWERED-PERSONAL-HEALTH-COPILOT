import cv2
import numpy as np

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

    # Resize if image width is under 1000 or over 3000
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
    except Exception:
        # If deskew calculation encounters edge case, continue with enhanced
        pass

    return enhanced
