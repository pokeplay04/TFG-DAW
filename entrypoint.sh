#!/bin/bash
set -e

# Crear directorio de logs si no existe
mkdir -p /var/log

# Crear archivos de log si no existen y darles permisos
touch /var/log/friend_suggestions.log /var/log/trends.log
chmod 666 /var/log/*.log

# Iniciar cron
echo "Starting cron..."
service cron start

# Forzar la carga del cronjob
crontab /etc/cron.d/every-hour-job || {
  echo "Error al cargar crontab. Revisando archivo..."
  cat /etc/cron.d/every-hour-job
}

# Aplicar migraciones
python manage.py migrate --noinput

# Ejecutar comando principal (el que venga de CMD)
exec "$@"