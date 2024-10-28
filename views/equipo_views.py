from flask import Blueprint

from flask_jwt_extended import get_jwt, jwt_required

# Importa los modelos y esquemas necesarios
from models import Accesorio, Categoria, Equipo
from schemas import (
    AcessorioSchema,
    AcessorioMinimalSchema,
    CategoriaMinimalSchema,
    CategoriaSchema,
    EquipoMinimalSchema,
    EquipoSchema,
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
