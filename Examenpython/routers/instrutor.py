from flask import render_template, request
from models.sena import NombreSena
from models.intructor import NombreIntructor
from app import app
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
                nuevo_instructor = NombreIntructor(
                    nombrecompleto=nombre,
                    correoelectronico=correo,
                    centro=sena_ref
                )
                nuevo_instructor.save()
                estado = True
                mensaje = "Instructor agregado correctamente"
            else:
                mensaje = "Centro SENA no encontrado"
        else:
            mensaje = "Método no permitido"
    except Exception as e:
        mensaje = f"Error: {str(e)}"
        print("EXCEPCIÓN:", mensaje)

    return render_template('agregarinstructor.html', estado=estado, mensaje=mensaje, senas=senas)