from app.dao.db_depends import get_connection
from app.schemas.component import Component


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
