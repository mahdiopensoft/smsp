from django.apps import AppConfig

class ExamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exams'

    def ready(self):
        from config.security_hardening import apply_security_hardening
        apply_security_hardening()
