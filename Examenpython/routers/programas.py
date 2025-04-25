from flask import request,render_template,jsonify,redirect,url_for,session,flash
from models.programas import NombredelPrograma
from app import app

@app.route("/agregarprograma/",methods=['GET', 'POST'])
def addPrograma():
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos=request.get_json(force=True)
            genero=NombredelPrograma(**datos)
            genero.save()
            estado=True
            mensaje="Sena Agregado correctamente"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
    return render_template('agregarprogma.html',estado=estado,mensaje=mensaje)