from django.apps import AppConfig


class IncubacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'incubacao'

    def ready(self):
        import incubacao.signals
