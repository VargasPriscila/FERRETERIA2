"""
Registro y configuración de modelos en el panel de administración de Django.

Esta clase contiene la configuración para administrar varios modelos relacionados con el inventario, proveedores, ventas y clientes dentro de la aplicación.

Cada modelo tiene configuraciones personalizadas para:

- `list_display`: Define las columnas que se mostrarán en la lista de cada modelo.
- `search_fields`: Define los campos por los que se puede buscar en cada modelo.
- `list_filter`: Define los filtros aplicables en cada modelo.
- `readonly_fields`: Campos que son de solo lectura en el panel de administración.
- `inlines`: Para algunos modelos, como `Pedido` y `Venta`, se incluyen vistas en línea de detalles relacionados.
"""
from django.contrib import admin
from .models import *
from django.utils.html import format_html



class ClienteAdmin(admin.ModelAdmin):
    """
    Administra la vista de los clientes en el panel de administración.

    list_display: Define las columnas que se mostrarán en la lista de clientes.
    search_fields: Permite buscar clientes por nombre, apellido o documento.
    """
    list_display = ('nombre', 'apellido', 'documento', 'telefono', 'email')
    search_fields = ('nombre', 'apellido', 'documento')




class CategoriaAdmin(admin.ModelAdmin):
    """
    Administra la vista de las categorías en el panel de administración.

    list_display: Muestra las columnas del nombre y descripción de las categorías.
    search_fields: Permite buscar categorías por nombre.
    """
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)




class ProveedorAdmin(admin.ModelAdmin):
    """
    Administra la vista de los proveedores en el panel de administración.

    list_display: Muestra las columnas con el nombre, tipo de producto, teléfono, email y dirección del proveedor.
    search_fields: Permite buscar proveedores por nombre o tipo de producto.
    """
    list_display = ('nombre', 'tipo_producto', 'telefono', 'email', 'direccion')
    search_fields = ('nombre', 'tipo_producto')




class MovimientoStockAdmin(admin.ModelAdmin):
    """
    Administra los movimientos de stock en el panel de administración.

    list_display: Muestra las columnas del producto, tipo de movimiento, cantidad, fecha y comprobante.
    list_filter: Filtra los movimientos por tipo y fecha.
    search_fields: Permite buscar movimientos por nombre del producto.
    """
    list_display = ('producto', 'tipo', 'cantidad', 'fecha', 'comprobante')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre',)




class DetallePedidoInline(admin.TabularInline):
    """
    Define la interfaz inline para los detalles de pedidos dentro del admin de pedidos.

    model: Modelo relacionado con los detalles del pedido.
    extra: Número de registros adicionales para agregar en la interfaz.
    """
    model = DetallePedido
    extra = 1




class PedidoAdmin(admin.ModelAdmin):

    """
    Administra los pedidos en el panel de administración.

    list_display: Muestra las columnas del proveedor, fecha del pedido y si ha sido recibido.
    list_filter: Filtra los pedidos por si han sido recibidos o por fecha.
    search_fields: Permite buscar pedidos por nombre del proveedor.
    inlines: Integra los detalles del pedido en el formulario.
    """
    list_display = ('proveedor', 'fecha_pedido', 'recibido')
    list_filter = ('recibido', 'fecha_pedido')
    search_fields = ('proveedor_nombre',)
    inlines = [DetallePedidoInline]




class ProductoAdmin(admin.ModelAdmin):
    """
    Administra los productos en el panel de administración.
    list_display: Muestra las columnas del nombre, descripción, precio, cantidad en stock, categoría, fecha de creación y actualización.
    list_filter: Filtra los productos por categoría y proveedor.
    search_fields: Permite buscar productos por nombre o descripción.
    list_editable: Define qué campos pueden ser editables directamente desde la lista de productos.
    """
    list_display = ('nombre', 'descripcion', 'precio', 'cantidad_stock', 'categoria', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('categoria', 'proveedor')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'cantidad_stock')

    def precio_con_simbolo(self, obj):
        """
        Devuelve el precio del producto formateado con un símbolo de peso.

        Parámetros:
        obj : Producto
            Instancia del producto.

        Retorna:
        str
            Precio formateado con símbolo de peso.
        """
        return f'$ {obj.precio}'
    precio_con_simbolo.short_description = "Precio"




class DetalleVentaInline(admin.TabularInline):
    """
    Define la interfaz inline para los detalles de ventas dentro del admin de ventas.

    model: Modelo relacionado con los detalles de la venta.
    extra: Número de registros adicionales para agregar en la interfaz.
    fields: Campos que se muestran para cada detalle.
    readonly_fields: Campos que son de solo lectura.
    """
    model = DetalleVenta
    extra = 1
    fields = ['producto', 'precio_unitario', 'cantidad', 'importe',]
    readonly_fields = ['precio_unitario', 'importe']

    def precio_unitario(self, obj):
        """
        Devuelve el precio unitario del producto en una venta.

        Parámetros:
        obj : DetalleVenta
            Instancia del detalle de venta.

        Retorna:
        str
            Precio unitario del producto formateado.
        """
        if obj.producto:
            return format_html(f'<span>$ {obj.producto.precio}</span>')
        return "-"

    precio_unitario.short_description = "Precio Unitario"

    def calcular_total(self):
        """
        Calcula el total de la venta multiplicando la cantidad por el precio unitario.

        Retorna:
        float
            Importe total de la venta.
        """
        return self.cantidad * self.precio_unitario

    class Media:
        """
        Define recursos de JavaScript adicionales que se utilizarán en el formulario de ventas.
        """
        js = ('static/js/detalle_venta.js',)




class VentaAdmin(admin.ModelAdmin):
    """
    Administra las ventas en el panel de administración.

    list_display: Muestra las columnas de la fecha, número de comprobante, cliente, medio de pago e importe total.
    readonly_fields: Define los campos que son de solo lectura.
    inlines: Integra los detalles de la venta en el formulario.
    """
    list_display = ('fecha', 'numero_comprobante', 'cliente', 'medio_de_pago', 'importe_total')
    readonly_fields = ['numero_comprobante', 'importe_total']
    inlines = [DetalleVentaInline]




class MedioDePagoAdmin(admin.ModelAdmin):
    """
    Administra los medios de pago en el panel de administración.

    list_display: Muestra las columnas con el nombre del medio de pago.
    search_fields: Permite buscar medios de pago por nombre.
    """
    list_display = ('nombre',)
    search_fields = ('nombre',)




class DetalleFacturaInline(admin.TabularInline):
    """
    Define la interfaz inline para los detalles de facturas dentro del admin de facturas.

    model: Modelo relacionado con los detalles de la factura.
    extra: Número de registros adicionales para agregar en la interfaz.
    """
    model = DetalleFactura
    extra = 1




class FacturaAdmin(admin.ModelAdmin):
    """
    Administra las facturas en el panel de administración.

    list_display: Muestra las columnas de la fecha, cliente e importe total.
    list_filter: Filtra las facturas por fecha o cliente.
    search_fields: Permite buscar facturas por nombre del cliente.
    inlines: Integra los detalles de la factura en el formulario.
    """
    list_display = ('fecha', 'cliente', 'importe_total')
    list_filter = ('fecha', 'cliente')
    search_fields = ('cliente__nombre',)
    inlines = [DetalleFacturaInline]



# Registro de modelos en el panel de administración de Django.
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(MovimientoStock, MovimientoStockAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(MedioDePago, MedioDePagoAdmin)
admin.site.register(Factura, FacturaAdmin)