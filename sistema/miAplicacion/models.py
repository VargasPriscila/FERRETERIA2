"""
Este módulo define los modelos principales para un sistema de gestión de una ferretería.

El sistema permite gestionar clientes, productos, proveedores, ventas, pedidos y la facturación.
A través de estos modelos, se puede realizar un seguimiento del inventario, registrar las transacciones de venta, gestionar los pedidos a proveedores y emitir facturas.
Los modelos están diseñados para trabajar de manera interconectada, actualizando automáticamente la información relevante, como el stock de productos y el importe total de las ventas.

"""
import uuid
import random
from django.db import models, transaction
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile

@receiver(post_save, sender=User)
def crear_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_cliente(sender, instance, **kwargs):
    instance.cliente.save()


class Cliente(models.Model):
    """
    Modelo que representa un cliente.

    Atributos:
    -----------
    nombre : str
        Nombre del cliente.
    apellido : str
        Apellido del cliente.
    documento : str
        Documento de identidad del cliente.
    direccion : str
        Dirección del cliente.
    telefono : str
        Teléfono del cliente.
    email : EmailField
        Correo electrónico del cliente.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, default=None , related_name='cliente')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200, default='', blank=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(default='', blank=True)

    def __str__(self):
        """
        Devuelve una representación en cadena del cliente.

        Atributos:
        ----------
        nombre : str
            Nombre de la categoría.
        descripcion : TextField
            Descripción de la categoría (opcional).

        """
        return f"{self.nombre} {self.apellido}"




class Categoria(models.Model):
    """
    Modelo que representa una categoría de productos.

    Atributos:
    ----------
    nombre : str
        Nombre de la categoría.
    descripcion : TextField
        Descripción de la categoría (opcional).
    """
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Devuelve una representación en cadena de la categoría.
        """
        return self.nombre




class Proveedor(models.Model):
    """
    Modelo que representa un proveedor de productos.

    Atributos:
    ----------
    nombre : str
        Nombre del proveedor.
    tipo_producto : str
        Tipo de producto que ofrece el proveedor.
    telefono : str
        Número de teléfono del proveedor.
    email : EmailField
        Correo electrónico del proveedor.
    direccion : str
        Dirección física del proveedor.
    """
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100, default='')
    telefono = models.CharField(max_length=15, default='')
    email = models.EmailField(default='', blank=True)
    direccion = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        """
        Devuelve una representación en cadena del proveedor.
        """
        return self.nombre




