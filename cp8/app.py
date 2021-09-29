from flask import Flask, render_template

app = Flask(__name__)

@app.route('/registro')
def registro():
    return render_template('registro.html')