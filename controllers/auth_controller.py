# controllers/auth_controller.py

from flask import redirect, url_for, flash, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from extensions import db, login_manager
from models.models import User

# 1) Loader para flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register(form):
    """Registra un usuario nuevo."""
    nombre     = form.get('nombre').strip().title()
    correo     = form.get('correo').lower()
    contrasena = form.get('contrasena')

    # Validación básica
    if User.query.filter_by(correo=correo).first():
        flash('El correo ya está registrado.', 'danger')
        return redirect(url_for('auth_bp.register_view'))

    user = User(
        nombre    = nombre,
        correo    = correo,
        contrasena= generate_password_hash(contrasena)
    )
    db.session.add(user)
    db.session.commit()

    flash('Cuenta creada. Por favor inicia sesión.', 'success')
    return redirect(url_for('auth_bp.login_view'))

def login_usuario(form):
    """Valida credenciales e inicia sesión."""
    correo     = form.get('correo').lower()
    contrasena = form.get('contrasena')
    user = User.query.filter_by(correo=correo).first()

    if user and check_password_hash(user.contrasena, contrasena):
        login_user(user)
        flash('Sesión iniciada.', 'success')

        # Redirige según rol
        if user.rol == 'admin':
            return redirect(url_for('admin_bp.panel'))
        else:
            # mantiene el ?next= si existe
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('graph_bp.consulta'))

    flash('Credenciales incorrectas.', 'danger')
    return redirect(url_for('auth_bp.login_view'))

def logout_usuario():
    """Cierra la sesión activa."""
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('auth_bp.login_view'))
