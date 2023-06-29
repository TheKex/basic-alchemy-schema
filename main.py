from os import getenv
from dotenv import load_dotenv

from models import create_tables
from load_test_data import load_data

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker



if __name__ == '__main__':
    load_dotenv()
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASS')

    db_name = 'postgres'
    engine = db.create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}",
                              echo=True)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    load_data(session, 'test_data.json')



    session.close()


