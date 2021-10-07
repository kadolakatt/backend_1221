import os
import yagmail as yagmail

from flask import Flask, jsonify, render_template, request
from mensajes import lista_mensajes
from forms import FormContactanos, FormRespuesta

app = Flask(__name__)

#INICIO - CP10
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contactanos/', methods=["GET", "POST"])
def contactanos():
     if request.method == "GET":
         formulario = FormContactanos()
         return render_template('contactanos.html', form = formulario)
     else:
        formulario = FormContactanos(request.form)
        if formulario.validate_on_submit():
            yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
            yag.send(to=formulario.correo.data, subject="Su mensaje ha sido recibido.",
            contents="Hola {0}, hemos recibido tu mensaje, pronto nos comunicaremos con ustedes.".format(formulario.nombre.data))
            return render_template("contactanos.html", form=FormContactanos(), mensaje="Su mensaje ha sido enviado.")
        return render_template("contactanos.html", form=formulario)
#FIN - CP10

#INICIO - Endpoint estilos servicios RESTful hechos en Flask
@app.route("/mensajes/listado/json",methods=["GET"])
def get_listado_mensajes_json():
    return jsonify(lista_mensajes)

@app.route("/mensajes/ver/json/<id>")
def get_mensaje_json(id):
    for i in range(len(lista_mensajes)):
        if lista_mensajes[i]["id"] == id:
            return lista_mensajes[i]
    
    return jsonify({"error":"No existe un mensaje con el id especificado." })
#FIN - Endpoint estilos servicios RESTful hechos en Flask

#INICIO - Funciones controladoras CP11
@app.route("/mensajes/listado/")
def get_listado_mensajes():
    return render_template('listado_mensajes.html',lista=lista_mensajes)


@app.route("/mensajes/ver/<id>")
def get_mensaje(id):
    for i in range(len(lista_mensajes)):
        if lista_mensajes[i]["id"] == id:
            return render_template('ver_mensaje.html', item=lista_mensajes[i])
    
    return render_template('ver_mensaje.html', error="No existe un mensaje para el id especificado.")


@app.route("/mensajes/respuesta/<id>",methods=["GET", "POST"])
def responder_mensaje(id):
    if request.method == "GET":
        formulario = FormRespuesta()
        #Buscamos en nuestra "base de datos" el mensaje con ese id.
        for i in range(len(lista_mensajes)):
            if lista_mensajes[i]["id"] == id:
                formulario.nombre.data = lista_mensajes[i]["nombre"]
                formulario.correo.data = lista_mensajes[i]["correo"]
                formulario.mensaje_original.data = lista_mensajes[i]["mensaje"]
                return render_template('responder_mensaje.html',id=id, form=formulario)
        
        return render_template('responder_mensaje.html',id=id, form=formulario, mensaje="No existe un mensaje para el id especificado")
    else:
        formulario = FormRespuesta(request.form)
        if formulario.validate_on_submit(): 
            yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
            yag.send(to=formulario.correo.data, subject="Su mensaje ha sido respondido.",
            contents="Hola, la respuesta a tu mensaje es: {0}".format(formulario.respuesta.data))
            return render_template('responder_mensaje.html', id=id,form=FormRespuesta(), mensaje="La respuesta ha sido enviada.")
        
        return render_template('responder_mensaje.html', id=id,form=formulario, mensaje="Todos los campos son obligatorios.")
            

