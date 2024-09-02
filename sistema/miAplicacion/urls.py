from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:pk>/', views.categoria_update, name='categoria_update'),
    path('categorias/eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nueva/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', views.proveedor_delete, name='proveedor_delete'),
    
]

