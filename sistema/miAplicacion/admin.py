from django.contrib import admin
from .models import Producto, Categoria, Proveedor, MovimientoStock, Pedido, DetallePedido, Venta, DetalleVenta

# Registrar modelos sin configuración personalizada
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(MovimientoStock)
admin.site.register(Pedido)
admin.site.register(DetallePedido)

# Configuración del admin para Producto
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Producto.
    """
    list_display = ('nombre', 'categoria', 'precio_con_simbolo', 'cantidad_stock')
    search_fields = ('nombre',)
    list_filter = ('categoria',)

    def precio_con_simbolo(self, obj):
        """
        Método para mostrar el precio con el símbolo de moneda.
        """
        return f'$ {obj.precio}'
    precio_con_simbolo.short_description = "Precio"

admin.site.register(Producto, ProductoAdmin)

# Configuración del admin para Venta y DetalleVenta
class DetalleVentaInline(admin.TabularInline):
    """
    Configuración inline para DetalleVenta dentro de Venta en el admin.
    """
    model = DetalleVenta
    extra = 1
    readonly_fields = ['subtotal']

class VentaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Venta.
    """
    inlines = [DetalleVentaInline]
    list_display = ['primer_producto', 'fecha_hora', 'total']
    readonly_fields = ['total']

    def primer_producto(self, obj):
        """
        Método para mostrar el primer producto de la venta.
        """
        primer_detalle = obj.detalles.first()
        return primer_detalle.producto.nombre if primer_detalle else 'Sin productos'
    primer_producto.short_description = 'Primer Producto'

    def get_queryset(self, request):
        """
        Método para personalizar el queryset del admin, ordenando por fecha y hora descendente.
        """
        queryset = super().get_queryset(request)
        return queryset.order_by('-fecha_hora')

    def changelist_view(self, request, extra_context=None):
        """
        Método para personalizar la vista de la lista de cambios, agregando el contexto de ventas recientes.
        """
        extra_context = extra_context or {}
        extra_context['ventas'] = Venta.objects.all().order_by('-fecha_hora')[:10]
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Venta, VentaAdmin)
