from django.apps import AppConfig


class AssessmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.assessment'
    
    def ready(self):
        # Import signals to register them
        import apps.assessment.signals
