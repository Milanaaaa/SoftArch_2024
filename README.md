# Anonymous Chat

## ⚙️ Project structure
- `/server` - server side application source code
- `/client.py` - client source code
- `/tests` - tests

## 🚀 Run

### Server
```commandline
docker-compose up 
```

### Client
```commandline
python -m ensurepip --upgrade
pip install requests
python client.py http://localhost:8888
```

## 🧪 Run and debug from sources

### Install requirements
```commandline
python -m ensurepip --upgrade
pip install poetry
poetry install 
```

### Run linter
```commandline
poetry run pylint **/*.py
```

### Run tests
```commandline
poetry run python -m unittest tests.test
```

### Run server
```commandline
poetry run uvicorn main:app forwarded-allow-ips='*' host 0.0.0.0 --port 8000
```