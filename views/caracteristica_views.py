from flask import Blueprint

from flask_jwt_extended import get_jwt, jwt_required


from models import Caracteristica
from schemas import CaracteristicaSchema, CaracteristicaMinimalSchema

caracteristica_bp = Blueprint("caracteristica", __name__)


# get de categoria
@caracteristica_bp.route("/caracteristica", methods=["GET"])
@jwt_required()
def caracteristicas():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador", False)

    caracteristica = Caracteristica.query.all()
    if administrador:
        return CaracteristicaSchema().dump(caracteristica, many=True)
    else:
        return CaracteristicaMinimalSchema().dump(caracteristica, many=True)
