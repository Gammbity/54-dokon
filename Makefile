run:
	python manage.py runserver

mig:
	python manage.py migrate

gun:
	gunicorn config.wsgi --workers 3

make:
	python manage.py makemigrations

coll:
	python manage.py collectstatic

admin:
	python manage.py createsuperuser

flush:
	python manage.py flush --noinput

shell:
	python manage.py shell

de:
	deactivate

test:
	python manage.py test
