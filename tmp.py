from ocr import detect_and_read
import os

def read_true_text(bbox_file_path):
    """Read the true text from the .bbox file."""
    with open(bbox_file_path, 'r', encoding='utf-8') as file:
        true_text = file.read().strip()
    return true_text

def process_images(image_folder, bbox_folder):
    """Process all images in a folder and compare detected text with true text."""
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            bbox_file_path = os.path.join(bbox_folder, f"{os.path.splitext(filename)[0]}.bbox")

            print(f"\nProcessing image: {filename}")
            detected_text_easyocr = detect_and_read(image_path)

            if os.path.exists(bbox_file_path):
                true_text = read_true_text(bbox_file_path)
                print(f"True text from file: {true_text}")
                print(f"Easyocr detected text: {detected_text_easyocr}")


if __name__ == '__main__':
    image_folder = 'D:\\hack_data\\train Росатом\\train\\imgs'
    bbox_folder = 'D:\\hack_data\\train Росатом\\train\\labels_with_text'
    process_images(image_folder, bbox_folder)