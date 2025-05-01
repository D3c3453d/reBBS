from django.apps import AppConfig


class DbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "db"
    name = "src.db"
    verbose_name = "DB"
