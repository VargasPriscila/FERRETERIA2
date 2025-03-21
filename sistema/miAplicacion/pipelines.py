from .models import Cliente

def crear_cliente_google(sociallogin, user, **kwargs):
    """
    Se ejecuta cuando un usuario inicia sesión con Google por primera vez.
    Si el usuario no tiene un Cliente, se crea automáticamente con su nombre y apellido.
    """
    if not Cliente.objects.filter(user=user).exists():  # Verifica si ya tiene un cliente
        extra_data = sociallogin.account.extra_data  # Obtiene los datos de Google
        nombre = extra_data.get('given_name', '')  # Nombre del usuario
        apellido = extra_data.get('family_name', '')  # Apellido del usuario

        # Crear el cliente con la información de Google
        Cliente.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            email=user.email
        )
