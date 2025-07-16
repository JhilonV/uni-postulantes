import pymongo
import os

# Obtén la URI desde la variable de entorno
mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    raise Exception("La variable de entorno MONGO_URI no está definida. Por favor, configúrala antes de ejecutar el ETL.")

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
