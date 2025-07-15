import pymongo
import json
from cryptography.fernet import Fernet
import os

# Clave en variable de entorno (ej. desde .env o Docker)
key = os.environ.get("SECRET_KEY").encode()
fernet = Fernet(key)

# Leer y desencriptar credenciales
with open("etl/config.enc.json", "rb") as f:
    encrypted = f.read()
config = json.loads(fernet.decrypt(encrypted).decode())

try:
    # Conexión a MongoDB Atlas
    client = pymongo.MongoClient(config["MONGO_URI"])
    oltp = client["oltp_postulantes"]["postulantes"]
    olap = client["olap_postulantes"]["analytics"]
    print("✅ Conectado a MongoDB Atlas para ETL")

    # Proceso ETL: extraer - transformar - cargar
    count = 0
    for doc in oltp.find():
        doc["rango_edad"] = "18-20" if 18 <= doc["edad"] <= 20 else "21+"
        doc.pop("_id", None)  # Eliminar _id para evitar duplicados
        olap.insert_one(doc)
        count += 1
    print(f"✅ ETL finalizado con éxito. {count} documentos migrados.")
except Exception as e:
    print(f"❌ Error en el proceso ETL: {e}")
