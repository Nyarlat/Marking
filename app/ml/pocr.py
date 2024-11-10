import cv2
import os
from ultralytics import YOLO
from paddleocr import PaddleOCR
from app.ml.image_rotation import rotate_image, segment_number_area, get_rotation_angle


class ImageProcessor:
    def __init__(self, yolo_model_path='app/ml/models/best.pt', ocr_lang='en', use_gpu=True):
        # Загружаем модель YOLO
        self.model = YOLO(yolo_model_path)
        # Инициализируем модель OCR
        self.ocr_model = PaddleOCR(use_angle_cls=True, lang=ocr_lang, use_gpu=use_gpu)

    def _ocr(self, img):
        """Вспомогательный метод для распознавания текста на изображении."""
        result = self.ocr_model.ocr(img, cls=True)
        if result and result[0]:
            full_text = " ".join([line[1][0] for line in result[0]])
        else:
            full_text = ""
        return full_text

    def detect_and_read(self, image_path):
        """Метод для загрузки изображения, выполнения детекции и распознавания текста."""
        # Загружаем изображение
        img_name = os.path.basename(image_path)
        img = cv2.imread(image_path)

        # Выполняем детекцию объектов
        height, width, _ = img.shape
        results = self.model.predict(img, verbose=False)

        yolo_bboxes = []
        full_text = ""
        # Проходим по найденным bounding boxes
        for result in results:
            for bbox in result.boxes.xyxy:  # Получаем координаты bounding box
                x1, y1, x2, y2 = map(int, bbox)  # Преобразуем в целые числа

                # Рассчитываем значения в формате YOLO
                x_center = (x1 + x2) / 2 / width
                y_center = (y1 + y2) / 2 / height
                bbox_width = (x2 - x1) / width
                bbox_height = (y2 - y1) / height

                # Добавляем в список ограничивающих прямоугольников YOLO
                yolo_bboxes.append(f"0 {round(x_center, 6)} {round(y_center, 6)} {round(bbox_width, 6)} {round(bbox_height, 6)}\n")

                # Обрезаем изображение по области bounding box
                cropped_img = img[y1:y2, x1:x2]

                # mask = segment_number_area(cropped_img)
                # angle = get_rotation_angle(mask)
                # rotated_image = rotate_image(cropped_img, angle)

                text = self._ocr(cropped_img)  # Распознаем текст на обрезанном изображении
                full_text += text + " "

        full_text = full_text.strip()
        yolo_bboxes = "".join(yolo_bboxes)
        return img_name, full_text, yolo_bboxes
