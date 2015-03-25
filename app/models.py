from werkzeug.security import generate_password_hash, check_password_hash
from . import db, lm
from flask.ext.login import UserMixin


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
