import csv
from pprint import pprint
from elasticsearch import Elasticsearch


def load_data(fname: str):
    data = []
    with open(fname, newline='') as source:
        rows = csv.DictReader(source, delimiter=';')
        for row in rows:
            last_name   = row.get('NameAlias_LastName') or ""
            first_name  = row.get('NameAlias_FirstName') or ""
            middle_name = row.get('NameAlias_MiddleName') or ""
            if last_name or first_name or middle_name:
                data.append({
                    "last_name": last_name,
                    "first_name": first_name, 
                    "middle_name": middle_name
                })
    return data
                
def upload_data_to_elastic(data):
    es = Elasticsearch("http://localhost:9200")    
    bulk_data = []
    for row in data:
        document = {
            "index": {
                "_index": "names", 
                "_type": "_doc"
            }
        }
        document.update(row)
        bulk_data.append(document)

    if bulk_data:
        res = es.bulk(index="names", body=bulk_data, refresh=True)  # Replace 'your_index_name'

def check_elastic():
    es = Elasticsearch("http://localhost:9200")    
    res = es.search(index='names', body={"query": {"match_all": {}}})  # Replace 'your_index_name'
    print(f"Indexed {res['hits']['total']['value']} documents into Elasticsearch.")


def main():
    #fname = "20231213-FULL-1_1.csv"
    #data = load_data(fname)
    #upload_data_to_elastic(data)
    #check_elastic()
    pass


if __name__ == "__main__":
    main()

