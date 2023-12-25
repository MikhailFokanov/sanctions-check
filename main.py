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
    query = search_person('Sultan')
    ps.search(query)


if __name__ == "__main__":
    main()

