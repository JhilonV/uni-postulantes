# Dockerfile para la app Flask
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la app
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir flask markupsafe pymongo

# Expone el puerto 5000
EXPOSE 5000

# Variable de entorno para la URI de MongoDB
ENV MONGO_URI=""

# Comando para ejecutar la app
CMD ["python", "app.py"] 