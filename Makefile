init-env:
	python3 -m venv .env

install:
	pip install -r requirements.txt

test:
	pytest

run:
	FLASK_DEBUG=1 FLASK_APP=./src/server.py flask run -p 8010

build:
	docker build -t openlobby/openlobby-server:latest .

push:
	docker push openlobby/openlobby-server:latest
