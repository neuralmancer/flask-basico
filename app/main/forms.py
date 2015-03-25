from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length


class LoginForm(Form):
    usuario = StringField("Usuario:", validators=[Required(), Length(1, 16)])
    password = PasswordField('Contraseña', validators=[Required()])
    recordarme = BooleanField("Recordarme")
    submit = SubmitField("Entrar")
