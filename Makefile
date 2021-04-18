.PHONY : install test app schema demo docker-build docker-clean docker-test docker-app docker-schema docker-demo


install:
	pip install -r requirements.txt
	python lemon/manage.py migrate

test:
	pytest -ra

app:
	gunicorn --env DJANGO_SETTINGS_MODULE=lemon.settings lemon.wsgi --bind 0.0.0.0:8000 --workers 2

schema:
	python lemon/manage.py runserver

demo:
	python3 demo.py

docker-build:
	docker-compose build

docker-clean:
	docker-compose down

docker-test:
	docker-compose run lemon bash -c "python3 -m pytest"

docker-app:
	docker-compose up

docker-schema:
	docker-compose run -p 8000:8000 lemon bash -c "lemon/manage.py runserver 0.0.0.0:8000"

docker-demo:
	docker-compose up -d
	sleep 5
	python3 demo.py
