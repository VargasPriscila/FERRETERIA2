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
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Proveedor, Producto, Venta, DetalleVenta, Cliente, Consulta
from .forms import (CategoriaForm, ProveedorForm, ProductoForm,VentaForm, DetalleVentaInlineFormSet,ClienteForm, ConsultaForm, RespuestaForm)
from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Count
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags






def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('panel_administracion')  # Redirige a la página de administración
                else:
                    return redirect('productos_list')  # Redirige a la página de productos para usuarios no administradores
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def index(request):
    productos = Producto.objects.all().order_by('nombre')
    productos_grupos = [productos[i:i + 6] for i in range(0, len(productos), 6)]  # Agrupar en grupos de 3
    is_admin = request.user.is_authenticated and request.user.is_staff  # Verifica si el usuario está autenticado y es administrador
    context = {
        'productos_grupos': productos_grupos,
        'is_admin': is_admin,  # Agrega la variable is_admin al contexto
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('panel_administracion')  # Redirigir al panel de administración
        else:
            return redirect('productos_list')  # Redirigir a la lista de productos
    # Lógica para manejar el formulario de inicio de sesión

def admin_required(view_func):
    """
    Decorador para restringir el acceso a las vistas solo a administradores.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:  # Verificar si el usuario es administrador
            raise PermissionDenied  # Denegar acceso si no es administrador
        return view_func(request, *args, **kwargs)
    return wrapper  
    

# ------------------------------ Proveedores -------------------------------------------------

@login_required
@admin_required
def proveedor_list(request):
    """
    Muestra una lista de todos los proveedores disponibles.
    """
    proveedores = Proveedor.objects.all()
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'proveedores/proveedor_list.html', {'proveedores': proveedores, 'is_admin': is_admin})

@login_required
@admin_required
def proveedor_create(request):
    """
    Crea un nuevo proveedor.
    """
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'proveedores/proveedor_form.html', {'form': form, 'is_admin': is_admin})

@login_required
@admin_required
def proveedor_update(request, pk):
    """
    Actualiza un proveedor existente.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'proveedores/proveedor_form.html', {'form': form, 'is_admin': is_admin})

@login_required
@admin_required
def proveedor_delete(request, pk):
    """
    Elimina un proveedor existente.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'proveedores/proveedor_confirm_delete.html', {'proveedor': proveedor, 'is_admin': is_admin})

@login_required
@admin_required
def proveedor_productos(request, proveedor_id):
    """
    Muestra los productos asociados a un proveedor.
    """
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    productos = proveedor.producto_set.all()
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'proveedores/proveedor_productos.html', {'proveedor': proveedor, 'productos': productos, 'is_admin': is_admin})



# ------------------------------ Categorías --------------------------------------------------

@login_required
@admin_required
def categoria_list(request):
    """
    Muestra una lista de todas las categorías disponibles.
    """
    categorias = Categoria.objects.all()
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'categorias/categoria_list.html', {'categorias': categorias, 'is_admin': is_admin})

@login_required
@admin_required
def categoria_create(request):
    """
    Crea una nueva categoría.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'categorias/categoria_form.html', {'form': form, 'is_admin': is_admin})

@login_required
@admin_required
def categoria_update(request, pk):
    """
    Actualiza una categoría existente.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'categorias/categoria_form.html', {'form': form, 'is_admin': is_admin})

@login_required
@admin_required
def categoria_delete(request, pk):
    """
    Elimina una categoría existente.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'categorias/categoria_confirm_delete.html', {'categoria': categoria, 'is_admin': is_admin})



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

        # Agregar is_admin al contexto
        context['is_admin'] = self.request.user.is_staff  # Verifica si el usuario es administrador

        return context
    

@admin_required
@login_required
def productos_create(request):
    """
    Crea un nuevo producto.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm()
    
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'productos/productos_form.html', {'form': form, 'is_admin': is_admin})

@admin_required
@login_required
def productos_update(request, pk):
    """
    Actualiza un producto existente.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_list')
    else:
        form = ProductoForm(instance=producto)
    
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'productos/productos_form.html', {'form': form, 'is_admin': is_admin})

