from flask import Blueprint

from flask_jwt_extended import get_jwt, jwt_required

# Importa los modelos y esquemas necesarios
from models import Inventario, Cliente, Proveedor
from schemas import (
    ProveedorMinimalSchema,
    ProveedorSchema,
    ClienteMinimalSchema,
    ClienteSchema,
    InventarioSchema,
    InventarioMinimalSchema,
)

# Crea un Blueprint llamado "inventario" para organizar rutas relacionadas con inventarios, proveedores y clientes
inventario_bp = Blueprint("inventario", __name__)


# Ruta para obtener todos los proveedores
@inventario_bp.route("/proveedor", methods=["GET"])
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
@inventario_bp.route("/clientes", methods=["GET"])
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
@inventario_bp.route("/inventarios", methods=["GET"])
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
