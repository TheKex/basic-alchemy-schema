from os import getenv
from tabulate import tabulate

from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Stock, Sale
from load_test_data import load_data


def get_publisher_sales(session, publisher_name):
    stock_q = session.query(Stock).filter(Stock.book.has(Book.publisher.has(Publisher.name == 'O’Reilly'))).subquery()
    res = []
    query = session.query(Sale).join(stock_q, Sale.id_stock == stock_q.c.id).all()
    for el in query:
        res.append([
            el.stock.book.title,
            el.stock.shop.name,
            el.price,
            el.date_sale.strftime("%Y-%m-%d")
        ])
    return res


if __name__ == '__main__':
    load_dotenv()
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASS')
    db_name = getenv('DB_NAME')

    engine = db.create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}",
                              echo=False)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    load_data(session, 'test_data.json')

    res = get_publisher_sales(session, 'O’Reilly')

    print(tabulate(res, tablefmt="orgtbl"))

    session.close()


