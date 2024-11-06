from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import get_jwt, jwt_required

from app import db

# Importa los modelos y esquemas necesarios
from models import Accesorio, Categoria, Equipo, Caracteristica, Inventario, Cliente, Proveedor, Modelo, Marca, Fabricante
from schemas import (
    AcessorioSchema,
    AcessorioMinimalSchema,
    CategoriaMinimalSchema,
    CategoriaSchema,
    EquipoMinimalSchema,
    EquipoSchema,
    CaracteristicaSchema,
    CaracteristicaMinimalSchema,
    ProveedorMinimalSchema,
    ProveedorSchema,
    ClienteMinimalSchema,
    ClienteSchema,
    InventarioSchema,
    InventarioMinimalSchema,
    ModeloSchema,
    MarcaSchema,
    FabricanteSchema,
    ModeloMinimalSchema,
    FabricanteMinimalSchema,
    MarcaMinimalSchema,
)

# Crea un Blueprint llamado "equipo" para organizar rutas relacionadas con equipos, categorías y accesorios
equipo_bp = Blueprint("equipo", __name__)


# Ruta para obtener todos los accesorios
@equipo_bp.route("/accesorio", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def accesorios():
    # Obtiene datos adicionales del token JWT
    additional_data = get_jwt()
    # Extrae el permiso de administrador del token, asignando False si no está presente
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Accesorio
    accesorio = Accesorio.query.all()
    # Si el usuario es administrador, usa el esquema completo para devolver todos los detalles
    if administrador:
        return AcessorioSchema().dump(accesorio, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return AcessorioMinimalSchema().dump(accesorio, many=True)


# Ruta para obtener todas las categorías
@equipo_bp.route("/categorias", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def categorias():
    # Obtiene datos adicionales del token JWT
    additional_data = get_jwt()
    # Extrae el permiso de administrador del token, asignando False si no está presente
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Categoria
    categoria = Categoria.query.all()
    # Si el usuario es administrador, usa el esquema completo para devolver todos los detalles
    if administrador:
        return CategoriaSchema().dump(categoria, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return CategoriaMinimalSchema().dump(categoria, many=True)


# Ruta para obtener todos los equipos
@equipo_bp.route("/equipos", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def equipos():
    # Obtiene datos adicionales del token JWT
    additional_data = get_jwt()
    # Extrae el permiso de administrador del token, asignando False si no está presente
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Equipo
    equipo = Equipo.query.all()
    # Si el usuario es administrador, usa el esquema completo para devolver todos los detalles
    if administrador:
        return EquipoSchema().dump(equipo, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return EquipoMinimalSchema().dump(equipo, many=True)

# Define la ruta "/caracteristica" para obtener todas las características
@equipo_bp.route("/caracteristica", methods=["GET"])
@jwt_required()  # Requiere autenticación JWT para acceder a la ruta
def caracteristicas():
    # Obtiene los datos adicionales del JWT (token de autenticación)
    additional_data = get_jwt()
    # Verifica si el usuario tiene permisos de administrador
    administrador = additional_data.get("administrador", False)  # False si no existe

    # Consulta todas las características en la base de datos
    caracteristica = Caracteristica.query.all()
    
    # Si el usuario es administrador, utiliza el esquema completo para serializar datos detallados
    if administrador:
        return CaracteristicaSchema().dump(caracteristica, many=True)
    # Si el usuario no es administrador, utiliza el esquema mínimo para serializar datos básicos
    else:
        return CaracteristicaMinimalSchema().dump(caracteristica, many=True)

# Ruta para obtener todos los proveedores
@equipo_bp.route("/proveedor", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def proveedores():
    # Obtiene datos adicionales del token JWT
    additional_data = get_jwt()
    # Extrae el permiso de administrador del token, asignando False si no está presente
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Proveedor
    proveedor = Proveedor.query.all()
    # Si el usuario es administrador, usa el esquema completo para devolver todos los detalles
    if administrador:
        return ProveedorSchema().dump(proveedor, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return ProveedorMinimalSchema().dump(proveedor, many=True)


# Ruta para obtener todos los clientes
@equipo_bp.route("/clientes", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def clientes():
    # Obtiene datos adicionales del token JWT
    additional_data = get_jwt()
    # Extrae el permiso de administrador del token, asignando False si no está presente
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Cliente
    cliente = Cliente.query.all()
    # Si el usuario es administrador, usa el esquema completo para devolver todos los detalles
    if administrador:
        return ClienteSchema().dump(cliente, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return ClienteMinimalSchema().dump(cliente, many=True)


# Ruta para obtener todos los inventarios
@equipo_bp.route("/inventarios", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def inventarios():
    # Obtiene datos adicionales del token JWT
    additional_data = get_jwt()
    # Extrae el permiso de administrador del token, asignando False si no está presente
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Inventario
    inventario = Inventario.query.all()
    # Si el usuario es administrador, usa el esquema completo para devolver todos los detalles
    if administrador:
        return InventarioSchema().dump(inventario, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return InventarioMinimalSchema().dump(inventario, many=True)

# Ruta para obtener todas las marcas
@equipo_bp.route("/marca", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def marcas():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Marca
    marcas = Marca.query.all()
    # Si el usuario es administrador, devuelve todos los detalles de cada marca
    if administrador:
        return MarcaSchema().dump(marcas, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return MarcaMinimalSchema().dump(marcas, many=True)


# Ruta para obtener todos los fabricantes
@equipo_bp.route("/fabricante", methods=["GET"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def fabricantes():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    # Consulta todos los registros de la tabla Fabricante
    fabricante = Fabricante.query.all()
    # Si el usuario es administrador, devuelve todos los detalles de cada fabricante
    if administrador:
        return FabricanteSchema().dump(fabricante, many=True)
    # Si no es administrador, usa el esquema mínimo con menos detalles
    else:
        return FabricanteMinimalSchema().dump(fabricante, many=True)


# Ruta CRUD para el modelo (GET, POST, PUT, DELETE)
@equipo_bp.route("/modelo", methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()  # Requiere autenticación mediante un token JWT
def modelos():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    # Crea un nuevo modelo en la base de datos
    if request.method == "POST":
        if administrador:  # Solo los administradores pueden crear un modelo
            data = request.get_json()  # Obtiene los datos enviados en formato JSON

            # Crea una nueva instancia del modelo usando los datos proporcionados
            nuevo_modelo = Modelo(
                nombre=data.get("nombre"),
                activo=data.get("activo", True),  # Establece activo en True por defecto
                marca_id=data.get("marca_id"),
                fabricante_id=data.get("fabricante_id"),
            )

            db.session.add(nuevo_modelo)  # Agrega el nuevo modelo a la sesión de la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos

            # Devuelve el modelo creado con un código de estado 201
            return make_response(ModeloSchema().dump(nuevo_modelo), 201)
        return jsonify({"Mensaje": "UD no está habilitado para crear un usuario."}), 403

     # PUT para actualizar un modelo existente
    # forma de modificar en thunderclient:
    # {
    # "id": 1,
    # "nombre": "Nuevo Nombre del Modelo",
    # "activo": true,
    # "marca_id": 2,
    # "fabricante_id": 3
    # }
    if request.method == "PUT":
        if administrador:  # Solo los administradores pueden actualizar un modelo
            data = request.get_json()
            modelo_id = data.get("id")  # Obtiene el ID del modelo a actualizar
            modelo = Modelo.query.get_or_404(modelo_id)  # Busca el modelo en la base de datos, devuelve 404 si no existe

            # Actualiza los campos del modelo con los datos proporcionados
            modelo.nombre = data.get("nombre", modelo.nombre)
            modelo.activo = data.get("activo", modelo.activo)
            modelo.marca_id = data.get("marca_id", modelo.marca_id)
            modelo.fabricante_id = data.get("fabricante_id", modelo.fabricante_id)

            db.session.commit()  # Guarda los cambios en la base de datos
            return make_response(ModeloSchema().dump(modelo), 200)  # Devuelve el modelo actualizado
        return jsonify({"Mensaje": "UD no está habilitado para actualizar un usuario."}), 403

    # Marca un modelo como inactivo (en lugar de eliminarlo físicamente) basado en el ID proporcionado
    # forma de "eliminar" en thunderclient:
    # http://localhost:5000/modelo?id=1
    if request.method == "DELETE":
        if administrador:  # Solo los administradores pueden marcar un modelo como inactivo
            modelo_id = request.args.get("id")  # Obtiene el ID del modelo desde los parámetros de la URL
            if not modelo_id:
                return jsonify({"Mensaje": "Falta el parámetro 'id' en la solicitud"}), 400  # Error si no se proporciona el ID

            modelo = Modelo.query.get(modelo_id)  # Busca el modelo por ID
            if not modelo:
                return jsonify({"Mensaje": "Modelo no encontrado"}), 404  # Error si el modelo no existe

            modelo.activo = False  # Cambia el estado a inactivo en lugar de eliminarlo
            db.session.commit()  # Guarda los cambios en la base de datos
            return jsonify({"Mensaje": "Modelo marcado como inactivo correctamente."}), 200
        return jsonify({"Mensaje": "UD no está habilitado para cambiar el estado de este modelo."}), 403

    # Consulta y devuelve todos los modelos si el método es GET
    modelo = Modelo.query.all()
    if administrador:
        return ModeloSchema().dump(modelo, many=True)  # Devuelve detalles completos si es administrador
    else:
        return ModeloMinimalSchema().dump(modelo, many=True)  # Devuelve detalles mínimos si no es administrador
