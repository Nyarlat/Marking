from app.dao.db_depends import get_connection
from app.schemas.component import Component
from app.services.retriever import Retriever

retriever = Retriever()


def get_random_row():
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM components LIMIT 1"
        cursor.execute(query)
        row = cursor.fetchone()

        fields = ["article", "number", "name", "order_number", "station"]
        data = dict(zip(fields, row))
        component = Component(**data)
        return component


def get_information_by_article(article: str):

    db_article = retriever.retrieve_most_similar_article(recognized_article=article)

    with get_connection() as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM components WHERE ДетальАртикул = '{db_article}'"
        cursor.execute(query)
        row = cursor.fetchone()

        fields = ["article", "number", "name", "order_number", "station"]
        data = dict(zip(fields, row))
        component = Component(**data)
        return component


