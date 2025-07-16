import os
from flask import Flask, request, render_template, redirect, url_for, session
from markupsafe import Markup
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey_jhair'  # Cambia esto en producción
app.debug = True

# Obtén la URI desde la variable de entorno
# --- INICIO: Configuración temporal para pruebas locales ---
# os.environ["MONGO_URI"] = "mongodb+srv://uni_postulante_user:jhairsiempreesseguro@clusterpostulantes.pytcwgu.mongodb.net/?retryWrites=true&w=majority&appName=clusterPostulantes"
# Quita la línea anterior antes de subir a GitHub o producción
# --- FIN: Configuración temporal ---
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise Exception("La variable de entorno MONGO_URI no está definida. Por favor, configúrala antes de ejecutar la app.")

try:
    client = MongoClient(MONGO_URI)
    db = client["oltp_postulantes"]
    usuarios = db["usuarios"]
    postulantes = db["postulantes"]
    print("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    print(f"❌ Error al conectar a MongoDB: {e}")
    usuarios = None
    postulantes = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        if not nombre or not email or not password:
            return render_template("register.html", error="Completa todos los campos.")
        if usuarios.find_one({"email": email}):
            return render_template("register.html", error="El correo ya está registrado.")
        hash_pw = generate_password_hash(password)
        usuarios.insert_one({"nombre": nombre, "email": email, "password": hash_pw})
        return render_template("register.html", success="¡Cuenta creada con éxito! Ahora puedes iniciar sesión.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = usuarios.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return render_template("login.html", error="Correo o contraseña incorrectos.")
        session['user_id'] = str(user['_id'])
        session['user_name'] = user['nombre']
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if postulantes is None:
        return "❌ No hay conexión a la base de datos. Intenta más tarde."
    if request.method == "POST":
        try:
            nuevo_postulante = {
                "IDHASH": request.form.get("IDHASH", "").strip(),
                "COLEGIO": request.form.get("COLEGIO", "").strip(),
                "COLEGIO_DEPA": request.form.get("COLEGIO_DEPA", "").strip(),
                "COLEGIO_PROV": request.form.get("COLEGIO_PROV", "").strip(),
                "COLEGIO_DIST": request.form.get("COLEGIO_DIST", "").strip(),
                "COLEGIO_PAIS": request.form.get("COLEGIO_PAIS", "").strip(),
                "COLEGIO_ANIO_EGRESO": request.form.get("COLEGIO_ANIO_EGRESO", "").strip(),
                "ESPECIALIDAD": request.form.get("ESPECIALIDAD", "").strip(),
                "ANIO_POSTULA": request.form.get("ANIO_POSTULA", "").strip(),
                "CICLO_POSTULA": request.form.get("CICLO_POSTULA", "").strip(),
                "DOMICILIO_DEPA": request.form.get("DOMICILIO_DEPA", "").strip(),
                "DOMICILIO_PROV": request.form.get("DOMICILIO_PROV", "").strip(),
                "DOMICILIO_DIST": request.form.get("DOMICILIO_DIST", "").strip(),
                "ANIO_NACIMIENTO": request.form.get("ANIO_NACIMIENTO", "").strip(),
                "NACIMIENTO_PAIS": request.form.get("NACIMIENTO_PAIS", "").strip(),
                "NACIMIENTO_DEPA": request.form.get("NACIMIENTO_DEPA", "").strip(),
                "NACIMIENTO_PROV": request.form.get("NACIMIENTO_PROV", "").strip(),
                "NACIMIENTO_DIST": request.form.get("NACIMIENTO_DIST", "").strip(),
                "SEXO": request.form.get("SEXO", "").strip(),
                "CALIF_FINAL": request.form.get("CALIF_FINAL", "").strip(),
                "INGRESO": request.form.get("INGRESO", "").strip(),
                "MODALIDAD": request.form.get("MODALIDAD", "").strip(),
                "FECHA_CORTE": request.form.get("FECHA_CORTE", "").strip(),
                "usuario": session.get('user_name', '')
            }
            postulantes.insert_one(nuevo_postulante)
            mensaje = Markup("<div style='background: #e1f8e6; border: 2px solid #81c784; border-radius: 18px; padding: 24px; margin: 40px auto; max-width: 400px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.08);'><h2 style='color: #388e3c;'>¡Postulante registrado con éxito!</h2><a href='/' style='display: inline-block; margin-top: 18px; background: linear-gradient(90deg, #ffd600 0%, #64b5f6 100%); color: #263238; font-size: 1.2em; font-weight: bold; border: none; border-radius: 16px; padding: 12px 32px; text-decoration: none; box-shadow: 0 4px 12px rgba(0,0,0,0.10); transition: background 0.3s, transform 0.2s;'>Registrar otro 🚀</a> <a href='/postulantes' style='display: inline-block; margin-top: 18px; margin-left: 10px; background: linear-gradient(90deg, #64b5f6 0%, #ffd600 100%); color: #263238; font-size: 1.1em; font-weight: bold; border: none; border-radius: 16px; padding: 10px 28px; text-decoration: none; box-shadow: 0 4px 12px rgba(0,0,0,0.10); transition: background 0.3s, transform 0.2s;'>Ver todos los postulantes 📋</a></div>")
            return mensaje
        except Exception as e:
            return f"❌ Error al registrar postulante: {e} <br><a href='/'>Volver</a>"
    return render_template("index.html", user=session.get('user_name', ''))

@app.route("/postulantes")
@login_required
def ver_postulantes():
    if postulantes is None:
        return "❌ No hay conexión a la base de datos. Intenta más tarde."
    lista = list(postulantes.find())
    return render_template("postulantes.html", postulantes=lista)

if __name__ == "__main__":
    print("🚀 Iniciando aplicación Flask en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
