# miAplicacion/forms.py
from django import forms
from .models import (Categoria, Proveedor, Producto, Venta, DetalleVenta,)

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad_stock', 'categoria', 'proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'medio_de_pago',]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'medio_de_pago': forms.Select(attrs={'class': 'form-control'}),
        }

class DetalleVentaForm(forms.ModelForm):
    precio = forms.DecimalField(label="Precio del producto", required=False, max_digits=10, decimal_places=2)

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
        
        # Validación personalizada para el campo "cantidad"
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser un número positivo.")
        return cantidad

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si ya tenemos un producto seleccionado, mostramos su precio
        if self.instance and self.instance.producto:
            self.fields['precio'].initial = self.instance.producto.precio
        self.fields['precio'].widget.attrs['readonly'] = True  # El precio no debe ser editable