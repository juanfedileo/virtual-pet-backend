# Imagen base con Python
FROM python:3.11-slim

# Evita que Python guarde archivos .pyc y use el buffer de salida
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (psycopg2 necesita libpq-dev y gcc)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc netcat-traditional && \
    apt-get clean

# Copiar los archivos de requerimientos
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el código del proyecto
COPY . /app/

# Copiar script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto donde correrá Django
EXPOSE 8000

# Usar el entrypoint que hace migraciones + arranca el server
ENTRYPOINT ["/entrypoint.sh"]
