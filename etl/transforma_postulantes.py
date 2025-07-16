import json

with open('postulantes_origen.json', encoding='utf-8') as f:
    docs = [json.loads(line) for line in f]

for doc in docs:
    edad = doc.get('edad', 0)
    doc['rango_edad'] = "18-20" if 18 <= edad <= 20 else "21+"
    doc.pop('_id', None)

with open('postulantes_transformados.json', 'w', encoding='utf-8') as f:
    for doc in docs:
        f.write(json.dumps(doc, ensure_ascii=False) + '\n')

print("Transformación completada. Archivo: postulantes_transformados.json") 