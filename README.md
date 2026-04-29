# reBBS

## Quick start
1. Установить [docker](https://www.docker.com)
2. Установить [pipx](https://pipx.pypa.io/stable/installation/)
3. `pipx install poetry` - ставит poetry
4. `poetry install` - создаёт окружение и ставит все нужные пакеты
5. `poetry run pre-commit install` - ставит линтеры
6. `make docker-compose` - билдит и поднимает контейнеры
7. `make superuser` - создаёт супер-пользователя