class MovimientoStock(models.Model):
    """
    Modelo que representa un movimiento de stock (entrada o salida).

    Atributos:
    ----------
    producto : ForeignKey
        Producto relacionado con el movimiento.
    tipo : str
        Tipo de movimiento ('entrada' o 'salida').
    cantidad : int
        Cantidad involucrada en el movimiento.
    fecha : DateTimeField
        Fecha en que se realizó el movimiento.
    comprobante : str
        Comprobante asociado con el movimiento (opcional).
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
        """
        Devuelve una representación en cadena del movimiento de stock.
        """
        return f'{self.tipo} - {self.producto.nombre} - {self.cantidad}'

    def save(self, *args, **kwargs):
        """
        Guarda el movimiento de stock y actualiza el stock del producto.
        """
        super().save(*args, **kwargs)  # Llamar primero al método save original

        if self.tipo == 'entrada':
            self.producto.cantidad_stock += self.cantidad
        self.producto.save()  # Guardar los cambios en el producto




class Pedido(models.Model):
    """
    Modelo que representa un pedido realizado a un proveedor.

    Atributos:
    ----------
    proveedor : ForeignKey
        Proveedor al que se realiza el pedido.
    fecha_pedido : DateTimeField
        Fecha en que se realizó el pedido.
    recibido : bool
        Indica si el pedido ha sido recibido.
    """
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    recibido = models.BooleanField(default=False)

    def __str__(self):
        """
        Devuelve una representación en cadena del pedido.
        """
        return f'Pedido a {self.proveedor} - {self.fecha_pedido}'




class DetallePedido(models.Model):
    """
    Modelo que representa el detalle de un pedido (productos y cantidades).

    Atributos:
    ----------
    pedido : ForeignKey
        Pedido al que pertenece este detalle.
    producto : ForeignKey
        Producto que se incluye en el pedido.
    cantidad : int
        Cantidad de productos solicitados.
    precio_unitario : Decimal
        Precio unitario del producto.
    """

    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        """
        Devuelve una representación en cadena del detalle del pedido.
        """
        return f'{self.producto} - {self.cantidad} unidades'




class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.000)
    cantidad_stock = models.PositiveIntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos/', default='productos/default.png', blank=True, null=True)
    codigo_barras = models.CharField(max_length=50, null=True, blank=True, unique=True)  # Asegúrate de que sea único
    imagen_codigo_barras = models.ImageField(upload_to='codigos_barras/', blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Sobreescribe el método save para generar un código de barras único
        solo si es un nuevo producto y no se proporciona un código de barras.
        """
        if not self.pk and not self.codigo_barras:  # Solo genera el código de barras si es un nuevo producto y no tiene código
            self.codigo_barras = str(uuid.uuid4().int)[:13]  # Genera un código único de 13 dígitos
            self.generar_imagen_codigo_barras()  # Genera la imagen del código de barras

        super().save(*args, **kwargs)

    def generar_imagen_codigo_barras(self):
        """
        Genera la imagen del código de barras y la guarda en el campo imagen_codigo_barras.
        """
        if self.codigo_barras:
            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(self.codigo_barras, writer=ImageWriter())

            buffer = BytesIO()
            ean.write(buffer)

            filename = f"{self.codigo_barras}.png"
            self.imagen_codigo_barras.save(filename, ContentFile(buffer.getvalue()), save=False)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_barras})"




class MedioDePago(models.Model):
    """
    Modelo que representa un medio de pago disponible en el sistema.

    Atributos:
    ----------
    nombre : str
        Tipo de medio de pago (Efectivo, Tarjeta de Crédito, Débito, Transferencia Bancaria, etc.).
    """
    TIPO_PAGO_CHOICES = [
        ('EF', 'Efectivo'),
        ('TC', 'Tarjeta de Crédito'),
        ('TD', 'Tarjeta de Débito'),
        ('TR', 'Transferencia Bancaria'),
    ]  # Puedes agregar más opciones aquí
    nombre = models.CharField(max_length=2, choices=TIPO_PAGO_CHOICES, unique=True)

    def __str__(self):
        """
        Devuelve una representación legible del medio de pago.
        """
        return self.get_nombre_display()




class Venta(models.Model):
    """
    Modelo que representa una venta en el sistema.

    Atributos:
    ----------
    fecha : DateField
        Fecha de la venta.
    numero_comprobante : str
        Número único de comprobante asociado a la venta.
    cliente : ForeignKey
        Cliente que realizó la compra.
    medio_de_pago : ForeignKey
        Medio de pago utilizado en la venta.
    detalle_ventas : ManyToManyField
        Productos comprados a través de la venta.
    importe_total : Decimal
        Importe total de la venta.
    anulada : bool
        Indica si la venta ha sido anulada.
    """
    fecha = models.DateTimeField(default=timezone.now)
    numero_comprobante = models.CharField(max_length=13, unique=True, verbose_name="Número de Comprobante")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None, null=True)
    medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE, default=None, null=True)
    detalle_ventas = models.ManyToManyField(Producto, through="DetalleVenta")
    importe_total = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0.00)
    anulada = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        """
        Devuelve una representación en cadena de la venta.
        """
        return str(self.numero_comprobante)

    def calcular_importe_total(self):
        # Calcular el importe total sumando los importes de los detalles de venta
        total = self.detalleventa_set.aggregate(total_importe=models.Sum('importe'))['total_importe'] or 0
        self.importe_total = total
        self.save(update_fields=['importe_total'])

    @transaction.atomic
    def save(self, *args, **kwargs):
        # Generar número de comprobante si no existe
        if not self.numero_comprobante:
            self.numero_comprobante = self.generar_numero_comprobante()

        super(Venta, self).save(*args, **kwargs)

    @staticmethod
    def generar_numero_comprobante():
        while True:
            numero = str(random.randint(10**12, 10**13 - 1))  # Genera un número de 13 dígitos
            if not Venta.objects.filter(numero_comprobante=numero).exists():  # Verifica que no se repita
                return numero




