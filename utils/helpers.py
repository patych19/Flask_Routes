from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def roles_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol != role:
                flash('Acceso denegado.', 'danger')
                return redirect(url_for('auth_bp.login_view'))
            return f(*args, **kwargs)
        return wrapped
    return decorator
