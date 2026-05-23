# Usamos la imagen oficial ligera de Python basada en el Stack del proyecto
FROM python:3.11-slim

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero el archivo de requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias oficiales
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente de la app al contenedor
COPY src/ ./src/

# Exponemos el puerto en el que corre Flask por defecto
EXPOSE 5000

# Comando por defecto para arrancar la API
CMD ["python", "src/app.py"]