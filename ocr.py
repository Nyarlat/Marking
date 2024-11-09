import cv2
import easyocr
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('best.pt')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the language(s) you want to use

def detect_and_read(image_path):
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

            # Use EasyOCR to read text from the cropped image
            text_results = reader.readtext(cropped_img)

            # Print detected text
            for (bbox, text, prob) in text_results:
                full_text += text + " "
                # print(f"Detected text: {text} with confidence: {prob:.2f}")

    # print(full_text.strip())
    return full_text.strip()

if __name__ == '__main__':
    detect_and_read('4.JPG')