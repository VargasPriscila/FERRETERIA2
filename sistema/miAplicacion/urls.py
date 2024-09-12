# urls.py
from django.urls import path
from . import views

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
]
