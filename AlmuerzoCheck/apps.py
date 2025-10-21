from django.apps import AppConfig


class AlmuerzocheckConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AlmuerzoCheck'

    def ready(self):
        from AlmuerzoCheck.job import scheduler
        scheduler.start()

