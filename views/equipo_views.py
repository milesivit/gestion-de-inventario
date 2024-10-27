from flask import Blueprint

from flask_jwt_extended import (
    get_jwt,
    jwt_required
)

from models import Accesorio, Categoria, Equipo
from schemas import AcessorioSchema, AcessorioMinimalSchema, CategoriaMinimalSchema, CategoriaSchema, EquipoMinimalSchema, EquipoSchema

equipo_bp= Blueprint('equipo', __name__)

#get de accesorio
@equipo_bp.route('/accesorio', methods=['GET'])
@jwt_required()
def accesorios():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)

    accesorio = Accesorio.query.all()
    if administrador:
        return AcessorioSchema().dump(accesorio, many=True)
    else:
        return AcessorioMinimalSchema().dump(accesorio, many=True)

#get de categorias
@equipo_bp.route('/categorias', methods=['GET'])
@jwt_required()
def categorias():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)

    categoria = Categoria.query.all()
    if administrador:
        return CategoriaSchema().dump(categoria, many=True)
    else:
        return CategoriaMinimalSchema().dump(categoria, many=True)
    
#get de equipos
@equipo_bp.route('/equipos', methods=['GET'])
@jwt_required()
def equipos():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)

    equipo = Equipo.query.all()
    if administrador:
        return EquipoSchema().dump(equipo, many=True)
    else:
        return EquipoMinimalSchema().dump(equipo, many=True)