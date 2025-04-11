from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from models.intructor import NombreIntructor
from app import app
from Examenpython.venv.correo import enviar_correo_asincrono
import requests

bcrypt = Bcrypt(app)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_input = request.form['correo']
        clave_input = request.form['clave']
        instructor = NombreIntructor.objects(correoelectronico=correo_input).first()
        if instructor and instructor.check_password(clave_input):
            session['instructor_id'] = str(instructor.id)
            session.permanent = True
            flash('Inicio de sesión exitoso.', 'success')
            asunto = "Inicio de sesión exitoso"
            mensaje = f"Hola {instructor.nombrecompleto}, has iniciado sesión correctamente."
            enviar_correo_asincrono(instructor.correoelectronico, asunto, mensaje)
            return redirect(url_for('principal'))
        else:
            flash('Correo o contraseña incorrectos. Intenta nuevamente.')
            return redirect(url_for('login'))

    return render_template('login.html')
