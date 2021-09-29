#Importamos la clase Flask del modulo
#flask que será nuestro framework.
from flask import Flask 

#A una variable app le asignamos
#una instancia de la aplicación Flask
#que creamos a partir de clase Flask, recibe 
#de parametros el nombre del modulo que se está ejecutando
#variable __name__
app = Flask(__name__)

#Decorador que nos permite especificar la URL
#que desde el navegador nos va a permitir
#ejecutar esta funcion del lado del servidor.
@app.route('/')
def index(): #función en sintaxis python
    
    #Este return devuelve, lo que el navegador
    #recibirá de respuesta.
    return "<h1>Hola, Mundo!</h1>" 


