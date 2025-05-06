from ultralytics import YOLO

def main():
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Train!
    model.train(
        data='datasets/data_manual_v2.yaml',  # path to your data config
        epochs=100,
        imgsz=512,
        batch=32,
        device="mps",
        workers=8,
        cache=True,
        augment=True,
        name='yolov8n_manual_v2_train',
        optimizer='AdamW',
        lr0=1e-3,
        lrf=0.01,
        weight_decay=1e-2,
        patience=10,
        seed=42,
    )

if __name__ == '__main__':
    main()