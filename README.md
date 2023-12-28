# sanctions-check

# Features
- load full names from csv
- upload to elasticsearch
- get normalized name from chatgpt
- provide search of any name by substring

# Local run

## 1. Provide source csv
You have to put csv file with data to the project root. Project will read data from `20231213-FULL-1_1.csv`.

## 2. Setup python dependencies

> Project uses poetry by default.

```bash
# With poetry
poetry shell
poetry install

# With pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure elasticsearch

> Elasticsearch version and python client version sould match

You have to have elasticsearch available on http://localhost:9200. You could use `setup.sh` script to 
setup elasticsearch from scratch with `docker-compose`.

## 4. Configure environment variables
Create `.env` file in the project root with the following content
```dotenv
POSTGRES_USER=sc
POSTGRES_DB=sc
POSTGRES_PASSWORD=123
ELASTIC_URL=http://localhost:9200
OPENAI_API_KEY=sk-123
```

## 5. Start project

Just run: 
```
python main.py
```

You will be able to search any string patterns in cli.

# Tips

To export poetry requirements to requirements.txt you could run
```bash
poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt
```