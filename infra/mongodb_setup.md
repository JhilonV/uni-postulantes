# MongoDB Atlas Setup (Infraestructura como Código)

## 1. Crear bases de datos y colecciones

Puedes ejecutar estos comandos en el MongoDB Shell (mongosh) o desde la consola de Atlas:

```js
// Crear base OLTP y colección de postulantes
use oltp_postulantes
// Crea la colección si no existe
if (!db.getCollectionNames().includes('postulantes')) {
  db.createCollection('postulantes');
}

// Crear base OLAP y colección analytics
use olap_postulantes
if (!db.getCollectionNames().includes('analytics')) {
  db.createCollection('analytics');
}
```

## 2. Crear índices recomendados

```js
use oltp_postulantes
// Índice por nombre
db.postulantes.createIndex({ nombre: 1 })
// Índice por carrera
db.postulantes.createIndex({ carrera: 1 })

use olap_postulantes
// Índice por rango_edad
db.analytics.createIndex({ rango_edad: 1 })
```

## 3. Crear usuario no administrativo

En la consola de Atlas, ve a **Database Access** y crea un usuario con:
- Nombre: `uni_postulante_user`
- Contraseña: (elige una segura)
- Permisos: Solo lectura/escritura en `oltp_postulantes` y `olap_postulantes` (no admin global)

O usa el siguiente comando en mongosh (ajusta la contraseña):

```js
use admin
// Crea usuario con permisos solo sobre las bases necesarias
// Reemplaza TU_PASSWORD por una contraseña segura
// Ejecuta esto una sola vez

db.createUser({
  user: "uni_postulante_user",
  pwd: "TU_PASSWORD",
  roles: [
    { role: "readWrite", db: "oltp_postulantes" },
    { role: "readWrite", db: "olap_postulantes" }
  ]
})
```

## 4. Permisos y buenas prácticas
- No uses el usuario admin para la app ni el ETL.
- Usa el usuario `uni_postulante_user` en tus URIs de conexión.
- No compartas la contraseña en público.

## 5. Referencias
- [MongoDB Atlas Docs: Database Users](https://www.mongodb.com/docs/atlas/security-add-mongodb-users/)
- [MongoDB createUser](https://www.mongodb.com/docs/manual/reference/method/db.createUser/)
