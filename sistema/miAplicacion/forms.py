# miAplicacion/forms.py

from django import forms
from .models import Categoria
from .models import Proveedor


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion']  # Incluye los campos que quieres que el formulario maneje

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre','contacto', 'direccion']


