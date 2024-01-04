from loguru import logger


class QueryBuilder():
    def __init__(self, name_keyword: str, address_keyword: str, normalized: str) -> None:
        self.name_keyword = name_keyword
        self.address_keyword = address_keyword
        self.normalized = normalized

    def get_search_person_query(self):
        parts = self.normalized.split()  # Split the keyword into parts
        should_clauses = []

        logger.info(f"Searching for name: {self.name_keyword} and normalized name: {self.normalized}")

        for part in parts:
            should_clauses.append({
                "match": {
                    "name_normalized": {
                        "query": part,
                    }
                }
            })

        name_split = self.name_keyword.split()
        for part in name_split:
            should_clauses.append({
                "match": {
                    "name": {
                        "query": part,
                        "fuzziness": 2
                    }
                }
            })
        
        if self.address_keyword:
            should_clauses.append({
                "term": {
                    "address": {
                        "value": self.address_keyword
                    }
                }
            })
        

        query = {
            "query": {
                "bool": {
                    "should": should_clauses,
                    "minimum_should_match": 1 #len(parts*2)
                }
            }
        }

        return query