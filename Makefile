SHELL := /bin/bash

DJANGO_SUPERUSER_NAME ?= admin
DJANGO_SUPERUSER_EMAIL ?= ''
DJANGO_SUPERUSER_PASSWORD ?= admin


ifeq ($(ENV),)
	include .env.dev
	env_file=.env.dev
endif

ifeq ($(ENV),dev)
	include .env.dev
	env_file=.env.dev
endif


docker-makefile:
	docker cp ./Makefile rebbs-django-1:/opt/Makefile

docker-compose:
	cd docker && docker compose --env-file=../${env_file} up -d --build

install-lint:
	poetry run pre-commit install

lint:
	poetry run pre-commit run --all-files

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

superuser: makemigrations migrate
	poetry run python manage.py createsuperuser --username=${DJANGO_SUPERUSER_NAME} --email=${DJANGO_SUPERUSER_EMAIL} --noinput
