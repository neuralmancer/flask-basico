from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/mensaje')
def mensaje():
    return "Escribe un mensaje aquí"

@app.route('/usuario/<usuario>')
def user_name(usuario):
    return "Hola {0}!".format(usuario)

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
