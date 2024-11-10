import cv2
import numpy as np
from sklearn.linear_model import LinearRegression


def segment_number_area(image):
    # Преобразуем изображение в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем бинаризацию
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Находим контуры
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Проверяем, есть ли найденные контуры
    if not contours:
        print("No contours found in the image.")
        return None  # или вернуть пустую маску np.zeros_like(binary)

    # Предполагаем, что номер находится в самом большом контуре
    largest_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(binary)
    cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

    return mask


def get_rotation_angle(mask):
    if mask is None:
        print("Mask is None. Cannot calculate rotation angle.")
        return 0

    # Получаем координаты точек маски
    y_indices, x_indices = np.where(mask > 0)

    # Формируем массив для линейной регрессии
    X = x_indices.reshape(-1, 1)
    Y = y_indices.reshape(-1, 1)

    # Создаем и обучаем модель линейной регрессии
    model = LinearRegression()
    model.fit(X, Y)

    # Получаем коэффициент наклона
    slope = model.coef_[0][0]

    # Вычисляем угол поворота (в радианах)
    angle = np.arctan(slope) * (180 / np.pi)

    return angle


def rotate_image(image, angle):
    # Поворачиваем изображение на заданный угол
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h))

    return rotated_image