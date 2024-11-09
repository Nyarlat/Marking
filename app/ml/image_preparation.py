import cv2
import numpy as np

def img_preparation(
        image,
        inverted = False,
        binarizated = False,
        noise_removed = False
):
    if inverted:
        image = cv2.bitwise_not(image)
    if binarizated:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if noise_removed:
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image, 3)
    return image



