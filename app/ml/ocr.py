import cv2
import os
import easyocr
from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, languages):
        # Загружаем модель YOLO один раз при инициализации класса
        self.model = YOLO('app/ml/models/best.pt')
        # Инициализируем EasyOCR reader
        self.reader = easyocr.Reader(languages)

    def detect_and_read(self, image_path):
        img_name = os.path.basename(image_path)
        img = cv2.imread(image_path)

        if img is None:
            raise ValueError(f"Image at {image_path} could not be loaded.")

        height, width, _ = img.shape
        results = self.model.predict(img, verbose=False)

        yolo_bboxes = []
        full_text = ""

        # Обрабатываем обнаруженные объекты
        for result in results:
            for bbox in result.boxes.xyxy:  # Получаем координаты ограничивающего прямоугольника
                x1, y1, x2, y2 = map(int, bbox)  # Преобразуем в целые числа

                # Рассчитываем значения в формате YOLO
                x_center = (x1 + x2) / 2 / width
                y_center = (y1 + y2) / 2 / height
                bbox_width = (x2 - x1) / width
                bbox_height = (y2 - y1) / height

                # Добавляем в список ограничивающих прямоугольников YOLO (предполагаем, что class_id равен 0)
                yolo_bboxes.append(f"0 {x_center} {y_center} {bbox_width} {bbox_height}")

                # Обрезаем изображение по координатам ограничивающего прямоугольника
                cropped_img = img[y1:y2, x1:x2]

                # Используем EasyOCR для чтения текста из обрезанного изображения
                text_results = self.reader.readtext(cropped_img)

                # Собираем обнаруженный текст
                for (bbox, text, prob) in text_results:
                    full_text += text + " "

        full_text = full_text.strip()
        yolo_bboxes = "\n".join(yolo_bboxes)

        return img_name, full_text, yolo_bboxes
