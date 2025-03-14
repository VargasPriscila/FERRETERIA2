"""
Este módulo define los formularios utilizados en la aplicación de gestión de una ferretería,
basados en los modelos de la base de datos. Los formularios permiten la creación y actualización
de categorías, proveedores, productos, ventas y clientes, con validaciones personalizadas y
widgets estilizados para mejorar la experiencia de usuario.


Widgets:
--------
Los formularios utilizan widgets personalizados para agregar clases CSS a los campos, permitiendo
una integración fluida con frameworks de diseño como Bootstrap.

Validaciones personalizadas:
----------------------------
- DetalleVentaForm: Valida que la cantidad de productos vendidos sea positiva.

Este módulo está diseñado para proporcionar una interfaz amigable para los administradores de la
ferretería, asegurando la entrada de datos precisa y coherente en la aplicación.
"""
# miAplicacion/forms.py
from django import forms
from .models import (Categoria, Proveedor, Producto, Venta, DetalleVenta,Cliente, Producto,Consulta)
from django.forms.models import inlineformset_factory
from django.forms import ValidationError


class ConsultaForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Consulta
        fields = ['mensaje', 'productos']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['respuesta']

# ------------------------------ Categorías ------------------------------
class CategoriaForm(forms.ModelForm):
    """
    Formulario para el modelo `Categoria`.

    Campos:
    - nombre: Nombre de la categoría.
    - descripcion: Descripción de la categoría.

    Se utilizan widgets personalizados para agregar clases CSS a los campos.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }



# ------------------------------ Proveedores ------------------------------
class ProveedorForm(forms.ModelForm):
    """
    Formulario para el modelo `Proveedor`.

    Campos:
    - nombre: Nombre del proveedor.
    - tipo_producto: Tipo de producto que ofrece el proveedor.
    - telefono: Número de teléfono del proveedor.
    - email: Correo electrónico del proveedor.
    - direccion: Dirección física del proveedor.

    Los widgets se utilizan para personalizar la apariencia de los campos en el formulario.
    """
    class Meta:
        model = Proveedor
        fields = ['nombre', 'tipo_producto', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



# ------------------------------ Productos ------------------------------
class ProductoForm(forms.ModelForm):
    """
    Formulario para el modelo `Producto`.

    Campos:
    - nombre: Nombre del producto.
    - descripcion: Descripción del producto.
    - precio: Precio del producto.
    - cantidad_stock: Cantidad en stock disponible.
    - categoria: Categoría a la que pertenece el producto.
    - proveedor: Proveedor del producto.

    Los widgets personalizados añaden clases CSS para mejorar la apariencia del formulario.
    """
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'descripcion', 'precio', 'cantidad_stock', 'categoria', 'proveedor', 'codigo_barras']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }



# ------------------------------ Ventas ------------------------------
#class VentaForm(forms.ModelForm):
    """
    Formulario para el modelo `Venta`.

    Campos:
    - cliente: Cliente que realiza la compra.
    - medio_de_pago: Medio de pago utilizado para la compra.

    Utiliza selectores personalizados para los campos de cliente y medio de pago.
    """
    #class Meta:
        #model = Venta
        #fields = ['cliente', 'medio_de_pago']
        #widgets = {
            #'cliente': forms.Select(attrs={'class': 'form-control'}),
            #'medio_de_pago': forms.Select(attrs={'class': 'form-control'}),
 #       }




#class DetalleVentaForm(forms.ModelForm):
    """
    Formulario para el modelo `DetalleVenta`.

    Campos:
    - producto: Producto seleccionado para la venta.
    - cantidad: Cantidad de producto vendida.

    Incluye validación personalizada para asegurarse de que la cantidad sea positiva.
    """
    #class Meta:
        #model = DetalleVenta
        #fields = ['producto', 'cantidad']
        #widgets = {
 #           'producto': forms.Select(attrs={'class': 'form-control'}),
  #          'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
   #     }

#   def clean_cantidad(self):
"""
        Valida que la cantidad ingresada sea un número positivo.

        Retorna:
        --------
        cantidad : int
            La cantidad validada.

        Lanza:
        -------
        forms.ValidationError:
            Si la cantidad no es positiva.
        """
        #cantidad = self.cleaned_data.get('cantidad')
        #if cantidad is None or cantidad <= 0:
            #raise forms.ValidationError("La cantidad debe ser un número positivo.")
        #return cantidad


# ------------------------------ Clientes ------------------------------
class ClienteForm(forms.ModelForm):
    """
    Formulario para el modelo `Cliente`.

    Campos:
    - nombre: Nombre del cliente.
    - apellido: Apellido del cliente.
    - documento: Documento de identificación del cliente.
    - direccion: Dirección física del cliente.
    - telefono: Número de teléfono del cliente.
    - email: Correo electrónico del cliente.
    """
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'documento', 'direccion', 'telefono', 'email']
        
        
        
        
        
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario', 'importe']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Calcular precio e importe inicial si el producto está definido
        if self.instance.producto:
            self.fields['precio_unitario'].initial = self.instance.producto.precio
            self.fields['importe'].initial = (
                self.instance.cantidad * self.instance.producto.precio
                if self.instance.cantidad else 0
            )

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')  # Obtener el producto seleccionado
        cantidad = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')

        # Validar si el producto y la cantidad existen
        if producto and cantidad:
            # Verificar que la cantidad no exceda el stock disponible
            if cantidad > producto.cantidad_stock:
                self.add_error(
                    'cantidad',
                    f"La cantidad seleccionada ({cantidad}) excede el stock disponible ({producto.cantidad_stock}) para '{producto.nombre}'."
                )

        # Calcular el importe (si ambos campos tienen valor)
        if cantidad and precio_unitario:
            cleaned_data['importe'] = cantidad * precio_unitario

        return cleaned_data


# Crear el inline formset para DetalleVenta
DetalleVentaInlineFormSet = inlineformset_factory(
    Venta,  # Modelo padre
    DetalleVenta,  # Modelo hijo
    form=DetalleVentaForm,
    fields=['producto', 'cantidad', 'precio_unitario', 'importe'],  # Campos a incluir en el form
    extra=1,  # Número de formularios extra
    can_delete=True  # Permitir eliminación de filas
)

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'medio_de_pago']



