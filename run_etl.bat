@echo off
REM Ve a la carpeta etl
cd etl

REM Construye la imagen Docker (solo si no existe o hay cambios)
docker build -t etl-postulantes .

REM Ejecuta el ETL en Docker
docker run --rm -e SECRET_KEY="tu_clave" -e MONGO_URI="mongodb+srv://uni_postulante_user:jhairsiempreesseguro@clusterpostulantes.pytcwgu.mongodb.net/?retryWrites=true&w=majority&appName=clusterPostulantes" etl-postulantes

pause 