from app.dao.db_depends import get_connection
from app.schemas.component import Component
from app.services.retriever import Retriever
from app.ml.ocr import TextRecognizer

retriever = Retriever()
recognizer = TextRecognizer(['en'])


def process_image(image_path: str) -> Component:
    _, recognized_text, _ = recognizer.detect_and_read(image_path=image_path)
    if recognized_text is not None:
        data = get_information_by_article(article=recognized_text)
        component = Component(**data)
        return component
    else:
        component = Component()
    return component


def get_information_by_article(article: str) -> dict:
    db_article = retriever.retrieve_most_similar_article(recognized_article=article)

    if db_article:
        with get_connection() as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM components WHERE ДетальАртикул = '{db_article}'"
            cursor.execute(query)
            row = cursor.fetchone()

            fields = ["article", "number", "name", "order_number", "station"]
            data = dict(zip(fields, row))
            return data
    else:
        return {}
