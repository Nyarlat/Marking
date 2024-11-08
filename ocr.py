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
    results = model.predict(img)

    # Iterate through detected bounding boxes
    for result in results:
        for bbox in result.boxes.xyxy:  # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, bbox)  # Convert to integer
            # Crop the image to the bounding box area
            cropped_img = img[y1:y2, x1:x2]

            # Use EasyOCR to read text from the cropped image
            text_results = reader.readtext(cropped_img)

            # Print detected text and bounding box coordinates
            for (bbox, text, prob) in text_results:
                print(f"Detected text: {text} with confidence: {prob:.2f}")
                # Optionally draw the bounding box on the original image
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the result image with detections
    cv2.imshow("Detected Text", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_and_read('367.JPG')