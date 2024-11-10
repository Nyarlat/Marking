import os
import pandas as pd
from app.ml.ocr import TextRecognizer
from app.ml.pocr import ImageProcessor
from app.services.retriever import Retriever
from app.services.utils import replace_latin_with_cyrillic

def get_submission_csv(folder_path, output_file='submission.csv'):
    # text_recognizer = TextRecognizer(['en'])
    image_proc = ImageProcessor()
    retriever = Retriever(ngrams_count=3)
    data = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.JPG')):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            img_name, label_text, label = image_proc .detect_and_read(image_path)
            replaced_text = replace_latin_with_cyrillic(label_text)
            retrieved_label = retriever.retrieve_most_similar_article(replaced_text)
            data.append({'image_file': img_name, 'label': label, 'label_text': f'"{retrieved_label}"'})

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, sep=',', encoding='utf-8')


if __name__ == '__main__':
    get_submission_csv('D:\\hack_data\\test Росатом\\test\\imgs')
    # get_submission_csv('D:\\hack_data\\train Росатом\\train\\imgs', 'app\\ml\\metrics\\submission.csv')
