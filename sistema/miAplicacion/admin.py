from django.contrib import admin
from .models import *

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'documento', 'telefono', 'email')
    search_fields = ('nombre', 'apellido', 'documento')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_producto', 'telefono', 'email', 'direccion')
    search_fields = ('nombre', 'tipo_producto')

class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha', 'observaciones')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre',)

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'fecha_pedido', 'recibido')
    list_filter = ('recibido', 'fecha_pedido')
    search_fields = ('proveedor__nombre',)
    inlines = [DetallePedidoInline]

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'cantidad_stock', 'categoria', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('categoria', 'proveedor')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'cantidad_stock')
    
    def precio_con_simbolo(self, obj):
        
        return f'$ {obj.precio}'
    precio_con_simbolo.short_description = "Precio"

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

class VentaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'numero_comprobante', 'cliente', 'medio_de_pago', 'importe_total')
    list_filter = ('fecha', 'medio_de_pago')
    search_fields = ('numero_comprobante', 'cliente__nombre')
    inlines = [DetalleVentaInline]

class MedioDePagoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 1

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'cliente', 'importe_total')
    list_filter = ('fecha', 'cliente')
    search_fields = ('cliente__nombre',)
    inlines = [DetalleFacturaInline]

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(MovimientoStock, MovimientoStockAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(MedioDePago, MedioDePagoAdmin)
admin.site.register(Factura, FacturaAdmin)
