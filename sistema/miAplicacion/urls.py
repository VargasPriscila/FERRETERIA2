# urls.py
from django.urls import path
from . import views
from .views import obtener_precio_producto

urlpatterns = [
    path('', views.index, name='index'),
    
    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:pk>/', views.categoria_update, name='categoria_update'),
    path('categorias/eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),
    
    # Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nueva/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', views.proveedor_delete, name='proveedor_delete'),
    
    # Productos
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/nueva/', views.productos_create, name='productos_create'),
    path('productos/editar/<int:pk>/', views.productos_update, name='productos_update'),
    path('productos/eliminar/<int:pk>/', views.productos_delete, name='productos_delete'),
    
    # Ventas
    path('ventas/', views.venta_lista, name='venta_lista'),
    path('ventas/agregar/', views.venta_agregar, name='venta_agregar'),
    path('ventas/anular/<int:pk>/', views.venta_anular, name='venta_anular'),
    
    # DetalleVenta
    path('ventas/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    
    # Clientes
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/agregar/', views.cliente_agregar, name='cliente_agregar'),
    path('clientes/editar/<int:pk>/', views.cliente_editar, name='cliente_editar'),
    path('clientes/eliminar/<int:pk>/', views.cliente_eliminar, name='cliente_eliminar'),
    path('clientes/ventas/<int:pk>/', views.cliente_ventas, name='cliente_ventas'),  # Nueva URL

    
    
    
    path('producto/precio/<int:producto_id>/', obtener_precio_producto, name='obtener_precio_producto'),

]
