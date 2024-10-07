# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Proveedor, Producto, Venta, DetalleVenta, Cliente
from .forms import (CategoriaForm, ProveedorForm, ProductoForm,VentaForm, DetalleVentaForm,ClienteForm)
from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Count





def index(request):
    return render(request, "index.html")

# Proveedor
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedor_list.html', {'proveedores': proveedores})

def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/proveedor_form.html', {'form': form})

def proveedor_update(request, pk):
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
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'proveedores/proveedor_confirm_delete.html', {'proveedor': proveedor})

# Categoria
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categoria_list.html', {'categorias': categorias})

def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/categoria_form.html', {'form': form})

def categoria_update(request, pk):
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
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
    return render(request, 'categorias/categoria_confirm_delete.html', {'categoria': categoria})




"""-------------------------------------------------------------------------------------------------------------------------------------------------
"""


def productos_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos_list.html', {'productos': productos})

def productos_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/productos_form.html', {'form': form})

def productos_update(request, pk):
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
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos_list')
    return render(request, 'productos/productos_confirm_delete.html', {'producto': producto})


"""-------------------------------------------------------------------------------------------------------------------------------------------------
"""

# Ventas

# Vista para listar ventas
def venta_lista(request):
    ventas = Venta.objects.filter(anulada=False).all()
    return render(request, 'ventas/venta_lista.html', {'ventas': ventas})

# Vista para agregar una venta
@transaction.atomic
def venta_agregar(request):
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

"""-------------------------------------------------------------------------------------------------------------------------------------------------
"""

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

def cliente_ventas(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    ventas = Venta.objects.filter(cliente=cliente)
    return render(request, 'clientes/cliente_ventas.html', {'cliente': cliente, 'ventas': ventas})
