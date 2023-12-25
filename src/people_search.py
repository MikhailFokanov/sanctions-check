from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from src.utils import load_data


class PeopleSearch():
    def __init__(self, fname) -> None:
        self.source_fname = fname 
        self.index_name = "people"
        self.es = Elasticsearch("http://localhost:9200")        
        self._setup_index()

    def _setup_index(self):
        try:
            exists = self.es.indices.exists(index=self.index_name)
            if exists:
                print(f"The index '{self.index_name}' exists.")
            else:
                self._create_index()
                self._load_data()
        except NotFoundError:
            print(f"The index '{self.index_name}' does not exist or the cluster is not reachable.")
    
    def _load_data(self):
        data = load_data(self.source_fname)     
        self._upload_data_to_elastic(data)

    def _create_index(self):
        mapping = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "name_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "asciifolding"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "analyzer": "name_analyzer",
                    },
                    "name_original": {
                        "type": "text",
                        "analyzer": "name_analyzer",
                    }
                }
            }
        }

        self.es.indices.create(index=self.index_name, body=mapping)

    def _upload_data_to_elastic(self, data):
        bulk_data = []
        for row in data:
            document = {
                "index": {
                    "_index": self.index_name
                }
            }
            document.update(row)
            bulk_data.append(document)

        if bulk_data:
            res = self.es.bulk(index=self.index_name, body=bulk_data, refresh=True)  
    
    def search(self, query):
        result = self.es.search(index=self.index_name, body=query)

        for hit in result['hits']['hits']:
            print(hit['_source'])