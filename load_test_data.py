import json
from os import getenv

from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

from pprint import pprint


def load_data(session, json_path):
    with open(json_path, 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()


if __name__ == '__main__':
    load_dotenv()
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASS')

    db_name = 'postgres'
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}", echo=True)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    load_data(session, 'test_data.json')
    # session.commit()
