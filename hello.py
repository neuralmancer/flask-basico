from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cadena_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datos.sqlite"
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'login'


class LoginForm(Form):
    usuario = StringField("Usuario:", validators=[Required(), Length(1, 16)])
    password = PasswordField('Contraseña', validators=[Required()])
    recordarme = BooleanField("Recordarme")
    submit = SubmitField("Entrar")

class Usuario(UserMixin, db.Model):
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


@lm.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usr = Usuario.query.filter_by(nombre=form.usuario.data).first()
        if usr is None or not usr.verify_password(form.password.data):
            return redirect(url_for('login', **request.args))
        login_user(usr, form.password.data)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

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
    if Usuario.query.filter_by(nombre='omar').first() is None:
        Usuario.registra('omar','muppets')
    app.run(debug=True)
