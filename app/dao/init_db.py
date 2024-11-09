import pandas as pd
from sqlalchemy import create_engine
from config import settings


def init_db():
    df = pd.read_excel('app/data/orders.xlsx')
    df = df.apply(lambda x: x.str.replace('"', '', regex=True) if x.dtype == "object" else x)
    engine = create_engine(settings.PG_URL)
    df.to_sql('components', engine, if_exists='replace', index=False)


init_db()