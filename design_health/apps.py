from django.apps import AppConfig


class DesignHealthConfig(AppConfig):
    name = 'design_health'

    def ready(self):
        import design_health.signals
