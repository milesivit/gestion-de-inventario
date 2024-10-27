from flask import Blueprint, request, jsonify, make_response

from datetime import timedelta

from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required,
    create_access_token
)

from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)

from app import db
from models import User
from schemas import UserSchema, UserMinimalSchema


auth_bp= Blueprint('auth', __name__)


@auth_bp.route("/login", methods=['POST'])
def login():
    
    data = request.authorization
    username = data.username
    password = data.password

    usuario= User.query.filter_by(username=username).first()

    if usuario and check_password_hash(pwhash=usuario.password_hash, password=password):
        acces_token= create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=20),
            additional_claims=dict(
                administrador= usuario.is_admin
            )
        )
        return jsonify({"Token": f"{acces_token}"})
    return jsonify({"Mensaje" : "El usuario y la contraseña no coinciden."})

@auth_bp.route("/users", methods=['GET', 'POST'])
@jwt_required()
def user():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador', False)  # Asignar False por defecto si no está presente

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            username = data.get('nombre_usuario')
            password = data.get('password')

            # verifica si el usuario ya existe
            si_existe_usuario = User.query.filter_by(username=username).first()
            if si_existe_usuario:
                return jsonify({"Error": "El nombre de usuario ya existe."}), 400

            password_hasheada = generate_password_hash(
                password=password,
                method='pbkdf2',
                salt_length=8,
            )
            print(password_hasheada)
            try:
                nuevo_usuario = User(username=username, password_hash=password_hasheada)
                db.session.add(nuevo_usuario)
                db.session.commit()

                return jsonify({"Usuario Creado": username}), 201  # Retorno correcto
            except:
                return jsonify({"Error": "Ocurrió un error al crear usuario."})  # Devuelve el error

        return jsonify({"Mensaje": "UD no está habilitado para crear un usuario."}), 403  # Código de estado adecuado

    # Para GET
    usuarios = User.query.all()
    if administrador:
        return jsonify(UserSchema().dump(obj=usuarios, many=True))
    else:
        return jsonify(UserMinimalSchema().dump(obj=usuarios, many=True))

