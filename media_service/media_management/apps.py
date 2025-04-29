from django.apps import AppConfig


class MediaManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media_management'

    def ready(self):
        import media_management.signals