class DetalleVenta(models.Model):
    """
    Modelo que representa el detalle de una venta (producto, cantidad, precio).

    Atributos:
    ----------
    venta : ForeignKey
        Venta a la que pertenece este detalle.
    producto : ForeignKey
        Producto vendido en este detalle.
    cantidad : int
        Cantidad de productos vendidos.
    precio_unitario : Decimal
        Precio unitario del producto en el momento de la venta.
    importe : Decimal
        Importe total de este detalle (cantidad * precio unitario).
    hora : DateTimeField
        Hora en que se realizó la venta.
    """
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE, default=None, null=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, default=None, null=True)
    cantidad = models.PositiveIntegerField(default=None, null=True)  # Cambiado a PositiveIntegerField
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Campo congelado
    importe = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Devuelve una representación en cadena del detalle de venta.
        """
        venta_str = str(self.venta) if self.venta else "No Venta"
        producto_str = str(self.producto) if self.producto else "No Producto"
        cantidad_str = str(self.cantidad) if self.cantidad is not None else "No Cantidad"
        return f"{venta_str} - {producto_str} - {cantidad_str}"

    def save(self, *args, **kwargs):
        # Si es una nueva instancia, establecer el precio_unitario del producto
        if self.pk is None and self.producto:
            self.precio_unitario = self.producto.precio  # Almacena el precio actual del producto

        # Calcular el importe (cantidad * precio_unitario)
        if self.cantidad and self.precio_unitario:
            self.importe = self.cantidad * self.precio_unitario

        super().save(*args, **kwargs)

        # Actualizar el importe total de la venta
        if self.venta:
            self.venta.calcular_importe_total()
            
            
            
class Consulta(models.Model):
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='consultas')
    productos = models.ManyToManyField(Producto, related_name='consultas')
    mensaje = models.TextField()
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    respuesta = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Consulta de {self.usuario.email} - {self.fecha_consulta}"
            
            
            
            
            
            
            




class Factura(models.Model):
    """
    Modelo que representa una factura generada en el sistema.

    Atributos:
    ----------
    fecha : DateField
        Fecha en la que se generó la factura.
    cliente : ForeignKey
        Cliente asociado a la factura (opcional).
    """
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, default=None, null=True, blank=True)

    @property
    def importe_total(self):
        """
        Calcula el importe total de la factura sumando los precios unitarios por cantidad de los detalles.
        """
        total = self.detalles.aggregate(total=Sum(models.F('precio_unitario') * models.F('cantidad')))['total']
        return total if total is not None else 0




class DetalleFactura(models.Model):
    """
    Modelo que representa el detalle de una factura.

    Atributos:
    ----------
    factura : ForeignKey
        Factura a la que pertenece este detalle.
    producto : ForeignKey
        Producto que aparece en la factura.
    cantidad : int
        Cantidad de productos en el detalle.
    precio_unitario : Decimal
        Precio unitario del producto.
    medio_de_pago : ForeignKey
        Medio de pago utilizado para este detalle.
    """
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, default=None, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        """
        Devuelve una representación en cadena del detalle de la factura.
        """
        return f"{self.cantidad} x {self.producto.nombre} ({self.get_medio_de_pago_display()})"
