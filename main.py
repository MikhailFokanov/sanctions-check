import logging 

from src.people_search import PeopleSearch
from src.database.db import Database
from src.database.models import Base
from src.config import postgres_settings


db = Database(db_url=postgres_settings.db_uri)
ps = PeopleSearch("20231213-FULL-1_1.csv", db, parse_data=False)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def search_pattern():
    pattern = input('Input any name part to search: ')
    print(f'------------- Search results for pattern: {pattern} -------------')
    ps.search(pattern)


def main():
    try:
        db.connect()
        db.create_tables(Base)

        while True:
            search_pattern()
    except Exception as e:
        logging.error(e)
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()

