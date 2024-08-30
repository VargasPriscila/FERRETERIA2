from django.apps import AppConfig


class MiaplicacionConfig(AppConfig):
    """
    Configuración de la aplicación 'miAplicacion'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miAplicacion'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        Importa los signals de la aplicación.
        """
        import miAplicacion.signals