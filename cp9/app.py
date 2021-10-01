#importamos el modulo yagmail instalado al inicio de la practica y sirve para enviar email a través de gmail
import yagmail as yagmail 

from flask import Flask, render_template, request, redirect, url_for

from utils import * #importamos el modulo util para invocar las validaciones
#import utils #otra forma de importar el modulo util, cambia la invocacion de las validaciones utils.isEmailValid

app = Flask(__name__)

@app.route('/',  methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    if (request.method == 'GET'):
        return render_template('registro.html')
    else:
        errores = ""
        exito = ""

        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        sexo = request.form['sexo']
        email = request.form['email']
        password = request.form['contrasena']

        if request.form['declaracion']:
            declaracion = request.form['declaracion']
        else:
            errores += "Debe especificar la declaración"


        

        if len(nombre) <= 0:
            errores += "Debe escribir un nombre válido."
        
        if len(apellidos) <=0:
            errores += "Debe digitar un apellido."
        
        if not isEmailValid(email): 
            errores += "Debe digitar un email válido."
        
        if not isPasswordValid(password):
            errores += "El password no cumple con los requisitos mínimos."

        if not declaracion == 'S':
            errores += "Debe aceptar los terminos legales del registro."

        if not errores:
            exito = "Su cuenta ha sido registrada."
            yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
            yag.send(to=email, subject="Activación de cuenta registro vacunación Covid-19.",
            contents="Bienvenido {0}, usa este link para activar tu cuenta. ".format(nombre + ' ' + apellidos))
            return redirect(url_for('login'))
            #return render_template('registro.html', exito=exito)
        else:
            return render_template('registro.html', errores=errores)