# Imagen base con Python
FROM python:3.11-slim

# Evita que Python guarde archivos .pyc y use el buffer de salida
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (opcional pero útil para psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Copiar los archivos de requerimientos
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el código del proyecto
COPY . /app/

# Exponer el puerto donde correrá Django
EXPOSE 8000

# Comando por defecto para correr la app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
