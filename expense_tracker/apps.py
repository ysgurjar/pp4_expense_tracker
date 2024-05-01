from django.apps import AppConfig


class ExpenseTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expense_tracker'

class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        # Register signals here
        from . import signals