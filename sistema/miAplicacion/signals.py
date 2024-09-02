from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleVenta

@receiver(post_save, sender=DetalleVenta)
def actualizar_stock_post_venta(sender, instance, created, **kwargs):
    """
    Signal receiver que actualiza el stock del producto cuando se crea un DetalleVenta.

    Args:
        sender (Model): El modelo que envía la señal.
        instance (DetalleVenta): La instancia de DetalleVenta que ha sido guardada.
        created (bool): Un booleano que indica si la instancia fue creada.
        **kwargs: Argumentos adicionales.
    """
    if created:
        instance.actualizar_stock()