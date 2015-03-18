from flask import Flask, render_template
#from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'muppet'
#bootstrap = Bootstrap(app)

class NameForm(Form):
    nombre = StringField('Escribe tu nombre:', validators=[Required()])
    submit = SubmitField('Enviar!')

@app.route('/')
def index():
    return "Hola Mundo!"
    #return render_template("index.html")

#ejemplo de forma
@app.route('/forma', methods=['GET', 'POST'])
def forma():
    nombre = None
    form = NameForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        form.nombre.data = ''
    return render_template("forma.html", form = form, nombre = nombre)

#template que se llena desde un archivo de texto
@app.route('/archivo')
def archivo():
    texto = []
    f = open('texto.txt', 'r')
    for linea in f:
        linea = linea.strip()
        texto.append(linea)
    f.close()
    return render_template("archivo.html", texto = texto)

#ejemplo pasar valor por url, en template
@app.route('/usuario/<usuario>')
def user_name(usuario):
    return render_template("usuario.html", usuario = usuario)

#404 personalizado
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
