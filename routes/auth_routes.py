# routes/auth_routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from controllers.auth_controller import register, login_usuario, logout_usuario

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET','POST'])
def register_view():
    if request.method == 'POST':
        return register(request.form)
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET','POST'])
def login_view():
    if request.method == 'POST':
        return login_usuario(request.form)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout_view():
    return logout_usuario()
