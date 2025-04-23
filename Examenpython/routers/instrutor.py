from flask import render_template, request
from models.sena import NombreSena
from models.intructor import NombreIntructor
from app import app, mail
from flask_mail import Message
from flask_bcrypt import Bcrypt
import secrets
import threading

bcrypt = Bcrypt(app)

@app.route("/agregarinstructor/", methods=['GET', 'POST'])
def agregar_instructor():
    try:
        mensaje = None
        estado = False
        senas = NombreSena.objects() 
        if request.method == 'POST':
            datos = request.json
            nombre = datos.get('nombrecompleto')
            correo = datos.get('correoelectronico')
            sena_id = datos.get('sena')
            sena_ref = NombreSena.objects(id=sena_id).first()
            if sena_ref:
                contrasena = secrets.token_urlsafe(8)
                contrasena_encriptada = bcrypt.generate_password_hash(contrasena).decode('utf-8')
                nuevo_instructor = NombreIntructor(
                    nombrecompleto=nombre,
                    correoelectronico=correo,
                    centro=sena_ref,
                    contrasena=contrasena_encriptada
                )
                nuevo_instructor.save()
                enviarCorreoIntructor(correo, contrasena)
                estado = True
                mensaje = "Instructor agregado correctamente y contraseña enviada al correo."
            else:
                mensaje = "Centro SENA no encontrado."
        else:
            mensaje = "Método no permitido."
    except Exception as e:
        mensaje = f"Error: {str(e)}"
        print("EXCEPCIÓN:", mensaje)

    return render_template('agregarinstructor.html', estado=estado, mensaje=mensaje, senas=senas)

def enviar_correo(destinatario, contrasena):

    try:
        with app.app_context():
            asunto = "Contraseña para acceso"
            cuerpo = f"HolaTu contraseña  es: {contrasena}"
            mensaje = Message(asunto, recipients=[destinatario])
            mensaje.body = cuerpo
            mail.send(mensaje)
            print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")

def enviarCorreoIntructor(destinatario, contrasena):

    hilo = threading.Thread(target=enviar_correo, args=(destinatario, contrasena))
    hilo.start()