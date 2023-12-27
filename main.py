import sys

from src.gpt_call import gpt_name_normalization
from src.people_search import PeopleSearch

def search_person(keyword):

    normalized = gpt_name_normalization(keyword)

    parts = normalized.split()  # Split the keyword into parts
    should_clauses = []

    print("searching for name and normalized name: " + normalized)

    for part in parts:
        should_clauses.append({
            "match": {
                "name_normalized": {
                    "query": part,
                }
            }
        })

    name_split = keyword.split()
    for part in name_split:
        should_clauses.append({
            "match": {
                "name": {
                    "query": part,
                    "fuzziness": 2
                }
            }
        })

    query = {
        "query": {
            "bool": {
                "should": should_clauses,
                "minimum_should_match": len(parts*2)
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

