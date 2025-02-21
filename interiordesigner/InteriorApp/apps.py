from django.apps import AppConfig


class InteriorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InteriorApp'

    def ready(self):
        from django.template.defaultfilters import register
        from .custom_filters import multiply
        register.filter('multiply', multiply)
