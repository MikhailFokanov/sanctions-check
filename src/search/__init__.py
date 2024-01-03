from src.database import get_db
from .people_search import PeopleSearch


db = get_db()
ps = PeopleSearch("20231213-FULL-1_1.csv", db)


def get_search_obj():
    return ps