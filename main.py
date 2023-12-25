from src.people_search import PeopleSearch

def search_person(last_name="", first_name="", middle_name=""):
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                      "match_phrase_prefix": {
                        "last_name": {
                          "query": last_name
                        }
                      }
                    },
                    {
                      "match_phrase_prefix": {
                        "first_name": {
                          "query": first_name
                        }
                      }
                    },
                    {
                      "match_phrase_prefix": {
                        "middle_name": {
                          "query": middle_name
                        }
                      }
                    },
                ]
            }
        }
    }
    return query

def main():
    ps = PeopleSearch("20231213-FULL-1_1.csv")


if __name__ == "__main__":
    main()

