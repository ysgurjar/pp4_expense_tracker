"""
This Django module configures app settings for an expense tracker and a generic
application within a project.The `ExpenseTrackerConfig` class sets up
configurations specific to an expense tracking application,including using a
`BigAutoField` for the default auto-generated primary key field type.The
`MyAppConfig` class configures settings for a general application and includes
methods to register signals upon app readiness.

Attributes:
    ExpenseTrackerConfig (AppConfig): Configuration class for the expense
    tracker application.
    MyAppConfig (AppConfig): Configuration class for a generic application
    within the project.
"""

from django.apps import AppConfig


class ExpenseTrackerConfig(AppConfig):
    """
    Configuration class for the expense tracker application within a Django
    project.
    This class specifies a custom primary key field type and the application
    name which Django uses to handle application-specific configurations.
    Attributes:
        default_auto_field (str): Specifies the field type to use for
        auto-generated primary key fields,set to django.db.models.BigAutoField
        name (str): Defines the application name used within Django's project
        settings.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "expense_tracker"
