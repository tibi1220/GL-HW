from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import uuid, base64, io
import numpy as np
import cv2

from ultralytics import YOLO
from fast_plate_ocr import ONNXPlateRecognizer

# Initialize FastAPI app
app = FastAPI()

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

detector = YOLO("yolov8_license_plate.pt")
ocr = ONNXPlateRecognizer("european-plates-mobile-vit-v2-model")


def pil_to_base64(pil_img: Image.Image) -> str:
    """
    Convert a PIL image to a Base64-encoded JPEG.
    """
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def format_hungarian_plate(plate: str) -> str:
    """
    Format the OCR text to match Hungarian license plate format.
    """
    if len(plate) == 6 and plate[:3].isalpha() and plate[3:].isdigit():
        return plate[:3] + '-' + plate[3:]
    
    elif len(plate) == 7 and plate[:4].isalpha() and plate[4:].isdigit():
        return plate[:4] + '-' + plate[4:]

    return plate


@app.post("/detect")
async def detect_license_plate(file: UploadFile = File(...)):
    # Read image bytes
    content = await file.read()
    pil_img = Image.open(io.BytesIO(content)).convert("RGB")
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.load_default()

    # Detect license plates with YOLO
    img_np = np.array(pil_img)
    results = detector(img_np)[0]
    boxes = results.boxes

    cropped_b64 = []
    ocr_texts = []

    for box in boxes:
        # Extract bounding box coordinates
        x, y, w, h = map(int, box.xyxy[0].tolist())

        # Crop license plate region
        plate_pil = pil_img.crop((x, y, w, h))
        cropped_b64.append(pil_to_base64(plate_pil))

        # Prepare array for OCR: convert to BGR then to grayscale
        plate_bgr = cv2.cvtColor(np.array(plate_pil), cv2.COLOR_RGB2BGR)
        plate_gray = cv2.cvtColor(plate_bgr, cv2.COLOR_BGR2GRAY)

        # Run OCR on grayscale plate
        ocr_result = ocr.run(plate_gray)
        text = getattr(ocr_result, 'text', str(ocr_result)).strip()

        # Remove non-alphanumeric characters
        text = ''.join(filter(str.isalnum, text))

        text = format_hungarian_plate(text)

        ocr_texts.append(text)

        # Draw detection box and confidence
        conf = float(box.conf[0])
        draw.rectangle((x, y, w, h), outline="blue", width=3)
        label = f"{conf:.2f}"
        
        x0, y0, x1b, y1b = font.getbbox(label)
        text_width  = x1b - x0
        text_height = y1b - y0
        # draw a filled background for the label
        draw.rectangle(
            [x, y - text_height - 4, x + text_width + 4, y],
            fill="blue"
        )
        draw.text(
            (x + 2, y - text_height - 2),
            label,
            fill="white",
            font=font
        )

    # Return JSON with cropped images, OCR texts, annotated image, and count
    return JSONResponse({
        "cropped": cropped_b64,
        "ocr": ocr_texts,
        "highlighted": pil_to_base64(pil_img),
        "length": len(ocr_texts)
    })