@admin_required
@login_required
def productos_confirm_delete(request, pk):
    """
    Elimina un producto existente.
    """
    producto = get_object_or_404(Producto, pk=pk)
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'productos/productos_confirm_delete.html', {'producto': producto, 'is_admin': is_admin})



# ------------------------------ Ventas --------------------------------------------------

# Vista para listar ventas

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
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
        context['is_admin'] = self.request.user.is_staff  # Verifica si el usuario es administrador
        return context
# Vista para agregar una venta
@admin_required
@login_required
@transaction.atomic
def agregar_venta(request):
    if request.method == "POST":
        form_venta = VentaForm(request.POST)
        formset_detalle = DetalleVentaInlineFormSet(request.POST, instance=form_venta.instance)
        
        if form_venta.is_valid() and formset_detalle.is_valid():
            # Guardar la venta
            venta = form_venta.save()

            # Procesar los formularios del formset
            for form in formset_detalle:
                print(form.cleaned_data)
                if form.cleaned_data.get('DELETE'):
                    if form.instance.pk:  # Si la instancia ya existe en la base de datos
                        form.instance.delete()  # Eliminar la instancia
                else:
                    detalle = form.save(commit=False)
                    detalle.venta = venta
                    detalle.importe = detalle.cantidad * detalle.precio_unitario
                    detalle.save()

            return redirect('venta_lista')  # Redirige a la lista de ventas
    else:
        form_venta = VentaForm()
        formset_detalle = DetalleVentaInlineFormSet(instance=Venta())
    
    # Obtener lista de productos para cargar en el select
    productos = Producto.objects.all()

    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'ventas/venta_agregar.html', {
        'form_venta': form_venta,
        'formset_detalle': formset_detalle,
        'productos': productos,
        'is_admin': is_admin,  # Pasar is_admin al contexto
    })

# Vista para anular una venta
@admin_required
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

    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'ventas/venta_anular.html', {'venta': venta, 'is_admin': is_admin})

@admin_required
@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles_venta = DetalleVenta.objects.filter(venta=venta)

    # Obtener la hora del primer detalle (si existe)
    hora_venta = detalles_venta.first().hora if detalles_venta.exists() else None

    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    context = {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'hora_venta': hora_venta,  # Pasar la hora del primer detalle al contexto
        'is_admin': is_admin,  # Pasar is_admin al contexto
    }
    return render(request, 'ventas/detalle_venta.html', context)

# ------------------------------ Clientes --------------------------------------------------
# Vista para listar clientes
@admin_required
@login_required
def cliente_lista(request):
    clientes = Cliente.objects.annotate(compras_recientes=Count('venta'))
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'clientes/cliente_lista.html', {'clientes': clientes, 'is_admin': is_admin})

# Vista para agregar cliente
@admin_required
@login_required
def cliente_agregar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_lista')
    else:
        form = ClienteForm()
    
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'clientes/cliente_form.html', {'form': form, 'is_admin': is_admin})

# Vista para editar cliente
@admin_required
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
    
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'clientes/cliente_form.html', {'form': form, 'is_admin': is_admin})

# Vista para eliminar cliente
@admin_required
@login_required
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    is_admin = request.user.is_staff  # Verifica si el usuario es administrador
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente, 'is_admin': is_admin})
# Función para obtener la cantidad de compras realizadas por cliente




# ------------------------------ PAGINACIÓN DE LA LISTA DE COMPRAS --------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
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


#----------------------------Endpoint para obtener el precio del Producto--------------------------------------------------------------------------------------------
def obtener_precio_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({'precio': producto.precio})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    
    
    
    
    
    
# ------------------------------ Consulta de Clientes --------------------------------------------------  


