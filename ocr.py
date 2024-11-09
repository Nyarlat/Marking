import cv2
import os
import easyocr
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('best.pt')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the language(s) you want to use


def detect_and_read(image_path):
    img_name = os.path.basename(image_path)
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    # Perform object detection
    results = model.predict(img, verbose=False)
    yolo_bboxes = []

    full_text = ""
    # Iterate through detected bounding boxes
    for result in results:
        for bbox in result.boxes.xyxy:  # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, bbox)  # Convert to integer

            # Calculate YOLO format values
            x_center = (x1 + x2) / 2 / width
            y_center = (y1 + y2) / 2 / height
            bbox_width = (x2 - x1) / width
            bbox_height = (y2 - y1) / height

            # Append to YOLO bounding boxes list (assuming class_id is 0)
            yolo_bboxes.append(f"0 {x_center} {y_center} {bbox_width} {bbox_height}")

            # Crop the image to the bounding box area
            cropped_img = img[y1:y2, x1:x2]

            # Use EasyOCR to read text from the cropped image
            text_results = reader.readtext(cropped_img)

            # Print detected text
            for (bbox, text, prob) in text_results:
                full_text += text + " "

    # print(full_text.strip())
    full_text = '"' + full_text.strip() + '"'
    yolo_bboxes = "\n".join(yolo_bboxes)
    return img_name, full_text, yolo_bboxes


if __name__ == '__main__':
    detect_and_read('4.JPG')
