@echo off
REM ==========================================
REM Ejecuta la app Flask en Docker
REM ==========================================
cd app

REM Pide la URI de MongoDB si no está definida
if "%MONGO_URI%"=="" (
    set /p MONGO_URI=Introduce la URI de MongoDB (Atlas o local):
)

REM Construye la imagen Docker
docker build -t flask-app .

REM Ejecuta el contenedor Docker
REM -p 5000:5000 expone el puerto 5000
REM -e MONGO_URI pasa la variable de entorno

docker run --rm -p 5000:5000 -e MONGO_URI="%MONGO_URI%" flask-app

pause 