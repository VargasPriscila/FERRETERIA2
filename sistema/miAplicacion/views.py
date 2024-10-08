"""
Vistas para la gestión del sistema de hardware.

Este archivo contiene las vistas utilizadas en la aplicación para gestionar los distintos
módulos como proveedores, categorías, productos, ventas y clientes. Las vistas proporcionan
funcionalidad para listar, crear, actualizar, eliminar y gestionar objetos en la base de datos.

Las vistas son:
    - index: Renderiza la página principal.
    - Proveedores: CRUD de proveedores.
    - Categorías: CRUD de categorías.
    - Productos: CRUD de productos.
    - Ventas: Gestión de ventas y detalles de ventas.
    - Clientes: CRUD de clientes.
"""
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Proveedor, Producto, Venta, DetalleVenta, Cliente
from .forms import (CategoriaForm, ProveedorForm, ProductoForm,VentaForm, DetalleVentaForm,ClienteForm)
from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Count




def index(request):
    """
    Renderiza la página principal del sitio.
    """
    return render(request, "index.html")



# ------------------------------ Proveedores -------------------------------------------------

def proveedor_list(request):
    """
    Muestra una lista de todos los proveedores disponibles.

    Args:
        request: El objeto de solicitud HTTP.

    Returns:
        Renderiza la plantilla 'proveedor_list.html' con la lista de proveedores.
    """
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedor_list.html', {'proveedores': proveedores})

def proveedor_create(request):
    """
    Crea un nuevo proveedor. Si se envía una solicitud POST válida,
    se guarda el proveedor en la base de datos.

    Args:
        request: El objeto de solicitud HTTP.

    Returns:
        Renderiza el formulario para crear un proveedor o redirige
        a la lista de proveedores si el formulario es válido.
    """
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/proveedor_form.html', {'form': form})

def proveedor_update(request, pk):
    """
    Actualiza un proveedor existente basado en el identificador proporcionado.

    Args:
        request: El objeto de solicitud HTTP.
        pk: El identificador del proveedor.

    Returns:
        Renderiza el formulario de actualización de proveedor o redirige
        a la lista de proveedores si el formulario es válido.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/proveedor_form.html', {'form': form})

def proveedor_delete(request, pk):
    """
    Elimina un proveedor existente basado en el identificador proporcionado.
    
    Args:
        request: El objeto de solicitud HTTP.
        pk: El identificador del proveedor.
    
    Returns:
        Renderiza una confirmación de eliminación o redirige a la lista 
        de proveedores si se confirma la eliminación.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'proveedores/proveedor_confirm_delete.html', {'proveedor': proveedor})



# ------------------------------ Categorías --------------------------------------------------

def categoria_list(request):
    """
    Muestra una lista de todas las categorías disponibles.
    
    Args:
        request: El objeto de solicitud HTTP.
    
    Returns:
        Renderiza la plantilla 'categoria_list.html' con la lista de categorías.
    """
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categoria_list.html', {'categorias': categorias})

def categoria_create(request):
    """
    Crea una nueva categoría. Si se envía una solicitud POST válida, 
    se guarda la categoría en la base de datos.
    
    Args:
        request: El objeto de solicitud HTTP.
    
    Returns:
        Renderiza el formulario para crear una categoría o redirige a la lista 
        de categorías si el formulario es válido.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/categoria_form.html', {'form': form})

def categoria_update(request, pk):
    """
    Actualiza una categoría existente basada en el identificador proporcionado.
    
    Args:
        request: El objeto de solicitud HTTP.
        pk: El identificador de la categoría.
    
    Returns:
        Renderiza el formulario de actualización de categoría o redirige 
        a la lista de categorías si el formulario es válido.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/categoria_form.html', {'form': form})

def categoria_delete(request, pk):
    """
    Elimina una categoría existente basada en el identificador proporcionado.
    
    Args:
        request: El objeto de solicitud HTTP.
        pk: El identificador de la categoría.
    
    Returns:
        Renderiza una confirmación de eliminación o redirige a la lista de 
        categorías si se confirma la eliminación.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
    return render(request, 'categorias/categoria_confirm_delete.html', {'categoria': categoria})




# ------------------------------ Productos -------------------------------------------------

def productos_list(request):
    """
    Muestra una lista de todos los productos disponibles.
    
    Args:
        request: El objeto de solicitud HTTP.
    
    Returns:
        Renderiza la plantilla 'productos_list.html' con la lista de productos.
    """
    productos = Producto.objects.all()
    return render(request, 'productos/productos_list.html', {'productos': productos})

def productos_create(request):
    """
    Crea un nuevo producto. Si se envía una solicitud POST válida, 
    se guarda el producto en la base de datos.
    
    Args:
        request: El objeto de solicitud HTTP.
    
    Returns:
        Renderiza el formulario para crear un producto o redirige a la lista 
        de productos si el formulario es válido.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/productos_form.html', {'form': form})

