import sys
from src.people_search import PeopleSearch

def search_person(keyword):
    query = {
        "query": {
            "fuzzy": {
                "name": {
                    "value": keyword,
                    "fuzziness": "AUTO"
                }
            } 
        }
    }
    return query


def main():
    ps = PeopleSearch("20231213-FULL-1_1.csv")
    while True:
        search_pattern = input('Input any name part to search: ')
        query = search_person(search_pattern)
        print(f'------------- search result for pattern: {search_pattern} -------------')
        ps.search(query)


if __name__ == "__main__":
    main()

