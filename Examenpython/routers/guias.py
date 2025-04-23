from flask import render_template, request, send_from_directory,flash, redirect, url_for, session
from models.guia import Guia
from models.intructor import NombreIntructor
from app import app
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from flask import send_from_directory


@app.route('/uploads/pdf/<filename>')
def upload_pdf(filename):
    return send_from_directory('upload/pdf', filename)

@app.route("/listarguia", methods=["GET"])
def listar_guias():
    if 'instructor_id' not in session:
        return redirect(url_for('login'))
    guias = Guia.objects()
    return render_template("listarguia.html", guias=guias)

app.config['CARPETA_SUBIDAS'] = 'upload/pdf'
app.config['EXTENSIONES_PERMITIDAS'] = {'pdf'}

def es_archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and nombre_archivo.rsplit('.', 1)[1].lower() in app.config['EXTENSIONES_PERMITIDAS']


@app.route("/agregarguia/", methods=["GET", "POST"])
def agregar_guia():
    if 'instructor_id' not in session:
        return redirect(url_for('login'))
    mensaje = None
    instructores = NombreIntructor.objects()

    if request.method == "POST":
        try:
            nombreguia = request.form.get("nombreguia")
            descripcion = request.form.get("descripcion")
            programa_formacion = request.form.get("programaformacion")
            fecha = request.form.get("fecha")
            instructor_id = request.form.get('instructor_id')
            instructor = NombreIntructor.objects(id=instructor_id).first()
            archivo = request.files.get("documento")

            if not archivo or archivo.filename == '':
                mensaje = "Debes seleccionar un archivo PDF."
                return render_template(
                    "agregarguia.html",
                    instructores=instructores,
                    mensaje=mensaje
                )

            if not es_archivo_permitido(archivo.filename):
                mensaje = "El archivo debe estar en formato PDF."
                return render_template(
                    "agregarguia.html",
                    instructores=instructores,
                    mensaje=mensaje
                )

            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                mensaje = "La fecha no tiene un formato válido."
                return render_template(
                    "agregarguia.html",
                    instructores=instructores,
                    mensaje=mensaje
                )

            nombre_archivo = secure_filename(archivo.filename)
            ruta_archivo = os.path.join(app.config['CARPETA_SUBIDAS'], nombre_archivo)
            archivo.save(ruta_archivo)

            nueva_guia = Guia(
                nombreguia=nombreguia,
                descripcion=descripcion,
                programaformacion=programa_formacion,
                documento=nombre_archivo, 
                fecha=fecha,
                instructor=instructor
            )
            nueva_guia.save()

            mensaje = "Guía registrada exitosamente."
            return render_template(
                "agregarguia.html",
                instructores=instructores,
                mensaje=mensaje
            )

        except Exception as e:
            mensaje = f"Error al guardar la guía: {str(e)}"
            return render_template(
                "agregarguia.html",
                instructores=instructores,
                mensaje=mensaje
            )

    return render_template("agregarguia.html", instructores=instructores, mensaje=None)
