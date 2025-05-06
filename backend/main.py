from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import uuid
import base64
import io

from ultralytics import YOLO
import pytesseract

# Load the YOLO model
model = YOLO("yolov8_license_plate.pt")

app = FastAPI()

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def pil_to_base64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()

@app.post("/detect")
async def detect_license_plate(file: UploadFile = File(...)):
    # Save uploaded file
    img_path = UPLOAD_DIR / f"{uuid.uuid4()}.jpg"
    with img_path.open("wb") as f:
        f.write(await file.read())

    # Load image
    image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Run YOLOv8 detection
    results = model(str(img_path))[0]
    if not results.boxes:
        return JSONResponse({
            "cropped": [],
            "ocr": [],
            "highlighted": pil_to_base64(image)
        })

    cropped_list = []
    ocr_list = []

    for box in results.boxes:
        coords = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
        conf = float(box.conf[0])

        # Crop the detected region
        cropped = image.crop(coords)
        cropped_list.append(pil_to_base64(cropped))

        # Run OCR on the cropped plate
        text = pytesseract.image_to_string(cropped, config="--psm 8").strip()
        ocr_list.append(text)

        # Draw bounding box in blue
        draw.rectangle(coords, outline="blue", width=4)

        # Draw confidence above the box
        label = f"{conf:.2f}"
        # Compute text size (Python 3.13-safe)
        bbox = font.getbbox(label)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x1, y1 = coords[0], coords[1]
        label_bg = [x1, y1 - text_height - 4, x1 + text_width + 4, y1]
        draw.rectangle(label_bg, fill="blue")
        draw.text((x1 + 2, y1 - text_height - 2), label, fill="white", font=font)

    return JSONResponse({
        "cropped": cropped_list,
        "ocr": ocr_list,
        "highlighted": pil_to_base64(image)
    })


# Enable CORS for local frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_methods=["*"],
    allow_headers=["*"],
)
