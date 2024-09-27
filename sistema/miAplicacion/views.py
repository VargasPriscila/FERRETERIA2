# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Proveedor, Producto, Venta, DetalleVenta
from .forms import (CategoriaForm, ProveedorForm, ProductoForm,VentaForm, DetalleVentaForm,)
from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse




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
    productos = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=productos)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm(instance=productos)
    return render(request, 'productos/productos_form.html', {'form': form})

def productos_delete(request, pk):
    productos = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        productos.delete()
        return redirect('productos_list')
    return render(request, 'productos/productos_confirm_delete.html', {'productos': productos})



"""-------------------------------------------------------------------------------------------------------------------------------------------------
"""

#ventas

# Vista para listar ventas
def venta_lista(request):
    ventas = Venta.objects.filter(anulada=False).all()
    return render(request, 'ventas/venta_lista.html', {'ventas': ventas})

# Vista para agregar una venta
@transaction.atomic
def venta_agregar(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_venta_form = DetalleVentaForm(request.POST)
        if venta_form.is_valid() and detalle_venta_form.is_valid():
            venta = venta_form.save()
            detalle_venta = detalle_venta_form.save(commit=False)
            detalle_venta.venta = venta
            detalle_venta.save()

            # Redirigir a la lista de ventas
            return redirect('venta_lista')
    else:
        venta_form = VentaForm()
        detalle_venta_form = DetalleVentaForm()

    return render(request, 'ventas/venta_agregar.html', {
        'venta_form': venta_form, 
        'detalle_venta_form': detalle_venta_form
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



def obtener_precio_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return JsonResponse({'precio': str(producto.precio)})

