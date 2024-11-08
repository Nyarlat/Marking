from ultralytics import YOLO

if __name__ == '__main__':
    # Load the model.
    model = YOLO('yolo11n.pt')

    # Training.
    results = model.train(
        data='marking.yaml',
        imgsz=640,
        epochs=1,
        batch=8,
        name='yolov11n_marking',
        device='0'
    )

    model.export(format="tflite")