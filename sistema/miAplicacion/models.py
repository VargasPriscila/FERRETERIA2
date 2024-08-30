from django.db import models
from django.db.models import Sum, F
from decimal import Decimal


class Categoria(models.Model):
    """
    Modelo que representa una categoría de productos.
    """
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    """
    Modelo que representa un proveedor de productos.
    """
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Modelo que representa un producto en el sistema.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_stock = models.PositiveIntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class MovimientoStock(models.Model):
    """
    Modelo que representa un movimiento de stock (entrada o salida).
    """
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.tipo.Charfield()} - {self.producto.nombre} - {self.cantidad}'

    def save(self, *args, **kwargs):
        if self.tipo == 'entrada':
            self.producto.cantidad_stock = F('cantidad_stock') + self.cantidad
        elif self.tipo == 'salida':
            if self.producto.cantidad_stock < self.cantidad:
                raise ValueError("No hay suficiente stock disponible para esta salida.")
            self.producto.cantidad_stock = F('cantidad_stock') - self.cantidad

        # Guardar los cambios en el producto
        self.producto.save()

        # Llamar al método save original
        super().save(*args, **kwargs)


class Pedido(models.Model):
    """
    Modelo que representa un pedido realizado a un proveedor.
    """
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    recibido = models.BooleanField(default=False)

    def __str__(self):
        return f'Pedido a {self.proveedor.nombre} - {self.fecha_pedido.strftime("%d/%m/%Y %H:%M")}'


class DetallePedido(models.Model):
    """
    Modelo que representa el detalle de un pedido, es decir, los productos y sus cantidades.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades'


class Venta(models.Model):
    """
    Modelo que representa una venta realizada.
    """
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Venta {self.id} - {self.fecha_hora.strftime("%d/%m/%Y %H:%M")}'

    @property
    def total(self):
        """
        Propiedad que calcula el total de la venta sumando los subtotales de sus detalles.
        """
        return self.detalles.aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')


class DetalleVenta(models.Model):
    """
    Modelo que representa el detalle de una venta, es decir, los productos vendidos y sus cantidades.
    """
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calcular el subtotal antes de guardar usando Decimal para precisión
        self.subtotal = Decimal(self.cantidad) * self.precio_unitario

        # Llamar al método save original
        super().save(*args, **kwargs)

        # Actualizar el stock del producto
        self.actualizar_stock()

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    def actualizar_stock(self):
        """
        Método para actualizar el stock del producto después de una venta.
        """
        if self.producto.cantidad_stock < self.cantidad:
            raise ValueError(f"No hay suficiente stock de {self.producto.nombre} para la venta.")
        self.producto.cantidad_stock = F('cantidad_stock') - self.cantidad
        self.producto.save()
