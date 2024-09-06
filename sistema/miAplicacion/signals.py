from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleVenta, MovimientoStock

@receiver(post_save, sender=DetalleVenta)
def actualizar_stock_post_venta(sender, instance, created, **kwargs):
    if created:  # Solo ejecutamos esto cuando se crea un DetalleVenta
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
