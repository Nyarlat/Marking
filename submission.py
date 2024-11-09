import os
import pandas as pd
from app.ml.ocr import ObjectDetector
from app.services.retriever import Retriever


def get_submission_csv(folder_path, output_file='submission.csv'):
    text_recognizer = ObjectDetector(['en'])
    retriever = Retriever()
    data = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            img_name, label_text, label = text_recognizer.detect_and_read(image_path)
            retrieved_label = retriever.retrieve_most_similar_article(label_text)
            data.append({'image_file': img_name, 'label': retrieved_label, 'label_text': label_text})

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, sep=',', encoding='utf-8')


if __name__ == '__main__':
    get_submission_csv('D:\\hack_data\\train Росатом\\train\\imgs')
