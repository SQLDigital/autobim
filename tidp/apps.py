from django.apps import AppConfig


class TidpConfig(AppConfig):
    name = 'tidp'

    def ready(self):
        import tidp.signals
