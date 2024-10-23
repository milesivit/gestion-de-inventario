from flask import Blueprint, request, jsonify

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


from models import User


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
        return jsonify({"Mensaje": f"{acces_token}"})
    return jsonify({"Mensaje" : "El usuario y la contraseña no coinciden."})

@auth_bp.route("/users", methods=['GET', 'POST'])
@jwt_required()
def user():
    if request.method == 'POST':
        additional_data = get_jwt()
        administrador = additional_data.get('administrador')

        if administrador is True:
            data = request.get_json()
            username = data.get('nombre_usuario')
            password = data.get('password')

            password_hasheada = generate_password_hash(
                password=password,
                method='pbkdf2',
                salt_length=8,
            )
            print(password_hasheada)
            try:
                nuevo_usuario = User(username=username, password_hash=password_hasheada)
                from app import db
                db.session.add(nuevo_usuario)
                db.session.commit()

                return jsonify({"Usuario Creado": username}), 201  # Retorno correcto
            except:
                return jsonify({"Error": "Sos burro"})  # Devuelve el error

        return jsonify({"Mensaje": "UD no está habilitado para crear un usuario."}), 403  # Código de estado adecuado

    usuarios = User.query.all()
    usuario_list = []
    for usuario in usuarios:
        usuario_list.append(
            dict(
                username=usuario.username,
                is_admin=usuario.is_admin,
                id=usuario.id,
            )
        )
    return jsonify(usuario_list), 200  # Retorno correcto para la lista de usuarios
