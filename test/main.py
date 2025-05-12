from pathlib import Path
from PIL import Image
import numpy as np
import cv2

from ultralytics import YOLO
from fast_plate_ocr import ONNXPlateRecognizer

IMAGES_DIR = Path("images")
OUTPUT_DIR = Path("out")
OUTPUT_FILENAME = "out.csv"

OUTPUT_DIR.mkdir(exist_ok=True)

detector = YOLO("yolov8_license_plate.pt")
ocr = ONNXPlateRecognizer("european-plates-mobile-vit-v2-model")

def format_hungarian_plate(plate: str) -> str:
    """
    Format the OCR text to match Hungarian license plate format.
    """
    if len(plate) == 6 and plate[:3].isalpha() and plate[3:].isdigit():
        return plate[:3] + '-' + plate[3:]
    
    elif len(plate) == 7 and plate[:4].isalpha() and plate[4:].isdigit():
        return plate[:4] + '-' + plate[4:]

    return plate


def main():
    # Open the output file for writing
    output = ""

    # Iterate over all images in the IMAGES_DIR
    for image_path in IMAGES_DIR.glob("*.jpg"):
        pil_img = Image.open(image_path).convert("RGB")

        # Detect plate with YOLO
        img_np = np.array(pil_img)
        results = detector(img_np)[0]
        boxes = results.boxes

        ocr_texts = []

        for box in boxes:
            x, y, w, h = map(int, box.xyxy[0].tolist())

            plate_pil = pil_img.crop((x, y, w, h))
            plate_bgr = cv2.cvtColor(np.array(plate_pil), cv2.COLOR_RGB2BGR)
            plate_gray = cv2.cvtColor(plate_bgr, cv2.COLOR_BGR2GRAY)

            ocr_result = ocr.run(plate_gray)
            text = getattr(ocr_result, 'text', str(ocr_result)).strip()

            text = ''.join(filter(str.isalnum, text))
            text = format_hungarian_plate(text)
            ocr_texts.append(text)

        # Write the results to the output file
        output += f"{image_path.name};{';'.join(ocr_texts)}\n"

    # Save the output to a CSV file
    with open(OUTPUT_DIR / OUTPUT_FILENAME, "w") as f:
        f.write(output)

    print(f"Results saved to {OUTPUT_DIR / OUTPUT_FILENAME}")


if __name__ == "__main__":
    main()
