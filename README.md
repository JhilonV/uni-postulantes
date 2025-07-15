# Proyecto Inteligencia de Negocios: UNI Postulantes

## Objetivo
Registrar postulantes a la UNI, migrar los datos a un modelo analítico (OLAP) y visualizar indicadores clave para la toma de decisiones usando Power BI.

---

> **Nota importante para el profesor:**
> - **Cluster Flex:** Por limitación de la API de MongoDB Atlas, el cluster gratuito Flex debe crearse manualmente desde la consola web. El resto de la infraestructura (proyecto, usuario, whitelist) se gestiona como código (IaC) con Terraform.
> - **MongoDB es NoSQL:** No utiliza archivos SQL, tablas, constraints ni sinónimos. En su lugar, se crean colecciones e índices usando comandos de MongoDB, documentados en `infra/mongodb_setup.md`.

---

## Estructura del repositorio
- `app/`: Aplicación Flask para registro de postulantes
- `etl/`: Proceso ETL para migrar datos de OLTP a OLAP
- `dashboard/`: Plantilla y recursos para Power BI
- `docs/`: Informe y diapositivas del proyecto
- `infra/`: Infraestructura y guías

## Ejemplo de documento de postulante en MongoDB
```json
{
  "nombre": "Ana",
  "edad": 19,
  "genero": "Femenino",
  "carrera": "Ingeniería de Sistemas",
  "rango_edad": "18-20"
}
```

## Requisitos
- Python 3.8+
- Flask
- PyMongo
- cryptography
- MongoDB Atlas (OLTP y OLAP)
- Power BI Desktop
- Docker (para ETL)

## Instalación y ejecución
1. Clona el repositorio:
   ```
   git clone https://github.com/tuusuario/uni-postulantes.git
   cd uni-postulantes
   ```
2. Instala dependencias:
   ```
   pip install flask pymongo cryptography
   ```
3. Ejecuta la app Flask:
   ```
   cd app
   python app.py
   ```
   Abre [http://127.0.0.1:5000](http://127.0.0.1:5000) en tu navegador.

## Proceso ETL
1. Configura la clave y credenciales en `etl/config.enc.json` (ver `encrypt_config.py`).
2. Ejecuta el ETL en Docker:
   ```
   cd etl
   docker build -t etl-postulantes .
   docker run --rm -e SECRET_KEY="<tu_clave>" etl-postulantes
   ```
   Los datos se migrarán de `oltp_postulantes.postulantes` a `olap_postulantes.analytics`.

## Dashboard Power BI
1. Abre `dashboard/UNI_Postulantes.pbip` en Power BI Desktop.
2. Conecta a MongoDB Atlas (OLAP) y selecciona la colección `analytics`.
3. Crea las visualizaciones:
   - Total de postulantes por carrera
   - Promedio de edad por carrera
   - Cantidad por rango de edad

## ¿Cómo correr este proyecto en otro computador?

1. Clona el repositorio:
   ```
   git clone https://github.com/TU_USUARIO/TU_REPO.git
   cd TU_REPO
   ```
2. Instala dependencias:
   ```
   pip install flask pymongo cryptography
   ```
3. Configura las credenciales y la clave secreta (SECRET_KEY) para desencriptar el archivo `etl/config.enc.json`.
4. Ejecuta la app Flask:
   ```
   cd app
   python app.py
   ```
   Abre [http://127.0.0.1:5000](http://127.0.0.1:5000) en tu navegador.
5. Ejecuta el ETL:
   ```
   cd etl
   python etl.py
   ```
   o con Docker:
   ```
   docker build -t etl-postulantes .
   docker run --rm -e SECRET_KEY="tu_clave" etl-postulantes
   ```
6. Abre Power BI Desktop y abre el archivo PBIP. Conecta a MongoDB Atlas usando el usuario y contraseña no admin.

---

## Contribución
Puedes mejorar el proyecto enviando PRs o issues.

## Licencia
MIT
