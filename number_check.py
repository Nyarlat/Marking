import re
import sqlite3
from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance
import pandas as pd


#очистка строки
def clean_number(number):
    cleaned_number = re.sub(r'[^A-Za-zА-Яа-я0-9\s.-]', '', number)
    cleaned_number = re.sub(r'\s+', ' ', cleaned_number).strip()
    return cleaned_number


#получение информации из столбца
def get_article(db_path, table_name, column_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    column_data = [row[0] for row in results]
    return column_data


#алгоримт SequenceMatcher
def find_most_similar_number(cleaned_number, database_numbers):
    closest_match = None
    highest_similarity = 0

    for db_number in database_numbers:
        similarity = SequenceMatcher(None, cleaned_number, db_number).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_match = db_number

    return closest_match, highest_similarity


#вычисление расстояния Левенштейна
def find_most_similar_number_levenshtein(cleaned_number, database_numbers):
    closest_match = None
    lowest_distance = float('inf')

    for db_number in database_numbers:
        distance = levenshtein_distance(cleaned_number, db_number)
        if distance < lowest_distance:
            lowest_distance = distance
            closest_match = db_number

    return closest_match, lowest_distance


#метод n-грамм
def generate_ngrams(text, n):
    ngrams = []
    text = text.replace(" ", "")
    for i in range(len(text) - n + 1):
        ngrams.append(text[i:i + n])
    return set(ngrams)


def find_most_similar_number_ngrams(cleaned_number, database_numbers, n=3):
    closest_match = None
    highest_overlap = 0

    cleaned_number_ngrams = generate_ngrams(cleaned_number, n)

    for db_number in database_numbers:
        db_number_ngrams = generate_ngrams(db_number, n)
        overlap = len(cleaned_number_ngrams & db_number_ngrams)
        if overlap > highest_overlap:
            highest_overlap = overlap
            closest_match = db_number

    return closest_match, highest_overlap


def extract_texts_to_lists(file_path):
    true_texts = []
    easyocr_texts = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("True text from file:"):
                true_text = re.search(r'"(.*?)"', line)
                if true_text:
                    true_texts.append(true_text.group(1))
            elif line.startswith("Easyocr detected text:"):
                easyocr_text = line.split("Easyocr detected text: ")[1].strip()
                easyocr_texts.append(easyocr_text)

    return true_texts, easyocr_texts


true_texts, easyocr_texts = extract_texts_to_lists('extracted_texts.txt')
easyocr_texts = list(map(clean_number, easyocr_texts))


db_path = 'rosatom.db'
table_name = 'components'
column_name = 'ДетальАртикул'

data = get_article(db_path, table_name, column_name)
model_res = "0 Us 0 49s-39 0"
model_res = clean_number(model_res)


best_match1, similarity1 = find_most_similar_number(model_res, data)
best_match2, similarity2 = find_most_similar_number_levenshtein(model_res, data)
best_match3, similarity3 = find_most_similar_number_ngrams(model_res, data, n=3)

print("Результат модели:", model_res)
print("SequenceMatcher:", best_match1)
print("Левенштейн:", best_match2)
print("N-gram:", best_match3)

'''results1 = list(map(lambda x: find_most_similar_number_ngrams(x, data, n=3), easyocr_texts))
results1 = list(map(lambda x: x[0], results1))

results2 = list(map(lambda x: find_most_similar_number(x, data), easyocr_texts))
results2 = list(map(lambda x: x[0], results2))

results3 = list(map(lambda x: find_most_similar_number_levenshtein(x, data), easyocr_texts))
results3 = list(map(lambda x: x[0], results3))

count_matches1 = sum(1 for i, j in zip(results1, true_texts) if i == j)
count_matches2 = sum(1 for i, j in zip(results2, true_texts) if i == j)
count_matches3 = sum(1 for i, j in zip(results3, true_texts) if i == j)

print(count_matches1)
print(count_matches2)
print(count_matches3)



data = {
    'true_text': true_texts,
    'ngram': results1,
    'ocr_res': easyocr_texts
}

df = pd.DataFrame(data)
df.to_excel('compare.xlsx', index=False)'''