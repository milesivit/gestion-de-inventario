# EFI Milena

Este proyecto está alojado en GitHub y se puede clonar y correr localmente siguiendo los pasos descritos a continuación.

## Clonar y correr el proyecto

```bash
# Clonar el proyecto
git clone https://github.com/milesivit/EFI-Milena
cd EFI-Milena

# Crear el entorno virtual
python3 -m venv env

# Activar el entorno virtual
source env/bin/activate

# Instalar requerimientos
pip install -r requirements.txt

# Correr el proyecto
flask run --reload
```

# Endpoints de la API

A continuación se describen los principales endpoints de la API con ejemplos de solicitud y respuesta.

## Autenticación
### ATENCIÓN CREAR USUARIO ADMINISTRADOR CON FLASK SHELL

Obtener token de autenticación
- Método: POST
- Endpoint: `localhost:5000/login`
- Cuerpo de la solicitud en el auth/basic:

```bash
{
    "username": "Admin",
    "password": "admin"
}
```

Ejemplo de respuesta:

```bash
{
    "Token": "<tu_token_de_autenticacion>"
}
```

### Creación de usuarios 
- Método: POST
- Endpoint: `localhost:5000/users`
- Pegar token de administrador en bearer.
- Cuerpo de la solicitud en el body/json:

```bash
{
    "nombre_usuario": "Matias",
    "password": "matiiii"
}
```
Ejemplo de respuesta:

```bash
{
  "Usuario Creado": "Matias"
}
```

### Ver lista de usuarios
- Método: GET
- Endpoint: `localhost:5000/users`
- Pegar token de administrador en auth/bearer.
- Pegar token de usuario en auth/bearer pero tendras limitaciones al no ser admin.

Ejemplo de respuesta si sos admin:

```bash
  {
    "id": 10,
    "is_admin": null,
    "password_hash": "pbkdf2:sha256:600000$8aTB3wMS$70c0174c4ec2b496d07734c070ad3dcb512c7f0d7274f8ee944e01715fc3bb9d",
    "username": "Milena"
  }
```
Ejemplo de respuesta si no sos admin:

```bash
{
    "username": "usuario 2"
  }
```

### CRUD en modelo

### Ver modelos
- Método: GET
- Endpoint: `localhost:5000/modelo`
- Pegar token de administrador en auth/bearer.
- Pegar token de usuario en auth/bearer pero tendras limitaciones al no ser admin.

### Crear modelos
- Método: POST
- SOLO USUARIO ADMIN
- Tiene que haber creado si o si un fabricante en la DB.
- Endpoint: `localhost:5000/modelo`
- Pegar token en bearer.
- Cuerpo de la solicitud en el body/json:

```bash
{
    "nombre": "iPhone 15",
    "activo": true,
    "marca_id": 1,
    "fabricante_id": 1
}
```

### Modificar modelos
- Método: PUT
- SOLO USUARIO ADMIN
- Tiene que haber creado si o si un fabricante en la DB.
- Endpoint: `localhost:5000/modelo`
- Pegar token en bearer.
- Cuerpo de la solicitud en el body/json:

```bash
{
  "id": 1,
  "nombre": "Nuevo Nombre del Modelo",
  "activo": true,
  "marca_id": 2,
  "fabricante_id": 3
 }
```

### Eliminar modelos
- Método: DELETE
- SOLO USUARIO ADMIN
- SE INACTIVA EL ID COPIANDO ESTA URL Y PONIENDO EL NUMERO DE ID QUE DESEAMOS DESACTIVAR.
- Endpoint: `http://localhost:5000/modelo?id=1`
- Pegar token en bearer.

Ejemplo de respuesta:
```bash
{
  "Mensaje": "Modelo marcado como inactivo correctamente."
}
```

### Demas vistas
- Método: GET
- Endpoint: `localhost:5000/caracteristica`
- Endpoint: `localhost:5000/accesorio`
- Endpoint: `localhost:5000/categorias`
- Endpoint: `localhost:5000/equipos`
- Endpoint: `localhost:5000/proveedor`
- Endpoint: `localhost:5000/clientes`
- Endpoint: `localhost:5000/inventario`
- Endpoint: `localhost:5000/marca`
- Endpoint: `localhost:5000/fabricante`
