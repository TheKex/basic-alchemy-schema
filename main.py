from os import getenv
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import NamedTupleCursor


if __name__ == '__main__':
    load_dotenv()
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASS')

    with psycopg2.connect(dbname='postgres', user=db_user, password=db_pass, host=db_host, port=db_port) as conn:
        pass



    conn.close()
