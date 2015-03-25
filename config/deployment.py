import os

DEBUG = True
SECRET_KEY = 'cadena_secreta'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__) , '../datos.sqlite')