def productos_update(request, pk):
    """
    Actualiza un producto existente basado en el identificador proporcionado.
    
    Args:
        request: El objeto de solicitud HTTP.
        pk: El identificador del producto.
    
    Returns:
        Renderiza el formulario de actualización de producto o redirige a la lista 
        de productos si el formulario es válido.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/productos_form.html', {'form': form})

def productos_delete(request, pk):
    """
    Elimina un producto existente basado en el identificador proporcionado.
    
    Args:
        request: El objeto de solicitud HTTP.
        pk: El identificador del producto.
    
    Returns:
        Renderiza una confirmación de eliminación o redirige a la lista de 
        productos si se confirma la eliminación.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos_list')
    return render(request, 'productos/productos_confirm_delete.html', {'producto': producto})




# ------------------------------ Ventas --------------------------------------------------

# Vista para listar ventas
def venta_lista(request):
    """
    Muestra una lista de todas las ventas no anuladas.
    
    Args:
        request: El objeto de solicitud HTTP.
    
    Returns:
        Renderiza la plantilla 'venta_lista.html' con la lista de ventas.
    """
    ventas = Venta.objects.filter(anulada=False).all()
    return render(request, 'ventas/venta_lista.html', {'ventas': ventas})

# Vista para agregar una venta
@transaction.atomic
def venta_agregar(request):
    """
    Crea una nueva venta, incluyendo el detalle de los productos seleccionados.
    
    Args:
        request: El objeto de solicitud HTTP.
    
    Returns:
        Renderiza el formulario para crear una venta o redirige a la lista 
        de ventas si el formulario es válido.
    """
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)

        # Comprobamos si el formulario de venta es válido
        if venta_form.is_valid():
            venta = venta_form.save()  # Guardamos la venta principal

            # Procesamos los productos seleccionados
            productos_ids = request.POST.getlist('producto[]')
            cantidades = request.POST.getlist('cantidad[]')

            # Iteramos sobre los productos seleccionados
            for producto_id, cantidad in zip(productos_ids, cantidades):
                producto = get_object_or_404(Producto, id=producto_id)
                cantidad = int(cantidad)

                # Creamos el detalle de la venta con el precio congelado
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,  # Guardamos el precio actual del producto
                )

            # Redirigimos a la lista de ventas
            return redirect('venta_lista')

    else:
        venta_form = VentaForm()

    return render(request, 'ventas/venta_agregar.html', {
        'venta_form': venta_form,
        'productos': Producto.objects.all()
    })

# Vista para anular una venta
def venta_anular(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.anulada = True
        venta.save()
        # Revertir el stock de los productos
        for detalle in venta.detalleventa_set.all():
            producto = detalle.producto
            producto.cantidad_stock += detalle.cantidad
            producto.save()

        return redirect('venta_lista')

    return render(request, 'ventas/venta_anular.html', {'venta': venta})

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles_venta = DetalleVenta.objects.filter(venta=venta)

    # Obtener la hora del primer detalle (si existe)
    hora_venta = detalles_venta.first().hora if detalles_venta.exists() else None

    context = {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'hora_venta': hora_venta,  # Pasar la hora del primer detalle al contexto
    }
    return render(request, 'ventas/detalle_venta.html', context)

def obtener_precio_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return JsonResponse({'precio': str(producto.precio)})



# ------------------------------ Clientes --------------------------------------------------
# Vista para listar clientes
def cliente_lista(request):
    clientes = Cliente.objects.annotate(compras_recientes=Count('venta'))
    return render(request, 'clientes/cliente_lista.html', {'clientes': clientes})


# Vista para agregar cliente
def cliente_agregar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_lista')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form})

# Vista para editar cliente
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_lista')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form})

# Vista para eliminar cliente
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_lista')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})

# Función para obtener la cantidad de compras realizadas por cliente

def cliente_compras(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    ventas = Venta.objects.filter(cliente=cliente)
    return render(request, 'clientes/cliente_compras.html', {'cliente': cliente, 'ventas': ventas})




# ------------------------------ PAGINACIÓN --------------------------------------------------

class 