@login_required
def enviar_consulta(request):
    productos_seleccionados = []  # Inicializamos una lista vacía

    if request.method == 'POST':
        productos_seleccionados_ids = request.POST.getlist('productos')
        productos_seleccionados = Producto.objects.filter(id__in=productos_seleccionados_ids)

        form = ConsultaForm(request.POST)
        if form.is_valid():
            # Verificar si el usuario tiene un cliente, si no, crearlo
            cliente, created = Cliente.objects.get_or_create(user=request.user)

            consulta = form.save(commit=False)
            consulta.usuario = cliente  # Ahora sí existe
            consulta.save()
            consulta.productos.set(productos_seleccionados)

            # Enviar correo al administrador
            subject = f"Nueva consulta de {consulta.usuario.user.username}"
            message = f"Has recibido una nueva consulta:\n\n" \
                f"Usuario: {consulta.usuario.user.username}\n" \
                f"Productos: {', '.join([p.nombre for p in productos_seleccionados])}\n" \
                f"Mensaje: {consulta.mensaje}\n\n" \
                f"Puedes responderla desde el panel de administración."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "Consulta enviada exitosamente.")
            return redirect('productos_list')
        else:
            messages.error(request, "Hubo un error al enviar la consulta.")
    else:
        form = ConsultaForm()

    return render(request, 'consultas/enviar_consulta.html', {'form': form, 'productos_seleccionados': productos_seleccionados})
# ------------------------------  Vista para Responder Consultas de Clientes --------------------------------------------------  
@login_required
def lista_consultas(request):
    if request.user.is_staff:  # Verificar si el usuario es administrador
        consultas = Consulta.objects.filter(respuesta__isnull=True)  # Mostrar solo consultas sin respuesta
        is_admin = request.user.is_staff  # Definir is_admin
        return render(request, 'consultas/lista_consultas.html', {'consultas': consultas, 'is_admin': is_admin})
    else:
        return redirect('index')  # Redirigir a usuarios no administradores

def enviar_respuesta_por_correo(consulta):
    """
    Envía un correo electrónico al usuario con la respuesta a su consulta.
    """
    subject = f"Respuesta a tu consulta sobre {', '.join([p.nombre for p in consulta.productos.all()])}"
    message = f"Hola {consulta.usuario.user.username},\n\n" \
        f"Gracias por contactarnos. Aquí está la respuesta a tu consulta:\n\n" \
        f"{consulta.respuesta}\n\n" \
        f"Saludos,\nEl equipo de Ferretería&BuloneríaSuárez"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [consulta.usuario.user.email]

    # Crear el objeto EmailMessage
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
        reply_to=[from_email],  # Configura el Reply-To
    )
    email.send()



@login_required
def responder_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        form = RespuestaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.fecha_respuesta = timezone.now()
            consulta.save()

            # Enviar correo al usuario con la respuesta
            subject = f"Respuesta a tu consulta sobre {', '.join([p.nombre for p in consulta.productos.all()])}"
            html_message = render_to_string('emails/respuesta_usuario.html', {
                'consulta': consulta,
                'productos': consulta.productos.all(),
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [consulta.usuario.user.email]

            email = EmailMessage(
                subject,
                plain_message,
                from_email,
                recipient_list,
            )
            email.content_subtype = "html"
            email.send()

            return redirect('lista_consultas')
    else:
        form = RespuestaForm(instance=consulta)
    
    # Agregar is_admin al contexto
    is_admin = request.user.is_staff
    context = {
        'form': form,
        'consulta': consulta,
        'is_admin': is_admin,  # Pasar is_admin al contexto
    }
    return render(request, 'consultas/responder_consulta.html', context)


# ------------------------------  Vista para Administrador --------------------------------------------------  
@admin_required
def panel_administracion(request):
    return render(request, 'admin/panel_administracion.html')



# ------------------------------  Agregar Producto por código de barras --------------------------------------------------  

def obtener_producto_por_codigo(request):
    codigo_barras = request.GET.get('codigo_barras', None)
    
    if codigo_barras:
        try:
            producto = Producto.objects.get(codigo_barras=codigo_barras)
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
            })
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    return JsonResponse({'error': 'Código de barras no proporcionado'}, status=400)




























#inicio para administradoressssssss

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Verifica si el usuario es staff (administrador)
            login(request, user)
            return redirect('panel_administracion')  # Redirige al panel de administración
        else:
            # Mensaje de error si las credenciales son incorrectas
            return render(request, 'admin_login.html', {'error': 'Credenciales inválidas o no eres administrador.'})
    return render(request, 'admin_login.html')