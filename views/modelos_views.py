from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Modelo, Marca, Fabricante
from schemas import (
    ModeloSchema,
    MarcaSchema,
    FabricanteSchema,
    ModeloMinimalSchema,
    FabricanteMinimalSchema,
    MarcaMinimalSchema,
)

# Define un Blueprint llamado "modelo" para organizar rutas relacionadas con modelos, marcas y fabricantes
modelo_bp = Blueprint("modelo", __name__)

# Ruta para obtener todas las marcas
@modelo_bp.route("/marca", methods=["GET"])
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
@modelo_bp.route("/fabricante", methods=["GET"])
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
@modelo_bp.route("/modelo", methods=["GET", "POST", "PUT", "DELETE"])
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
