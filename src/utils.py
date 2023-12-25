import csv

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
