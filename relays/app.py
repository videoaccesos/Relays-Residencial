import os
from flask import Flask, redirect, url_for
from flask_apscheduler import APScheduler
from flask_login import LoginManager, current_user

# Importa aquí tus blueprints
from api.auth    import auth_bp
from api.remote  import remote_bp
from api.admin   import admin_bp

# Importa tu modelo de usuario y la sesión
from models import User, SessionLocal

# Importa tus tareas periódicas
from tasks  import health_check

# --- FLASK APP SETUP ---
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', 'devkey')

# --- FLASK-LOGIN SETUP ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login llama a esta función con el valor que devuelve user.get_id().
    En tu modelo User, get_id() debería devolver username.
    """
    db = SessionLocal()
    user = db.query(User).filter_by(username=user_id).first()
    db.close()
    return user

# --- RUTA INDEX (home) ---
@app.route('/')
def index():
    # Si no está autenticado → login
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    # Si es admin → panel de admin
    if current_user.role == 'admin':
        return redirect(url_for('admin.panel'))
    # Si es operator → panel remoto
    return redirect(url_for('remote.remote_panel'))

# --- REGISTRAR BLUEPRINTS ---
app.register_blueprint(auth_bp)    # rutas de /login, /logout
app.register_blueprint(remote_bp)  # ruta /remote
app.register_blueprint(admin_bp)   # rutas /config, /config/*

# --- SCHEDULER / WATCHDOG ---
app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(
    id='watchdog',
    func=health_check,
    trigger='interval',
    seconds=int(os.getenv('WATCHDOG_INTERVAL', '60'))
)

# --- EJECUCIÓN ---
if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', '5002'))
    app.run(host='0.0.0.0', port=port)
