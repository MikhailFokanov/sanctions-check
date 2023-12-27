import csv

from src.gpt_call import gpt_name_normalization

start_idx = 12840
end_idx = 12880

def load_data(fname: str):
    data = {}
    with open(fname, newline='', encoding="utf8") as source:
        rows = csv.DictReader(source, delimiter=';')
        i = -1
        for row in rows:
            i+=1
            id = row.get('Entity_LogicalId') or ""
            name = row.get('NameAlias_WholeName') or ""
            if i not in range(start_idx, end_idx) or name == "":
                continue
            if id not in data:
                data[id] = [ name ]
            elif name:
                data[id].append(name)
    data_arr = []
    for key_id in data:
        normalization = gpt_name_normalization(data[key_id][0])
        data_arr.append({'id': key_id, 'name': data[key_id], 'name_normalized': normalization})
    return data_arr
