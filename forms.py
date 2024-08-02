from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Email# bibliotecas externas a Flask-WTF, pero se usa junto con Flask-WTF

class MarcaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Agregar Marca')

class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Agregar Marca')

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=50)])
    direccion = StringField('Dirección', validators=[Length(max=50)])
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Agregar Proveedor')

class EmptyForm(FlaskForm):
    submit = SubmitField('Eliminar')

class FabricanteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    pais_origen = StringField('País de Origen', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class ModeloForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    fabricante_id = SelectField('Fabricante', coerce=int, validators=[DataRequired()])
    marca_id = SelectField('Marca', coerce=int, validators=[DataRequired()])  # Añadido aquí
    submit = SubmitField('Guardar')

class CaracteristicaForm(FlaskForm):
    modelo_id = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    peso = FloatField('Peso', validators=[DataRequired()])
    resolucion_pantalla = StringField('Resolución de Pantalla', validators=[Length(max=50)])
    capacidad_bateria = IntegerField('Capacidad de Batería')
    sistema_operativo = StringField('Sistema Operativo', validators=[Length(max=50)])
    precio_lista = FloatField('Precio de Lista')
    camara = StringField('Cámara', validators=[Length(max=200)])
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(max=200)])
    lanzamiento = DateField('Fecha de Lanzamiento', format='%Y-%m-%d')
    submit = SubmitField('Guardar')

class AccesorioForm(FlaskForm):
    modelo_id = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    cargador = BooleanField('Cargador')
    auriculares = BooleanField('Auriculares')
    chip = BooleanField('Chip')
    funda = BooleanField('Funda')
    submit = SubmitField('Guardar')

class AccesorioForm(FlaskForm):
    modelo_id = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    cargador = BooleanField('Cargador')
    auriculares = BooleanField('Auriculares')
    chip = BooleanField('Chip')
    funda = BooleanField('Funda')
    submit = SubmitField('Guardar')

class EquipoForm(FlaskForm):
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    marca_id = SelectField('Marca', coerce=int, validators=[DataRequired()])
    modelo_id = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    caracteristica_id = SelectField('Precio dólar - Batería en horas', coerce=int, validators=[DataRequired()])
    accesorio_id = SelectField('Cargador - Auriculares', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')