from django.apps import AppConfig


class IncubacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'incubacao'

    def ready(self):
        from incubacao.tasks import verificar_lotes_task
        verificar_lotes_task(repeat=3600) 
        import incubacao.signals
