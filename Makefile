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

createsuperuser: makemigrations migrate
	poetry run python manage.py createsuperuser --username=${DJANGO_SUPERUSER_NAME} --email=${DJANGO_SUPERUSER_EMAIL} --noinput

init: makemigrations migrate create_superuser
	echo "All done."
