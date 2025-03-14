from django.core.mail import send_mail

def enviar_respuesta_por_correo(consulta):
    subject = f"Respuesta a tu consulta del {consulta.fecha_consulta}"
    message = f"Hola {consulta.usuario.nombre},\n\n{consulta.respuesta}\n\nSaludos,\nEl equipo de soporte"
    send_mail(subject, message, 'tu_correo@gmail.com', [consulta.usuario.email])