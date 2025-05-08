# api/admin.py

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from config import CONFIG

admin_bp = Blueprint('admin', __name__, url_prefix='/config')

# Cualquier petición a /config/* requiere estar logueado...
@admin_bp.before_request
@login_required
def require_login():
    pass  # el decorador ya redirige a /login si no estás autenticado

# ...y ser admin
@admin_bp.before_request
def require_admin():
    if current_user.role != 'admin':
        abort(403, description="Acceso denegado")

# Panel principal de configuración
@admin_bp.route('/')
def panel():
    residences = CONFIG.get('residences', [])
    return render_template('admin_config.html', residences=residences)
