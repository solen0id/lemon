.PHONY : install test app demo


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
