import csv
from loguru import logger
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from src.config import elastic_settings
from src.search.query_builder import QueryBuilder
from src.database.models import SearchLog
from src.llm.llama_normalizer import LlamaNormalizer
from src.llm.gpt_normalizer import GPTNormalizer
from src.llm.abstract_normalizer import Normalizer


def parse_address(row):
    address_city = row.get("Address_City") or ""
    address_street = row.get("Address_Street") or ""

    return ",".join([x for x in [address_city, address_street] if x])


class PeopleSearch:
    def __init__(self, fname, db) -> None:
        self.source_fname = fname
        self.index_name = "people"
        self.db = db

        self.es = Elasticsearch(elastic_settings.ELASTIC_URL)
        self.normalizer: Normalizer = GPTNormalizer(db)
        # self.normalizer: Normalizer = LlamaNormalizer(db)

        self._setup_index()
        if elastic_settings.FORCE_LOAD_DATA:
            data = self._data_parse(self.source_fname)
            self._upload_data_to_elastic(data)

    def _setup_index(self):
        try:
            exists = self.es.indices.exists(index=self.index_name)
            if exists:
                logger.info(f"The index '{self.index_name}' exists.")
            else:
                self._create_index()
                data = self._data_parse(self.source_fname)
                self._upload_data_to_elastic(data)
        except NotFoundError:
            logger.error(
                f"The index '{self.index_name}' does not exist or the cluster is not reachable."
            )

    def _create_index(self):
        mapping = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "name_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "asciifolding"],
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
                    },
                    "address": {"type": "keyword"},
                }
            },
        }

        self.es.indices.create(index=self.index_name, body=mapping)

    def _upload_data_to_elastic(self, data):
        bulk_data = []
        for row in data:
            document = {"index": {"_index": self.index_name}}
            document.update(row)
            bulk_data.append(document)

        if bulk_data:
            res = self.es.bulk(index=self.index_name, body=bulk_data, refresh=True)

    def _data_parse(self, fname: str):
        start_idx = 12745  # 12840
        end_idx = 12880
        data: dict = {}

        with open(fname, newline="", encoding="utf8") as source:
            rows = csv.DictReader(source, delimiter=";")
            for i, row in enumerate(rows):
                if i < start_idx or i > end_idx:
                    continue
                id = row.get("Entity_LogicalId") or ""
                name = row.get("NameAlias_WholeName") or ""
                address = parse_address(row)
                if id not in data:
                    data[id] = {}
                    data[id]["name"] = [name]
                    data[id]["address"] = [address]
                elif name:
                    data[id]["name"].append(name)
                elif address:
                    data[id]["address"].append(address)

        data_arr = []
        for key_id in data:
            rnd_name_alias = data[key_id]["name"][0]
            normalized_name = self.normalizer.normalize(rnd_name_alias)
            data_arr.append(
                {
                    "id": key_id,
                    "name": data[key_id]["name"],
                    "address": data[key_id]["address"],
                    "name_normalized": normalized_name,
                }
            )

        return data_arr

    def search(self, name_search_pattern, address_search_pattern=""):
        normalized_pattern = self.normalizer.normalize(name_search_pattern)
        qb = QueryBuilder(
            name_search_pattern, address_search_pattern, normalized_pattern
        )
        query = qb.get_search_person_query()

        result = self.es.search(index=self.index_name, body=query)
        hits = []

        for hit in result["hits"]["hits"]:
            hits.append(hit["_source"])

        self.db.create_object(
            model_class=SearchLog,
            index=self.index_name,
            name_search_pattern=name_search_pattern,
            address_search_pattern=address_search_pattern,
            n_results=len(hits),
            search_query=query,
            search_result=hits,
        )

        return hits
