init-env:
	python3 -m venv .env

install:
	pip install --upgrade -r requirements.txt -r test-requirements.txt
	pip install -e .

run:
	DEBUG=1 python manage.py runserver 8010

migrate:
	DEBUG=1 python manage.py migrate
	DEBUG=1 python manage.py search_index --rebuild -f

build:
	docker build -t openlobby/openlobby-server:latest .

push:
	docker push openlobby/openlobby-server:latest

release:
	make build
	make push
