from ultralytics import YOLO

model = YOLO("./runs/detect/yolov8n_manual_v2_train/weights/best.pt")
test_folder = "./datasets/00_original"

results = model.predict(
    source=test_folder,
    imgsz=512,
    device="mps",
    conf=0.2,
    save=True,
    save_txt=False,
    project="./annotated",
    name="test-images",
    exist_ok=True
)