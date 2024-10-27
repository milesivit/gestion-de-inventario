from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt,
    jwt_required
)

from app import db
from models import Modelo, Marca, Fabricante
from schemas import ModeloSchema, MarcaSchema, FabricanteSchema, ModeloMinimalSchema, FabricanteMinimalSchema, MarcaMinimalSchema

modelo_bp= Blueprint('modelo', __name__)

#creacion de endpoints donde modelo tiene marca y fabricante anidado.
#CRUD DE MODELO

#get de marca
@modelo_bp.route('/marca', methods=['GET'])
@jwt_required()
def marcas():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)

    marcas = Marca.query.all()
    if administrador:
        return MarcaSchema().dump(marcas, many=True)
    else:
        return MarcaMinimalSchema().dump(marcas, many=True)


#get de fabricante
@modelo_bp.route('/fabricante', methods=['GET'])
@jwt_required()
def fabricantes():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)

    fabricante = Fabricante.query.all()
    if administrador:
        return FabricanteSchema().dump(fabricante, many=True)
    else:
        return FabricanteMinimalSchema().dump(fabricante, many=True)

# CRUD de modelo (GET, POST, PUT, DELETE)
@modelo_bp.route('/modelo', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def modelos():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)

    if request.method == 'POST':
        if administrador:
            data = request.get_json()

            nuevo_modelo = Modelo(
                nombre=data.get('nombre'),
                activo=data.get('activo', True),  # default activo a True
                marca_id=data.get('marca_id'),
                fabricante_id=data.get('fabricante_id')
            )

            db.session.add(nuevo_modelo)
            db.session.commit()
            
            return make_response(ModeloSchema().dump(nuevo_modelo), 201)
        return jsonify({"Mensaje": "UD no está habilitado para crear un usuario."}), 403
    
    # PUT para actualizar un modelo existente
    #forma de modificar en thunderclient:
   # {
    #"id": 1,
    #"nombre": "Nuevo Nombre del Modelo",
    #"activo": true,
    #"marca_id": 2,
    #"fabricante_id": 3
    #}
    if request.method == 'PUT':
        if administrador:
            data = request.get_json()
            modelo_id = data.get('id')
            modelo = Modelo.query.get_or_404(modelo_id)

            modelo.nombre = data.get('nombre', modelo.nombre)
            modelo.activo = data.get('activo', modelo.activo)
            modelo.marca_id = data.get('marca_id', modelo.marca_id)
            modelo.fabricante_id = data.get('fabricante_id', modelo.fabricante_id)

            db.session.commit()
            return make_response(ModeloSchema().dump(modelo), 200)
        return jsonify({"Mensaje": "UD no está habilitado para actualizar un usuario."}), 403
    
    # DELETE para eliminar un modelo existente por ID
    # forma de "eliminar" en thunderclient: 
    # http://localhost:5000/modelo?id=1
    if request.method == 'DELETE':
        if administrador:
            modelo_id = request.args.get('id')
            if not modelo_id:
                return jsonify({"Mensaje": "Falta el parámetro 'id' en la solicitud"}), 400  # error si falta el ID

            modelo = Modelo.query.get(modelo_id)
            if not modelo:
                return jsonify({"Mensaje": "Modelo no encontrado"}), 404  # si el modelo no existe

            # cambia el estado a inactivo en vez de eliminarlo
            modelo.activo = False
            db.session.commit()
            return jsonify({"Mensaje": "Modelo marcado como inactivo correctamente."}), 200
        return jsonify({"Mensaje": "UD no está habilitado para cambiar el estado de este modelo."}), 403
    
    modelo = Modelo.query.all()
    if administrador:
        return ModeloSchema().dump(modelo, many=True)
    else:
        return ModeloMinimalSchema().dump(modelo, many=True)

