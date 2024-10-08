from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleVenta, MovimientoStock, Producto, Venta


@receiver(post_save, sender=DetalleVenta)
def actualizar_stock_post_venta(sender, instance, created, **kwargs):
    """
    Señal que se dispara después de guardar un DetalleVenta.

    Actualiza el stock del producto asociado al detalle de la venta y
    registra un movimiento de stock en la tabla de MovimientoStock,
    siempre y cuando la venta no esté anulada.

    Parámetros:
    sender (Model): El modelo que envía la señal, en este caso, 'DetalleVenta'.
    instance (DetalleVenta): La instancia de 'DetalleVenta' que ha sido guardada.
    created (bool): Indica si la instancia fue creada (True) o actualizada (False).
    **kwargs: Parámetros adicionales que pueden ser enviados por la señal.

    Lógica:
    - Si la venta no está anulada y el DetalleVenta es nuevo:
        1. Actualiza el stock del producto restando la cantidad vendida.
        2. Crea un registro en MovimientoStock para registrar la salida del producto.
    """
    # Verificamos que el DetalleVenta fue creado y que la venta no está anulada
    if created and instance.venta and not instance.venta.anulada:  # Solo ejecutamos esto si la venta no está anulada
        producto = instance.producto
        cantidad_vendida = instance.cantidad

        # Crear movimiento de stock si no existe uno con el mismo comprobante
        if not MovimientoStock.objects.filter(comprobante=f"Venta {instance.venta.numero_comprobante}", producto=producto).exists():
            MovimientoStock.objects.create(
                producto=producto,
                tipo='salida',
                cantidad=cantidad_vendida,
                comprobante=f"Venta {instance.venta.numero_comprobante}"
            )

        # Actualizar la cantidad en el producto
        producto.cantidad_stock -= cantidad_vendida
        producto.save()

