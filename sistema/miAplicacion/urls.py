# urls.py
from django.urls import include, path
from . import views
from .views import obtener_precio_producto
from .views import clienteCompras
from .views import ProductosListView
from .views import VentaListView
from .views import panel_administracion
from .views import enviar_consulta, responder_consulta, lista_consultas
from .views import obtener_producto_por_codigo
from .views import admin_login
from django.contrib.auth import views as auth_views
from allauth.account.views import signup as allauth_signup

urlpatterns = [
    
    path('', views.index, name='index'),
    
    path('account/', include('allauth.urls')),

    #Administración
    path('panel/', panel_administracion, name='panel_administracion'), 
    path('admin/login/', admin_login, name='admin_login'),
    
    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/agrear/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:pk>/', views.categoria_update, name='categoria_update'),
    path('categorias/eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),

    # Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/agregar/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', views.proveedor_delete, name='proveedor_delete'),
    path('proveedores/<int:proveedor_id>/', views.proveedor_productos, name='proveedor_productos'),

    # Productos
# productos_list es una Class NO un def por eso esta diferente de las demas funciones que tiene Productos
    path('productos/', ProductosListView.as_view(), name='productos_list'),
    
    path('productos/agregar/', views.productos_create, name='productos_create'),
    path('productos/editar/<int:pk>/', views.productos_update, name='productos_update'),
    path('productos/eliminar/<int:pk>/', views.productos_confirm_delete, name='productos_confirm_delete'),

    # Ventas
    path('ventas/', VentaListView.as_view(), name='venta_lista'),
    #path('ventas/agregar/', views.venta_agregar, name='venta_agregar'),
    path('ventas/anular/<int:pk>/', views.venta_anular, name='venta_anular'),
    path('ventas/agregar/', views.agregar_venta, name='venta_agregar'),

    # DetalleVenta
    path('ventas/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    
    # Clientes
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/agregar/', views.cliente_agregar, name='cliente_agregar'),
    path('clientes/editar/<int:pk>/', views.cliente_editar, name='cliente_editar'),
    path('clientes/eliminar/<int:pk>/', views.cliente_eliminar, name='cliente_eliminar'),
    path('clientes/compras/<int:pk>/', clienteCompras.as_view(), name='cliente_compras'),

    
    # Consultas
    path('consultas/', lista_consultas, name='lista_consultas'),
    path('consultas/enviar/', enviar_consulta, name='enviar_consulta'),
    path('consultas/responder/<int:consulta_id>/', responder_consulta, name='responder_consulta'),
    


    path('obtener_precio/', views.obtener_precio_producto, name='obtener_precio_producto'),

    #Codigo de barras
    path('obtener_producto/', obtener_producto_por_codigo, name='obtener_producto'),
]
