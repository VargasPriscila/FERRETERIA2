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
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator






def index(request):
    """
    Renderiza la página principal del sitio.
    """
    return render(request, "index.html")



# ------------------------------ Proveedores -------------------------------------------------
@login_required #Agregar esta linea para asegurar que sea visible el template si el usuario se logueo.
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
@login_required
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

@login_required
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

@login_required
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

@login_required
def proveedor_productos(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    productos = proveedor.producto_set.all()  # Acceso a través de la relación ForeignKey
    return render(request, 'proveedores/proveedor_productos.html', {'proveedor': proveedor, 'productos': productos})




# ------------------------------ Categorías --------------------------------------------------
@login_required
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

@login_required
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

@login_required
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

@login_required
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
@method_decorator(login_required, name='dispatch')
class ProductosListView(ListView):
    model = Producto
    template_name = 'productos/productos_list.html'
    context_object_name = 'productos'
    ordering = ['nombre', '-fecha_creacion']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrar por categoría
        categoria = self.request.GET.get('categoria')
        if categoria and categoria != 'todo':
            queryset = queryset.filter(categoria__nombre=categoria)

        # Filtrar por proveedor
        proveedor = self.request.GET.get('proveedor')
        if proveedor:
            queryset = queryset.filter(proveedor__nombre=proveedor)

        # Búsqueda por nombre de producto
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todas las categorías y proveedores para los filtros
        context['categorias'] = Categoria.objects.all()
        context['proveedores'] = Proveedor.objects.all()
        context['query'] = self.request.GET.get('q', '')  # Mantener la búsqueda en la barra
        context['busqueda_placeholder'] = 'nombre del Producto'
        context['categoria_seleccionada'] = self.request.GET.get('categoria', 'todo')
        context['proveedor_seleccionado'] = self.request.GET.get('proveedor', '')

        return context
    

@login_required
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
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/productos_form.html', {'form': form})

@login_required
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

@login_required
def productos_confirm_delete(request, pk):
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
@method_decorator(login_required, name='dispatch')
class VentaListView(ListView):
    model = Venta
    template_name = 'ventas/venta_lista.html'  # Plantilla que se va a renderizar
    context_object_name = 'ventas'  # Nombre de la variable en el contexto
    ordering = ['-fecha']  # Orden por defecto (descendente por fecha)

    def get_queryset(self):
        queryset = super().get_queryset().filter(anulada=False).order_by('-fecha')  # Filtrar solo ventas no anuladas
        query = self.request.GET.get('q')  # Obtener el valor de la búsqueda desde la barra
        if query:
            try:
                # Intentar interpretar la cadena como una fecha en formato 'DD-MM-YY'
                fecha_buscada = datetime.strptime(query, '%d-%m-%y').date()  # Convierte a formato 'YYYY-MM-DD'
                queryset = queryset.filter(fecha=fecha_buscada)
            except ValueError:
                # Si no es una fecha, buscar por cliente o número de comprobante
                queryset = queryset.filter(
                    Q(cliente__nombre__icontains=query) |
                    Q(numero_comprobante__icontains=query)
                )
        return queryset
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Para mantener el valor de búsqueda en la barra
        context['busqueda_placeholder'] = 'fecha(D-M-A),cliente,número de comprobante.'  # Placeholder
        return context
# Vista para agregar una venta
@transaction.atomic
@login_required
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
@login_required
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

@login_required
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
@login_required
def cliente_lista(request):
    clientes = Cliente.objects.annotate(compras_recientes=Count('venta'))
    return render(request, 'clientes/cliente_lista.html', {'clientes': clientes})


# Vista para agregar cliente
@login_required
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
@login_required
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
@login_required
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_lista')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})

# Función para obtener la cantidad de compras realizadas por cliente




# ------------------------------ PAGINACIÓN DE LA LISTA DE COMPRAS --------------------------------------------------
@method_decorator(login_required, name='dispatch')
class clienteCompras(ListView):
    model = Venta
    template_name = 'clientes/cliente_compras.html'
    context_object_name = 'ventas'
    paginate_by = 10

    def get_queryset(self):
        cliente = get_object_or_404(Cliente, pk=self.kwargs['pk'])  # Obtener el cliente usando el pk
        queryset = super().get_queryset().filter(cliente=cliente)  # Filtrar ventas por el cliente
        query = self.request.GET.get('q')  # Considerando el caso de búsqueda
        if query:
            queryset = queryset.filter(Q(titulo__icontains=query) | Q(de__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = get_object_or_404(Cliente, pk=self.kwargs['pk'])  # Obtener el cliente
        return context



