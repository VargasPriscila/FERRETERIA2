import random
from django.db import models, transaction
from django.db.models import Sum
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200, default='', blank=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(default='', blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Categoria(models.Model):
    """
    Modelo que representa una categoría de productos.
    """
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100, default='')
    telefono = models.CharField(max_length=15, default='')
    email = models.EmailField(default='', blank=True)
    direccion = models.CharField(max_length=200, default='', blank=True)

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

    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    comprobante = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.tipo} - {self.producto.nombre} - {self.cantidad}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Llamar primero al método save original

        if self.tipo == 'entrada':
            self.producto.cantidad_stock += self.cantidad
        elif self.tipo == 'salida':
            self.producto.cantidad_stock -= self.cantidad

        self.producto.save()  # Guardar los cambios en el producto


class Pedido(models.Model):
    """
    Modelo que representa un pedido realizado a un proveedor.
    """
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    recibido = models.BooleanField(default=False)

    def __str__(self):
        return f'Pedido a {self.proveedor} - {self.fecha_pedido}'


class DetallePedido(models.Model):
    """
    Modelo que representa el detalle de un pedido, es decir, los productos y sus cantidades.
    """
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.producto} - {self.cantidad} unidades'


class Producto(models.Model):
    """
    Modelo que representa un producto en el sistema.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cantidad_stock = models.IntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class MedioDePago(models.Model):
    TIPO_PAGO_CHOICES = [
        ('EF', 'Efectivo'),
        ('TC', 'Tarjeta de Crédito'),
        ('TD', 'Tarjeta de Débito'),
        ('TR', 'Transferencia Bancaria'),
    ]  # Puedes agregar más opciones aquí
    nombre = models.CharField(max_length=2, choices=TIPO_PAGO_CHOICES, unique=True)

    def __str__(self):
        return self.get_nombre_display()


class Venta(models.Model):
    fecha = models.DateField(default=timezone.now)
    numero_comprobante = models.CharField(max_length=13, unique=True, verbose_name="Número de Comprobante")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None, null=True)
    medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE, default=None, null=True)
    detalle_ventas = models.ManyToManyField(Producto, through="DetalleVenta")
    importe_total = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.numero_comprobante)

    def calcular_importe_total(self):
        # Calcular el importe total sumando los precios de los productos en los detalles de venta
        total = sum(detalle.cantidad * detalle.producto.precio for detalle in self.detalleventa_set.all())
        self.importe_total = total
        self.save(update_fields=['importe_total'])

    @transaction.atomic
    def save(self, *args, **kwargs):
        # Generar número de comprobante si no existe
        if not self.numero_comprobante:
            self.numero_comprobante = self.generar_numero_comprobante()

        super(Venta, self).save(*args, **kwargs)
        # Nota: la lógica de actualización de stock ahora se maneja completamente en las señales

    @staticmethod
    def generar_numero_comprobante():
        while True:
            numero = str(random.randint(10**12, 10**13 - 1))  # Genera un número de 13 dígitos
            if not Venta.objects.filter(numero_comprobante=numero).exists():  # Verifica que no se repita
                return numero


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, default=None, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=None, null=True)
    cantidad = models.IntegerField(default=None, null=True)

    def __str__(self):
        venta_str = str(self.venta) if self.venta else "No Venta"
        producto_str = str(self.producto) if self.producto else "No Producto"
        cantidad_str = str(self.cantidad) if self.cantidad is not None else "No Cantidad"
        return f"{venta_str} - {producto_str} - {cantidad_str}"

    def save(self, *args, **kwargs):
        # Verificar si es una creación o una actualización
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Actualizar el importe total de la venta después de agregar o actualizar un detalle
        if self.venta:
            self.venta.calcular_importe_total()


class Factura(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, default=None, null=True, blank=True)

    @property
    def importe_total(self):
        total = self.detalles.aggregate(total=Sum(models.F('precio_unitario') * models.F('cantidad')))['total']
        return total if total is not None else 0


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, default=None, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} ({self.get_medio_de_pago_display()})"
