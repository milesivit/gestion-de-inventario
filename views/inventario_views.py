from flask import Blueprint

from flask_jwt_extended import get_jwt, jwt_required

from models import Inventario, Cliente, Proveedor
from schemas import (
    ProveedorMinimalSchema,
    ProveedorSchema,
    ClienteMinimalSchema,
    ClienteSchema,
    InventarioSchema,
    InventarioMinimalSchema,
)

inventario_bp = Blueprint("inventario", __name__)


# get de proveedor
@inventario_bp.route("/proveedor", methods=["GET"])
@jwt_required()
def proveedores():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    proveedor = Proveedor.query.all()
    if administrador:
        return ProveedorSchema().dump(proveedor, many=True)
    else:
        return ProveedorMinimalSchema().dump(proveedor, many=True)


# get de cliente
@inventario_bp.route("/clientes", methods=["GET"])
@jwt_required()
def clientes():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    cliente = Cliente.query.all()
    if administrador:
        return ClienteSchema().dump(cliente, many=True)
    else:
        return ClienteMinimalSchema().dump(cliente, many=True)


# get de inventario
@inventario_bp.route("/inventarios", methods=["GET"])
@jwt_required()
def inventarios():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    inventario = Inventario.query.all()
    if administrador:
        return InventarioSchema().dump(inventario, many=True)
    else:
        return InventarioMinimalSchema().dump(inventario, many=True)
