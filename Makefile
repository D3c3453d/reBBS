SHELL := /bin/bash


ifeq ($(ENV),)
	include .env.dev
	env_file=.env.dev
endif

ifeq ($(ENV),dev)
	include .env.dev
	env_file=.env.dev
endif


DJANGO_SUPERUSER_NAME ?= admin
DJANGO_SUPERUSER_EMAIL ?= ''
DJANGO_SUPERUSER_PASSWORD ?= admin


docker-sync:
	docker cp ./Makefile rebbs-django-1:/opt/Makefile
	docker cp ./.env.dev rebbs-django-1:/opt/.env.dev

docker-compose:
	cd docker && docker compose --env-file=../${env_file} up -d --build

lint:
	poetry run pre-commit run --all-files

makemigrations:
	docker exec -it rebbs-django-1 sh -c "poetry run python manage.py makemigrations"

migrate:
	docker exec -it rebbs-django-1 sh -c "poetry run python manage.py migrate"

superuser: makemigrations migrate
	docker exec -it rebbs-django-1 sh -c "poetry run python manage.py createsuperuser --username=${DJANGO_SUPERUSER_NAME} --email=${DJANGO_SUPERUSER_EMAIL} --noinput"

static:
	docker exec -it rebbs-django-1 sh -c "poetry run python manage.py collectstatic --noinput"
	docker restart rebbs-django-1

test:
	docker exec -it rebbs-django-1 sh -c "poetry run pytest --ds=src.settings tests"
