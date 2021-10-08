import os
import yagmail as yagmail

from flask import Flask, jsonify, render_template, request
from forms import FormContactanos, FormRespuesta
from models import mensaje #Importamos del models nuestra modelo mensaje

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

            #Creamos una instancia de la clase mensaje e invocamos el metodo insertar
            obj_mensaje = mensaje(p_id=0, p_nombre=formulario.nombre.data,
            p_correo = formulario.correo.data, p_mensaje=formulario.mensaje.data)

            #Invocamos el metodo insertar
            if obj_mensaje.insertar():
                yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
                yag.send(to=formulario.correo.data, subject="Su mensaje ha sido recibido.",
                contents="Hola {0}, hemos recibido tu mensaje, pronto nos comunicaremos con ustedes.".format(formulario.nombre.data))
                return render_template("contactanos.html", form=FormContactanos(), mensaje="Su mensaje ha sido enviado.")
            else:
                return render_template("contactanos.html", form=formulario, mensaje="No se pudo guardar el mensaje. Consulte a sopote técnico.")

        return render_template("contactanos.html", form=formulario)
#FIN - CP10

#INICIO - Endpoint estilos servicios RESTful hechos en Flask
@app.route("/mensajes/listado/json",methods=["GET"])
def get_listado_mensajes_json():
    #devuelve el listado de mensajes de la base de datos
    return jsonify(mensaje.listado())

@app.route("/mensajes/ver/json/<id>")
def get_mensaje_json(id):
    obj_mensaje = mensaje.cargar(id)
    if obj_mensaje:
        return obj_mensaje
    return jsonify({"error":"No existe un mensaje con el id especificado." })
#FIN - Endpoint estilos servicios RESTful hechos en Flask

#INICIO - Funciones controladoras CP11
@app.route("/mensajes/listado/")
def get_listado_mensajes():
    return render_template('listado_mensajes.html',lista=mensaje.listado())


@app.route("/mensajes/ver/<id>")
def get_mensaje(id):
    obj_mensaje = mensaje.cargar(id)
    if obj_mensaje:
        return render_template('ver_mensaje.html', item=obj_mensaje)
    
    return render_template('ver_mensaje.html', error="No existe un mensaje para el id especificado.")


@app.route("/mensajes/respuesta/<id>",methods=["GET", "POST"])
def responder_mensaje(id):
    if request.method == "GET":
        formulario = FormRespuesta()
        #Buscamos en nuestra "base de datos" el mensaje con ese id.
        obj_mensaje = mensaje.cargar(id)
        if obj_mensaje:
            formulario.nombre.data = obj_mensaje.nombre
            formulario.correo.data = obj_mensaje.correo
            formulario.mensaje_original.data = obj_mensaje.mensaje
            return render_template('responder_mensaje.html',id=id, form=formulario)
        
        return render_template('responder_mensaje.html',id=id, form=formulario, mensaje="No existe un mensaje para el id especificado")
    else:
        formulario = FormRespuesta(request.form)
        if formulario.validate_on_submit(): 

            obj_mensaje = mensaje.cargar(id)
            if obj_mensaje:
                obj_mensaje.respuesta = formulario.respuesta.data
                if obj_mensaje.responder():
                    yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
                    yag.send(to=formulario.correo.data, subject="Su mensaje ha sido respondido.",
                    contents="Hola, la respuesta a tu mensaje es: {0}".format(formulario.respuesta.data))
                    return render_template('responder_mensaje.html', id=id,form=FormRespuesta(), mensaje="La respuesta ha sido enviada.")
            else:
                return render_template('responder_mensaje.html', id=id,form=formulario, mensaje="No existe un mensaje para el id seleccionado.")        
        
        return render_template('responder_mensaje.html', id=id,form=formulario, mensaje="Todos los campos son obligatorios.")
            

