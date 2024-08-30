import os
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from miAplicacion.models import Categoria, Proveedor

# Crear categorías
categorias_nombres = [
    "Herramientas Manuales",
    "Herramientas Eléctricas",
    "Equipos de Seguridad",
    "Materiales de Construcción",
    "Pinturas y Acabados",
    "Fontanería",
    "Electricidad",
    "Jardinería",
    "Adhesivos y Selladores",
    "Ferretería General"
]

for nombre in categorias_nombres:
    Categoria.objects.get_or_create(nombre=nombre)

print("Categorías creadas.")

# Crear proveedores
proveedores_nombres = [
    "Proveedor A",
    "Proveedor B",
    "Proveedor C",
    "Proveedor D",
    "Proveedor E"
]

for nombre in proveedores_nombres:
    Proveedor.objects.get_or_create(nombre=nombre)

print("Proveedores creados.")
