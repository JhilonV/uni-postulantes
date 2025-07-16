import pymongo
import os
import json
from cryptography.fernet import Fernet

# Desencriptar configuración
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("La variable de entorno SECRET_KEY no está definida. Por favor, configúrala antes de ejecutar el ETL.")

with open("etl/config.enc.json", "rb") as f:
    encrypted = f.read()
fernet = Fernet(SECRET_KEY.encode() if isinstance(SECRET_KEY, str) else SECRET_KEY)
config = json.loads(fernet.decrypt(encrypted).decode())

mongo_uri = config.get("MONGO_URI")
if not mongo_uri:
    raise Exception("No se encontró MONGO_URI en la configuración desencriptada.")

try:
    # Conexión a MongoDB Atlas
    client = pymongo.MongoClient(mongo_uri)
    oltp = client["oltp_postulantes"]["postulantes"]  # Origen (NO se modifica)
    destino = client["mi_nueva_base"]["postulantes_transformados"]  # Nueva base y colección
    print("✅ Conectado a MongoDB Atlas para ETL")

    # Proceso ETL: extraer - transformar - cargar
    count = 0
    for doc in oltp.find():
        doc["rango_edad"] = "18-20" if 18 <= doc.get("edad", 0) <= 20 else "21+"
        doc.pop("_id", None)  # Eliminar _id para evitar duplicados
        destino.insert_one(doc)
        count += 1
    print(f"✅ ETL finalizado con éxito. {count} documentos migrados a la nueva base de datos.")
except Exception as e:
    print(f"❌ Error en el proceso ETL: {e}")
