import cv2
import pytesseract
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('best.pt')

def detect_and_read2(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Perform object detection
    results = model.predict(img, verbose=False)

    full_text = ""
    # Iterate through detected bounding boxes
    for result in results:
        for bbox in result.boxes.xyxy:  # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, bbox)  # Convert to integer
            # Crop the image to the bounding box area
            cropped_img = img[y1:y2, x1:x2]
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # Use Tesseract to read text from the cropped image
            text = pytesseract.image_to_string(cropped_img)

            # Print detected text
            if text.strip():  # Check if text is not empty
                full_text += text + " "

    # print(full_text.strip())
    return full_text.strip()

if __name__ == '__main__':
    detect_and_read2('4.JPG')