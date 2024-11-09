import os
import pandas as pd
from ocr import detect_and_read


def get_submission_csv(folder_path, output_file='submission.csv'):
    data = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            img_name, label_text, label = detect_and_read(image_path)
            data.append({'image_file': img_name, 'label': label, 'label_text': label_text})

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, sep=',', encoding='utf-8')


if __name__ == '__main__':
    get_submission_csv('D:\\hack_data\\train Росатом\\train\\imgs')
