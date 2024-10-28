from flask import Blueprint
from flask_jwt_extended import get_jwt, jwt_required

# Importa el modelo Caracteristica y los esquemas para serializar datos
from models import Caracteristica
from schemas import CaracteristicaSchema, CaracteristicaMinimalSchema

# Crea un Blueprint llamado "caracteristica", que permite definir rutas específicas para las características
caracteristica_bp = Blueprint("caracteristica", __name__)

# Define la ruta "/caracteristica" para obtener todas las características
@caracteristica_bp.route("/caracteristica", methods=["GET"])
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
