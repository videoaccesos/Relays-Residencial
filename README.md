# Relays-Residencial
proyecto desarrollo de aplicacion relays residencial
# Relay Accesos

Aplicación web para gestionar remotamente múltiples tarjetas de relés (Dingtian, SmartDen-16R, Panel Chino, etc.) usando Flask, SQLAlchemy y un frontend ligero.

---

## 📋 Características

- **CRUD de residencias y relés** desde un CSV (`seed_from_csv.py`) o migraciones.
- **Autenticación** con Flask-Login (operadores).
- **API REST**:
  - `GET /api/residences`  
  - `GET /api/residences/<id>/relays`
  - `POST /api/execute` → controla un relé y devuelve el comando `curl`.
- **Backend**:  
  - Gestión de distintos protocolos en `device_manager.py` (HTML, XML, CGI, Arduino).  
  - Logs en BD de cada comando ejecutado.
- **Frontend**:  
  - `templates/operator.html`  
  - `static/js/remote.js` para interactuar con la API.
- **Migraciones** con Flask-Migrate/Alembic.
- **Seed** de datos desde CSV.

---

## 🚀 Instalación y puesta en marcha

1. **Clona el repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/relay-accesos.git
   cd relay-accesos
Crea y activa un virtualenv


python3 -m venv .venv
source .venv/bin/activate
Instala dependencias


pip install -r requirements.txt
Variables de entorno
Crea un fichero .env en la raíz con al menos:


FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=una_clave_segura
DATABASE_URL=sqlite:///data.db
FLASK_PORT=5002
(Opcional: WATCHDOG_INTERVAL, WATCHDOG_THRESHOLD, etc.)

Inicializa la base de datos y migraciones

flask db init
flask db migrate -m "Inicial"
flask db upgrade
Carga datos de ejemplo

./seed_from_csv.py
Arranca la aplicación


python app.py
Abre 👉 http://localhost:5002/ e ingresa como operador.

📂 Estructura de directorios

relay-accesos/
├── app.py
├── config.py
├── requirements.txt
├── seed_from_csv.py
├── migrations/           # Alembic
├── data.db               # SQLite (generado)
├── models.py
├── device_manager.py
├── api/
│   ├── auth.py
│   └── remote.py
├── static/
│   └── js/
│       └── remote.js
└── templates/
    ├── base.html
    ├── login.html
    └── operator.html
app.py: Arranque de Flask, registro de Blueprints y LoginManager.

config.py: Configuración por defecto, lee .env.

models.py: Definición de User, Residence, Plate, Relay, Log.

device_manager.py: Lógica para hablar con cada tipo de tarjeta.

api/:

auth.py: login/logout.

remote.py: endpoints de panel y API de relés.

seed_from_csv.py: Script para poblar residences, plates y relays desde CSV.

migrations/: Versionado de esquema con Alembic.

static/js/remote.js: Lógica AJAX y renderizado de la UI.

templates/: Plantillas Jinja2.

🗃️ CSV de semillas
Fichero: Relacion de Relays.csv

Encabezados:

Privada, auth_user, dyndns, Tipo de Tarjeta, auth_pw, Relay 1, Relay 2, …, Relay 16
Delimitador: , (puede ajustarse a ; si lo prefieres).

Comportamiento: Filas con Relay X = nada se omiten. Actualiza credenciales si cambian.

🔧 Configuración avanzada
Timeout de requests: 5 s (en device_manager.py).

Retries: Por defecto los de requests.

Watchdog: Variables WATCHDOG_INTERVAL y WATCHDOG_THRESHOLD en setuprelays.sh (si usas flask_apscheduler).

Logging:

Nivel DEBUG en entorno development.

Logs de control en tabla logs.

📄 Migraciones
Las migraciones Alembic están en migrations/. Para ver el modelo ER simplificado, echa un ojo a:


cat migrations/versions/<revision>_*.py
diagrama ER básico:


+-------------+      +----------+     +--------+
| Residence   |1----*| Relay    |     | Plate  |
|-------------|      |----------|     |--------|
| id PK       |      | id PK    |     | id PK  |
| name        |      | res_id FK|     | desc   |
| url_base    |      | relay_id |     | url_tmplt |
| type        |      | cmd_tmplt|
| dyndns      |
| auth_user   |
| auth_pw     |
+-------------+
            \
             \
              *----1  +------+
                     | Log  |
                     |------|
                     | id   |
                     | ts   |
                     | user |
                     | …    |
                     +------+
