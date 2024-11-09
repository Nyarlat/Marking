from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('yolo11n.pt')

    results = model.train(
        data='marking.yaml',
        imgsz=640,
        epochs=50,
        batch=8,
        name='yolov11n_marking',
        device='0'
    )