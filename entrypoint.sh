#!/bin/sh

echo "Esperando a que PostgreSQL esté disponible..."
while ! nc -z postgres_db 5432; do
  sleep 1
done
echo "PostgreSQL está listo"

echo "Aplicando migraciones..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
