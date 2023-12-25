# sanctions-check

## Local run

You have to put csv file with data to the project root 

1. run setup.sh to setup elasticsearch in docker-compose
2. setup venv with poetry/pip
3. to start project run `python upload.py`

## Plans
- init: Проверяет, есть ли маппинг. Если нет - кладем маппинг.
- 

Entity_EU_ReferenceNumber - id
NameAlias_WholeName - original_name

Произвольный из NameAlias_WholeName приводим к английскому

PUT /people{  "settings": {    "analysis": {      "analyzer": {        "name_analyzer": {          "type": "custom",          "tokenizer": "standard",          "filter": ["lowercase", "asciifolding"]        }      }    }  },  "mappings": {    "properties": {      "name": {        "type": "text",        "analyzer": "name_analyzer",        "fields": {          "keyword": {            "type": "keyword"          }        }      }    }  }}