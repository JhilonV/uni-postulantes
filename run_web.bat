@echo off
REM Configura la variable de entorno (ajusta si tu URI cambia)
set MONGO_URI=mongodb+srv://uni_postulante_user:jhairsiempreesseguro@clusterpostulantes.pytcwgu.mongodb.net/?retryWrites=true^&w=majority^&appName=clusterPostulantes

REM Ejecuta la app Flask
cd app
python app.py

pause 