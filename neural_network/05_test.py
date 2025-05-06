from ultralytics import YOLO

# 1. Load your best checkpoint
model = YOLO("./runs/detect/yolov8n_manual_v2_train/weights/best.pt")

# 2. Point to your test images folder
test_folder = "./datasets/00_original"  # e.g. "./datasets/license_plate/images/test"

# 3. Run prediction and save annotated output
results = model.predict(
    source=test_folder,       # folder of test images
    imgsz=512,               # match training image size
    device="mps",             # or "cpu"/"cuda:0"
    conf=0.2,                # confidence threshold
    save=True,                # save images with boxes drawn
    save_txt=False,           # skip saving raw coords (optional)
    project="./annotated",    # output directory
    name="test-images",    # subfolder name
    exist_ok=True             # overwrite if exists
)