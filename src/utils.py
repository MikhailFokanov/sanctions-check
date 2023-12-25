import csv

def load_data(fname: str):
    data = {}
    with open(fname, newline='', encoding="utf8") as source:
        rows = csv.DictReader(source, delimiter=';')
        for row in rows:
            id = row.get('Entity_LogicalId') or ""
            name = row.get('NameAlias_WholeName') or ""
            if id not in data:
                data[id] = name
            else:
                data[id] = ' '.join([data[id], name])
    data_arr = [{'id': key_id, 'name': data[key_id]} for key_id in data]
    return data_arr
