import re
from app.dao.db_depends import get_connection


class Retriever:
    def __init__(self, ngrams_count=3):
        self.articles = self._get_all_articles()
        self.ngrams_count = ngrams_count

    def retrieve_most_similar_article(self, recognized_article: str):
        closest_match = None
        highest_overlap = 0

        cleaned_article = self._clean_number(recognized_article)

        article_ngrams = self._generate_ngrams(text=cleaned_article)

        for db_article in self.articles:
            db_article_ngrams = self._generate_ngrams(text=db_article)
            overlap = len(article_ngrams & db_article_ngrams)
            if overlap > highest_overlap:
                highest_overlap = overlap
                closest_match = db_article

        return closest_match

    @staticmethod
    def _get_all_articles():
        with get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT ДетальАртикул FROM components"
            cursor.execute(query)
            results = cursor.fetchall()

        column_data = [row[0] for row in results]
        return column_data

    @staticmethod
    def _clean_number(number):
        cleaned_number = re.sub(r'[^A-Za-zА-Яа-я0-9\s.-]', '', number)
        cleaned_number = re.sub(r'\s+', ' ', cleaned_number).strip()
        return cleaned_number

    def _generate_ngrams(self, text):
        ngrams = []
        text = text.replace(" ", "")
        for i in range(len(text) - self.ngrams_count + 1):
            ngrams.append(text[i:i + self.ngrams_count])
        return set(ngrams)
