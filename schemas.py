from db import ma
from marshmallow import validates, ValidationError, fields

from models import User, Marca, Fabricante, Modelo, Caracteristica, Categoria, Accesorio, Equipo
    
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model= User
    
    id = ma.auto_field()
    username = ma.auto_field()
    password_hash = ma.auto_field()
    is_admin = ma.auto_field()
    
    @validates('username')
    def validate_username(self, value):
        user = User.query.filter_by(username=value).first()
        if user:
            raise ValidationError('Ya existe un usuario con ese username.')
        return value


class UserMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model= User
    
    username = ma.auto_field()

class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    activo = ma.auto_field()


class MarcaMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    nombre = ma.auto_field()


class FabricanteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabricante
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    pais_origen = ma.auto_field()
    activo = ma.auto_field()

class FabricanteMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabricante

    nombre = ma.auto_field()

class ModeloSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    activo = ma.auto_field()
    
    fabricante = fields.Nested(FabricanteSchema)  # fabricante anidado
    marca = fields.Nested(MarcaSchema)  # marca anidada

class ModeloMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo
    
    nombre = ma.auto_field()

class CaracteristicaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caracteristica
        
    id = ma.auto_field()
    modelo_id = ma.auto_field()
    peso = ma.auto_field()
    resolucion_pantalla = ma.auto_field()
    capacidad_bateria = ma.auto_field()
    sistema_operativo = ma.auto_field()
    precio_lista = ma.auto_field()
    camara = ma.auto_field()
    descripcion = ma.auto_field()
    lanzamiento = ma.auto_field()
    activo = ma.auto_field()

    modelo = fields.Nested(ModeloSchema)

class CaracteristicaMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caracteristica
        
    
    peso = ma.auto_field()
    resolucion_pantalla = ma.auto_field()
    capacidad_bateria = ma.auto_field()
    sistema_operativo = ma.auto_field()
    camara = ma.auto_field()
    descripcion = ma.auto_field()
    lanzamiento = ma.auto_field()

class CategoriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    activo = ma.auto_field()
    
class CategoriaMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria
    
    nombre = ma.auto_field()

class AcessorioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorio
    
    id = ma.auto_field()
    modelo_id = ma.auto_field()
    cargador = ma.auto_field()
    auriculares = ma.auto_field()
    chip = ma.auto_field()
    funda = ma.auto_field()
    activo = ma.auto_field()
    
    modelo = fields.Nested(ModeloSchema)

class AcessorioMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorio
    
    cargador = ma.auto_field()
    auriculares = ma.auto_field()
    chip = ma.auto_field()
    funda = ma.auto_field()

class EquipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo
    
    categoria_id = ma.auto_field()
    marca_id = ma.auto_field()
    modelo_id = ma.auto_field()
    caracteristica_id = ma.auto_field()
    accesorio_id = ma.auto_field()

    categoria = fields.Nested(CategoriaSchema)
    marca = fields.Nested(MarcaSchema)
    modelo = fields.Nested(ModeloSchema)
    caracteristica = fields.Nested(CaracteristicaSchema)
    accesorio = fields.Nested(AcessorioSchema)
 
class EquipoMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo

    categoria_id = ma.auto_field()
    marca_id = ma.auto_field()
    modelo_id = ma.auto_field()
    caracteristica_id = ma.auto_field()
    accesorio_id = ma.auto_field()

    