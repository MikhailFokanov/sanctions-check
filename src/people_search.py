import csv
import logging
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from src.config import elastic_settings
from src.query_builder import QueryBuilder
from src.database.models import SearchLog, GPTResponse
from src.gpt_call import GPTNormalizer


class PeopleSearch():
    def __init__(self, fname, db, parse_data=False) -> None:
        self.source_fname = fname
        self.index_name = "people"
        self.db = db

        self.es = Elasticsearch(elastic_settings.ELASTIC_URL)
        self.gpt_normalizer = GPTNormalizer(db)

        self._setup_index()
        if parse_data:
            data = self._data_parse(self.source_fname)
            self._upload_data_to_elastic(data)


    def _setup_index(self):
        try:
            exists = self.es.indices.exists(index=self.index_name)
            if exists:
                logging.info(f"The index '{self.index_name}' exists.")
            else:
                self._create_index()
        except NotFoundError:
            logging.error(
                f"The index '{self.index_name}' does not exist or the cluster is not reachable.")

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
                    "name_normalized": {
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
            res = self.es.bulk(index=self.index_name, body=bulk_data,
                               refresh=True)

    def _data_parse(self, fname: str):
        start_idx = 12840
        end_idx = 12880
        data = {}

        with open(fname, newline='', encoding="utf8") as source:
            rows = csv.DictReader(source, delimiter=';')
            for i, row in enumerate(rows):
                if start_idx <= i <= end_idx or name == "":
                    continue
                id = row.get('Entity_LogicalId') or ""
                name = row.get('NameAlias_WholeName') or ""
                if id not in data:
                    data[id] = [ name ]
                elif name:
                    data[id].append(name)

        data_arr = []
        for key_id in data:
            normalized_name = self.gpt_normalizer.gpt_name_normalize(data[key_id][0])
            data_arr.append({'id': key_id, 'name': data[key_id], 'name_normalized': normalized_name})

        return data_arr

    def search(self, search_pattern):
        normalized_pattern = self.gpt_normalizer.gpt_name_normalize(search_pattern)
        qb = QueryBuilder(search_pattern, normalized_pattern)
        query = qb.get_search_person_query()

        result = self.es.search(index=self.index_name, body=query)
        hits = []

        for hit in result['hits']['hits']:
            print(hit['_source'])
            hits.append(hit['_source'])
        
        self.db.create_object(model_class=SearchLog, 
                              index=self.index_name,
                              search_query=query, 
                              search_result=hits)
