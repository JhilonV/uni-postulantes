from flask import Flask, request, render_template, Markup
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True  # Activa modo debug de Flask

# Conexión directa a MongoDB Atlas (OLTP)
try:
    client = MongoClient("mongodb+srv://uni_postulante_user:jhairseguro14@clusterpostulantes.pytcwgu.mongodb.net/?retryWrites=true&w=majority&appName=clusterPostulantes")
    db = client["oltp_postulantes"]
    collection = db["postulantes"]
    print("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    print(f"❌ Error al conectar a MongoDB: {e}")
    collection = None

@app.route("/", methods=["GET", "POST"])
def index():
    carreras = [
        "Ingeniería de Sistemas", "Psicología", "Medicina", "Derecho", "Administración",
        "Arquitectura", "Contabilidad", "Ingeniería Civil", "Ingeniería Industrial",
        "Educación", "Economía", "Marketing", "Otra"
    ]
    if request.method == "POST":
        if collection is None:
            return "❌ No hay conexión a la base de datos. Intenta más tarde."
        try:
            nuevo_postulante = {
                "nombre": request.form["nombre"],
                "edad": int(request.form["edad"]),
                "genero": request.form["genero"],
                "carrera": request.form["carrera"]
            }
            collection.insert_one(nuevo_postulante)
            mensaje = Markup(f'''
            <div style="background: #e1f8e6; border: 2px solid #81c784; border-radius: 18px; padding: 24px; margin: 40px auto; max-width: 400px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
                <div style="margin-bottom: 10px;">
                  <svg width="60" height="68" viewBox="0 0 80 90" fill="none" style="vertical-align: middle;">
                    <ellipse cx="40" cy="50" rx="30" ry="35" fill="#e3f2fd"/>
                    <ellipse cx="40" cy="38" rx="24" ry="28" fill="#fff"/>
                    <ellipse cx="40" cy="38" rx="18" ry="20" fill="#e0f7fa"/>
                    <ellipse cx="40" cy="38" rx="10" ry="12" fill="#263238"/>
                    <ellipse cx="36" cy="36" rx="2" ry="3" fill="#fff"/>
                    <ellipse cx="44" cy="36" rx="2" ry="3" fill="#fff"/>
                    <rect x="32" y="65" width="16" height="10" rx="5" fill="#b3e5fc"/>
                  </svg>
                </div>
                <h2 style="color: #388e3c; font-family: 'Comic Sans MS', cursive;">¡Postulante registrado con éxito!</h2>
                <p style="color: #1976d2; font-size: 1.1em;">🤖 Jhair dice: <b>¡Sigue aprendiendo y registrando más amigos!</b></p>
                <a href="/" style="display: inline-block; margin-top: 18px; background: linear-gradient(90deg, #ffd600 0%, #64b5f6 100%); color: #263238; font-size: 1.2em; font-weight: bold; border: none; border-radius: 16px; padding: 12px 32px; text-decoration: none; box-shadow: 0 4px 12px rgba(0,0,0,0.10); transition: background 0.3s, transform 0.2s;">Registrar otro 🚀</a>
                <a href="/postulantes" style="display: inline-block; margin-top: 18px; margin-left: 10px; background: linear-gradient(90deg, #64b5f6 0%, #ffd600 100%); color: #263238; font-size: 1.1em; font-weight: bold; border: none; border-radius: 16px; padding: 10px 28px; text-decoration: none; box-shadow: 0 4px 12px rgba(0,0,0,0.10); transition: background 0.3s, transform 0.2s;">Ver todos los postulantes 📋</a>
            </div>
            ''')
            return mensaje
        except Exception as e:
            return f"❌ Error al registrar postulante: {e} <br><a href='/'>Volver</a>"
    return render_template("index.html", carreras=carreras)

@app.route("/postulantes")
def ver_postulantes():
    if collection is None:
        return "❌ No hay conexión a la base de datos. Intenta más tarde."
    postulantes = list(collection.find())
    tabla = '''
    <html>
    <head>
      <title>Lista de Postulantes</title>
      <meta charset="UTF-8">
      <style>
        body { background: linear-gradient(120deg, #e0f7fa 0%, #fffde7 100%); font-family: 'Comic Sans MS', cursive; }
        .tabla-postulantes { margin: 40px auto; background: #fff; border-radius: 18px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); padding: 24px; max-width: 700px; }
        h2 { color: #1976d2; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 18px; }
        th, td { padding: 10px 8px; text-align: center; border-bottom: 1px solid #b3e5fc; }
        th { background: #b3e5fc; color: #263238; font-size: 1.1em; }
        tr:last-child td { border-bottom: none; }
        .volver { display: inline-block; margin-top: 18px; background: linear-gradient(90deg, #ffd600 0%, #64b5f6 100%); color: #263238; font-size: 1.1em; font-weight: bold; border: none; border-radius: 16px; padding: 10px 28px; text-decoration: none; box-shadow: 0 4px 12px rgba(0,0,0,0.10); transition: background 0.3s, transform 0.2s; }
        .volver:hover { background: linear-gradient(90deg, #64b5f6 0%, #ffd600 100%); transform: scale(1.05); }
      </style>
    </head>
    <body>
      <div class="tabla-postulantes">
        <h2>Lista de Postulantes Registrados</h2>
        <table>
          <tr>
            <th>Nombre</th>
            <th>Edad</th>
            <th>Género</th>
            <th>Carrera</th>
          </tr>
    '''
    for p in postulantes:
        tabla += f"<tr><td>{p.get('nombre','')}</td><td>{p.get('edad','')}</td><td>{p.get('genero','')}</td><td>{p.get('carrera','')}</td></tr>"
    tabla += '''
        </table>
        <a class="volver" href="/">Registrar otro</a>
      </div>
    </body>
    </html>
    '''
    return tabla

if __name__ == "__main__":
    print("🚀 Iniciando aplicación Flask en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
