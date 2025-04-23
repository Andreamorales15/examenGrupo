from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from models.intructor import NombreIntructor
from app import app

bcrypt = Bcrypt(app)

@app.route('/base', methods=['GET', 'POST'])
def base():
    return render_template('basee.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_input = request.form['correo']
        clave_input = request.form['clave']
        instructor = NombreIntructor.objects(correoelectronico=correo_input).first()
        if instructor and bcrypt.check_password_hash(instructor.contrasena, clave_input):
            session['instructor_id'] = str(instructor.id)
            session.permanent = True
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('base'))
        else:
            flash('Correo o contraseña incorrectos. Intenta nuevamente.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/cerrarlasesion')
def logout():
    session.pop('instructor_id', None)
    flash('se cerro la sesion', 'info')
    return redirect(url_for('login'))