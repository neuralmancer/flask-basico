from flask import render_template, redirect, url_for, request
from flask.ext.login import login_user, logout_user, login_required
from ..models import Usuario
from . import main
from .forms import LoginForm


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usr = Usuario.query.filter_by(nombre=form.usuario.data).first()
        if usr is None or not usr.verify_password(form.password.data):
            return redirect(url_for('main.login', **request.args))
        login_user(usr, form.password.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/protected')
@login_required
def protected():
    return render_template('protected.html')
