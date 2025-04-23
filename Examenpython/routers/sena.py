from flask import request,render_template,jsonify,redirect,url_for,session,flash
from models.sena import NombreSena
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/agregarsena/",methods=['GET', 'POST'])
def addGenero():
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos=request.get_json(force=True)
            genero=NombreSena(**datos)
            genero.save()
            estado=True
            mensaje="Sena Agregado correctamente"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
    return render_template('agregarsena.html',estado=estado,mensaje=mensaje)