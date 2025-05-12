from ultralytics import YOLO

def main():
    model = YOLO('runs/detect/yolov8n_manual_train/weights/best.pt')

    model.predict(
        source='datasets/original',
        save_txt=True,
        project='datasets',
        name='02_auto_predictions_v1',
        device='mps',
        conf=0.5,
        imgsz=512,
        augment=True,
    )

if __name__ == '__main__':
    main()