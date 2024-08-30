import os
import django
import random
from datetime import datetime

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from miAplicacion.models import Producto, Categoria, Proveedor

# Asegúrate de tener algunas categorías y proveedores en tu base de datos
categorias = Categoria.objects.all()
proveedores = Proveedor.objects.all()

if not categorias.exists() or not proveedores.exists():
    print("Por favor, agrega algunas categorías y proveedores antes de ejecutar este script.")
    exit()

# Lista de nombres de productos
nombres_productos = [
    "Martillo", "Taladro", "Sierra", "Destornillador", "Llave Inglesa", "Alicate", "Cinta Métrica", "Nivel", "Lijadora",
    "Pistola de Calor", "Soplete", "Cúter", "Escalera", "Serrucho", "Broca", "Mazo", "Cincel", "Compresor de Aire",
    "Gato Hidráulico", "Cepillo de Carpintero", "Llave Allen", "Soldador", "Desarmador de Impacto", "Mordaza",
    "Regla", "Metro", "Cinta Aislante", "Clavos", "Tornillos", "Tuercas", "Arandelas", "Anillos de Retención",
    "Pasadores", "Remaches", "Tapones", "Tacos de Expansión", "Grapas", "Cadenas", "Eslingas", "Poleas",
    "Rodamientos", "Ruedas", "Ejes", "Puntas", "Discos de Corte", "Limas", "Brocha", "Pincel", "Masilla"
]

# Lista para almacenar los productos a crear
productos = []

# Creación de 50 productos con datos aleatorios
for i in range(50):
    producto = Producto(
        nombre=random.choice(nombres_productos),
        descripcion="Descripción del producto " + str(i+1),
        precio=round(random.uniform(10.0, 500.0), 2),
        cantidad_stock=random.randint(1, 100),
        categoria=random.choice(categorias),
        proveedor=random.choice(proveedores)
    )
    productos.append(producto)

# Guardar los productos en la base de datos usando bulk_create
Producto.objects.bulk_create(productos)
print("50 productos agregados exitosamente.")
