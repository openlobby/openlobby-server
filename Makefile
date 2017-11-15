init-env:
	python3 -m venv .env

install:
	pip install -r requirements.txt

run:
	FLASK_DEBUG=1 FLASK_APP=./openlobby/server.py flask run -p 8010

build:
	docker build -t openlobby/openlobby-server:latest .

push:
	docker push openlobby/openlobby-server:latest

release:
	make build
	make push
