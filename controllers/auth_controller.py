# controllers/auth_controller.py

import re
from flask import redirect, url_for, flash, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from extensions import db, login_manager
from models.models import User

def validar_email(email):
    """Valida formato de email con regex."""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

# 1) Loader para flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register(form):
    """Registra un usuario nuevo."""
    nombre     = form.get('nombre').strip().title()
    correo     = form.get('correo').lower().strip()
    contrasena = form.get('contrasena')
    

    # Validaciones
    if not validar_email(correo):
        flash('El formato del email no es válido. Debe contener @', 'danger')
        return redirect(url_for('auth_bp.register_view'))
    
    if len(contrasena) < 6:
        flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
        return redirect(url_for('auth_bp.register_view'))
    
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
    correo     = form.get('correo').lower().strip()
    contrasena = form.get('contrasena')
    
    # Validar formato de email
    if not validar_email(correo):
        flash('El formato del email no es válido.', 'danger')
        return redirect(url_for('auth_bp.login_view'))
    
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
