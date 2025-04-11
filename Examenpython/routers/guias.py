from flask import render_template, request
from models.guia import NombreGuia
from models.intructor import NombreIntructor
from app import app
from werkzeug.utils import secure_filename
import os

app.config['UPLOAD_FOLDER'] = 'uploads/pdf'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/listarguia", methods=["GET"])
def listar_guias():
    guias = NombreGuia.objects() 
    return render_template("listarguia.html", guias=guias)


@app.route("/agregarguia", methods=["GET", "POST"])
def agregar_guia():
    mensaje = None
    estado = False
    instructores = NombreIntructor.objects()

    if request.method == "POST":
        try:
            nombreguia = request.form.get("nombreguia")
            descripcions = request.form.get("descripcions")
            programaformacion = request.form.get("programaformacion")
            fecha = request.form.get("fecha")
            instructor_id = request.form.get("intructordeproceso")
            if 'documento' not in request.files:
                mensaje = "No se ha subido ningún archivo PDF."
                return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)
            archivo = request.files['documento']
            if archivo.filename == '':
                mensaje = "No seleccionaste un archivo PDF."
                return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)
            if archivo and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                archivo.save(filepath)
                instructor_ref = NombreIntructor.objects(id=instructor_id).first()
                if instructor_ref:
                    nueva_guia = NombreGuia(
                        nombreguia=nombreguia,
                        descripcions=descripcions,
                        programaformacion=programaformacion,
                        documento=filepath,  
                        fecha=fecha,
                        intructordeproceso=instructor_ref
                    )
                    nueva_guia.save()
                    estado = True
                    mensaje = "Guía registrada exitosamente con el documento PDF."
                else:
                    mensaje = "Instructor no encontrado."
            else:
                mensaje = "El archivo no es un PDF válido."
        except Exception as e:
            mensaje = f"Error al guardar la guía: {str(e)}"
    return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)

