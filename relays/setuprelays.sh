#!/usr/bin/env bash

# Atención: este script debe ejecutarse con Bash, NO con Python.
# Uso:
#   chmod +x setuprelays.sh
#   ./setuprelays.sh

set -euo pipefail

# 1. Instalar / actualizar dependencias
echo "Instalando dependencias desde requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Dependencias instaladas."

# 2. Variables de entorno recomendadas (define estas en tu shell o .env)
cat <<EOF
export FLASK_ENV=production
export FLASK_CONFIG=config.yaml
export FLASK_PORT=5002        # Puerto para esta aplicación
export WATCHDOG_INTERVAL=60   # Segundos entre checks de salud
export WATCHDOG_THRESHOLD=120 # Umbral para alerta de watchdog
EOF

echo "Recuerda activar el entorno virtual: source relays/bin/activate"