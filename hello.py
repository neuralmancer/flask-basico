from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template
#from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length

from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cadena_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datos.sqlite"

db = SQLAlchemy(app)
#bootstrap = Bootstrap(app)

class NameForm(Form):
    nombre = StringField('Escribe tu nombre:', validators=[Required(),
                                                            Length(1,16)])
    submit = SubmitField('Enviar!')

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def registra(usuario, password):
        user = Usuario(nombre=usuario)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return "{}".format(self.nombre)


@app.route('/')
def index():
    return "Hola Mundo!"

#ejemplo de forma
@app.route('/forma', methods=['GET', 'POST'])
def forma():
    nombre = None
    form = NameForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        form.nombre.data = ''
        if Usuario.query.filter_by(nombre=nombre).first() is None:
            db.session.add(Usuario(nombre=nombre))
            db.session.commit()
    return render_template("forma.html", form = form, nombre = nombre)

@app.route('/todos')
def todos():
    lst = []
    result = Usuario.query.all()
    for lista in result:
        lst.append(lista)
    return render_template("todos.html", lst=lst)

@app.route('/sql')
def todos_sql():
    result = db.engine.execute("select * from usuarios")
    lst = []
    for lista in result:
        lst.append(lista)
    return render_template("todos.html", lst=lst)

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
    db.create_all()
    app.run(debug=True)
