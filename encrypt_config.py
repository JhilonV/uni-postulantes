from cryptography.fernet import Fernet
import json

# Generar clave
key = Fernet.generate_key()
fernet = Fernet(key)

# ⚠️ Reemplaza esta URI con tu propia conexión de MongoDB Atlas
config = {
    "MONGO_URI": "mongodb+srv://jneciosupj:Devilman1414@clusterpostulantes.pytcwgu.mongodb.net/?retryWrites=true&w=majority&appName=clusterPostulantes"
}

# Encriptar el diccionario
encrypted = fernet.encrypt(json.dumps(config).encode())

# Guardar archivo en etl/
with open("etl/config.enc.json", "wb") as f:
    f.write(encrypted)

# Mostrar la clave (la usarás como variable de entorno)
print("SECRET_KEY =", key.decode())
