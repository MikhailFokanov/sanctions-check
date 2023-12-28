class QueryBuilder():
    def __init__(self, keyword: str, normalized: str) -> None:
        self.keyword = keyword
        self.normalized = normalized

    def get_search_person_query(self):
        parts = self.normalized.split()  # Split the keyword into parts
        should_clauses = []

        print(f"Searching for name: {self.keyword} and normalized name: {self.normalized}")

        for part in parts:
            should_clauses.append({
                "match": {
                    "name_normalized": {
                        "query": part,
                    }
                }
            })

        name_split = self.keyword.split()
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