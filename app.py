from flask import Flask, render_template,redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/phone.db' #puerto de la db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#esto sirve para flaskWTF
app.config['SECRET_KEY'] = 'milena'

db= SQLAlchemy(app)
migrate= Migrate(app, db) 

from models import Marca, Proveedor, Modelo, Fabricante, Categoria, Caracteristica, Accesorio, Equipo, Inventario, Cliente
from forms import MarcaForm, ProveedorForm, EmptyForm, FabricanteForm, ModeloForm, CategoriaForm, CaracteristicaForm, AccesorioForm, EquipoForm
#-----------------------------------------------------------------------------------------------------------------
@app.route("/") #página principal
def index():
    return render_template ('index.html')
#-----------------------------------------------------------------------------------------------------------------
@app.route("/marcas")
def marcas():
    marcas = Marca.query.filter_by(activo=True).all()  # Filtra solo las marcas activas
    return render_template('marcas.html', marcas=marcas)

@app.route('/agregar-marcas', methods=['GET', 'POST'])
def agregar_marcas():
    form = MarcaForm()
    if form.validate_on_submit(): #validate_on_submit es un método de Flask-WTF que valida el formulario y asegura que fue enviado mediante un POST request
        if Marca.query.filter_by(nombre=form.nombre.data).first(): #consulta la base de datos para verificar si ya existe una marca con el mismo nombre 
            form.nombre.errors.append('Esta marca ya existe.') #si existe tira error
        else:
            nueva_marca = Marca(nombre=form.nombre.data) #si no existe se guarda en la base de datos la nueva marca
            db.session.add(nueva_marca) #añade la nueva marca
            db.session.commit() #confirma la transacción en la base de datos. 
            return redirect(url_for('marcas')) #cuando vos modificas la variable y pones guardar te lleva a la pagina marcas
            
            
    return render_template('agregar_marcas.html', form=form) #form es un objeto de formulario que contiene datos y validaciones para el formulario.

@app.route('/eliminar-marcas', methods=['GET', 'POST'])
def eliminar_marcas():
    form = MarcaForm()  # Asegúrate de que MarcaForm esté definido y utilizado
    if request.method == 'POST':
        marca_id = request.form.get('marca_id')
        marca = Marca.query.get(marca_id)
        if marca:
            marca.activo = False  # Oculta la marca en lugar de eliminarla
            db.session.commit()
            return redirect(url_for('eliminar_marcas'))
        else:
            form.errors['marca_id'] = ['Marca no encontrada.']
    marcas = Marca.query.filter_by(activo=True).all()  # Filtra solo las marcas activas
    return render_template('eliminar_marcas.html', marcas=marcas, form=form)

@app.route('/modificar-marcas/<int:id>', methods=['GET', 'POST'])
def modificar_marcas(id):
    marca = Marca.query.get_or_404(id)
    form = MarcaForm(obj=marca)
    if form.validate_on_submit():
        if Marca.query.filter_by(nombre=form.nombre.data).first() and marca.nombre != form.nombre.data:
            form.nombre.errors.append('Esta marca ya existe.')
        else:
            marca.nombre = form.nombre.data
            db.session.commit()
            return redirect(url_for('marcas'))
    form.submit.label.text = 'Guardar Cambios'
    return render_template('modificar_marcas.html', form=form, marca=marca)

#-----------------------------------------------------------------------------------------------------------------
@app.route("/proveedores")
def proveedores():
    proveedores = Proveedor.query.all()  # Devuelve una lista de todas las instancias del modelo Proveedor que existen en la base de datos
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/agregar-proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit(): # validate_on_submit es un método de Flask-WTF que valida el formulario y asegura que fue enviado mediante un POST request
        if Proveedor.query.filter_by(nombre=form.nombre.data).first(): # consulta la base de datos para verificar si ya existe un proveedor con el mismo nombre
            form.nombre.errors.append('Este proveedor ya existe.') # si existe tira error
        else:
            nuevo_proveedor = Proveedor(
                nombre=form.nombre.data,
                telefono=form.telefono.data,
                direccion=form.direccion.data,
                correo_electronico=form.correo_electronico.data
            ) # si no existe se guarda en la base de datos el nuevo proveedor
            db.session.add(nuevo_proveedor) # añade el nuevo proveedor
            db.session.commit() # confirma la transacción en la base de datos
            return redirect(url_for('proveedores')) # cuando vos modificas la variable y pones guardar te lleva a la pagina proveedores
    return render_template('agregar_proveedor.html', form=form)

@app.route('/eliminar-proveedor', methods=['GET', 'POST'])
def eliminar_proveedor():
    form = ProveedorForm()
    if request.method == 'POST':
        proveedor_id = request.form.get('proveedor_id')
        proveedor = Proveedor.query.get(proveedor_id)
        if proveedor:
            proveedor.activo = False  # Oculta el proveedor en lugar de eliminarlo
            db.session.commit()
            return redirect(url_for('eliminar_proveedor'))
        else:
            form.errors['proveedor_id'] = ['Proveedor no encontrado.']
    
    # Cambia la consulta para obtener proveedores inactivos
    proveedores = Proveedor.query.filter_by(activo=True).all()
    return render_template('eliminar_proveedor.html', proveedores=proveedores, form=form)


@app.route('/modificar-proveedor/<int:id>', methods=['GET', 'POST'])
def modificar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)
    
    if form.validate_on_submit():
        proveedor.nombre = form.nombre.data
        proveedor.telefono = form.telefono.data
        proveedor.direccion = form.direccion.data
        proveedor.correo_electronico = form.correo_electronico.data
        db.session.commit()
        return redirect(url_for('proveedores'))
    
    form.submit.label.text = 'Guardar cambios'
    return render_template('modificar_proveedor.html', form=form, proveedor=proveedor)
#-----------------------------------------------------------------------------------------------------------------
@app.route("/modelos")
def modelos():
    modelos = Modelo.query.filter_by(activo=True).all()  # Filtra solo los modelos activos
    return render_template('modelos.html', modelos=modelos)

@app.route('/eliminar-modelo', methods=['GET', 'POST'])
def eliminar_modelo():
    form = ModeloForm()
    if request.method == 'POST':
        modelo_id = request.form.get('modelo_id')
        modelo = Modelo.query.get(modelo_id)
        if modelo:
            modelo.activo = False  # Oculta el modelo en lugar de eliminarlo
            db.session.commit()
            return redirect(url_for('eliminar_modelo'))
        else:
            form.errors['modelo_id'] = ['Modelo no encontrado.']
    modelos = Modelo.query.filter_by(activo=True).all()  # Filtra solo los modelos activos
    return render_template('eliminar_modelo.html', modelos=modelos, form=form)

@app.route('/modificar-modelo/<int:id>', methods=['GET', 'POST'])
def modificar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    form = ModeloForm(obj=modelo)
    
    # Cargar los fabricantes en el campo select
    form.fabricante_id.choices = [(fabricante.id, fabricante.nombre) for fabricante in Fabricante.query.filter_by(activo=True).all()]
    form.marca_id.choices = [(m.id, m.nombre) for m in Marca.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        modelo.nombre = form.nombre.data
        modelo.fabricante_id = form.fabricante_id.data
        modelo.marca_id = form.marca_id.data
        db.session.commit()
        return redirect(url_for('modelos'))

    return render_template('modificar_modelo.html', form=form, modelo=modelo)  # Pasar el objeto modelo al template




@app.route('/agregar-modelo', methods=['GET', 'POST'])
def agregar_modelo():
    form = ModeloForm()
    
    # cargar los fabricantes en el campo select asi puedo elegirlos y no escribirlos porque ya estan cargados en la base de datos desde fabricantes
    form.fabricante_id.choices = [(fabricante.id, fabricante.nombre) for fabricante in Fabricante.query.all()]
    form.marca_id.choices = [(m.id, m.nombre) for m in Marca.query.filter_by(activo=True).all()]
    if form.validate_on_submit():
        nuevo_modelo = Modelo(
            nombre=form.nombre.data,
            fabricante_id=form.fabricante_id.data,
            marca_id=form.marca_id.data

        )
        db.session.add(nuevo_modelo)
        db.session.commit()
        return redirect(url_for('modelos'))

    return render_template('agregar_modelo.html', form=form)

 #-----------------------------------------------------------------------------------------------------------------
@app.route('/fabricantes')
def fabricantes():
    fabricantes = Fabricante.query.filter_by(activo=True).all()
    return render_template('fabricantes.html', fabricantes=fabricantes)


@app.route('/agregar-fabricante', methods=['GET', 'POST'])
def agregar_fabricante():
    form = FabricanteForm()
    if form.validate_on_submit():
        if Fabricante.query.filter_by(nombre=form.nombre.data).first():
            form.nombre.errors.append('Este fabricante ya existe.')
        else:
            nuevo_fabricante = Fabricante(
                nombre=form.nombre.data,
                pais_origen=form.pais_origen.data
            )
            db.session.add(nuevo_fabricante)
            db.session.commit()
            return redirect(url_for('fabricantes'))
    return render_template('agregar_fabricante.html', form=form)

@app.route('/modificar-fabricante/<int:id>', methods=['GET', 'POST'])
def modificar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    form = FabricanteForm(obj=fabricante)
    if form.validate_on_submit():
        if Fabricante.query.filter_by(nombre=form.nombre.data).first() and fabricante.nombre != form.nombre.data:
            form.nombre.errors.append('Esta marca ya existe.')
        else:
            fabricante.nombre = form.nombre.data
            fabricante.pais_origen = form.pais_origen.data
            db.session.commit()
            return redirect(url_for('fabricantes'))
    form.submit.label.text = 'Guardar Cambios'
    return render_template('modificar_fabricante.html', form=form, fabricante=fabricante)

@app.route('/eliminar-fabricante', methods=['GET', 'POST'])
def eliminar_fabricante():
    form = EmptyForm()  # Usa un formulario vacío si no necesitas validaciones adicionales
    if form.validate_on_submit():
        fabricante_id = request.form.get('fabricante_id')
        fabricante = Fabricante.query.get(fabricante_id)
        if fabricante:
            fabricante.activo = False  # Oculta el fabricante en lugar de eliminarlo
            db.session.commit()
            return redirect(url_for('eliminar_fabricante'))
        else:
            form.errors['fabricante_id'] = ['Fabricante no encontrado.']
    
    # Filtra solo los fabricantes activos
    fabricantes = Fabricante.query.filter_by(activo=True).all()
    return render_template('eliminar_fabricante.html', fabricantes=fabricantes, form=form)

#-----------------------------------------------------------------------------------------------------------------
@app.route('/restaurar', methods=['GET', 'POST'])
def restaurar():
    form = EmptyForm()  # Usa un formulario vacío si no es necesario realizar una entrada adicional

    if request.method == 'POST':
        # Restaurar marcas
        marca_id = request.form.get('marca_id')
        if marca_id:
            marca = Marca.query.get(marca_id)
            if marca:
                marca.activo = True
                db.session.commit()
        
        # Restaurar categorías
        categoria_id = request.form.get('categoria_id')
        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            if categoria:
                categoria.activo = True
                db.session.commit()
        
        # Restaurar modelos
        modelo_id = request.form.get('modelo_id')
        if modelo_id:
            modelo = Modelo.query.get(modelo_id)
            if modelo:
                modelo.activo = True
                db.session.commit()
        
        # Restaurar proveedores
        proveedor_id = request.form.get('proveedor_id')
        if proveedor_id:
            proveedor = Proveedor.query.get(proveedor_id)
            if proveedor:
                proveedor.activo = True
                db.session.commit()
        
        # Restaurar accesorios
        accesorio_id = request.form.get('accesorio_id')
        if accesorio_id:
            accesorio = Accesorio.query.get(accesorio_id)
            if accesorio:
                accesorio.activo = True
                db.session.commit()
        
        # Restaurar fabricantes
        fabricante_id = request.form.get('fabricante_id')
        if fabricante_id:
            fabricante = Fabricante.query.get(fabricante_id)
            if fabricante:
                fabricante.activo = True
                db.session.commit()
        
        # Restaurar características
        caracteristica_id = request.form.get('caracteristica_id')
        if caracteristica_id:
            caracteristica = Caracteristica.query.get(caracteristica_id)
            if caracteristica:
                caracteristica.activo = True
                db.session.commit()
        
        # Restaurar equipos
        equipo_id = request.form.get('equipo_id')
        if equipo_id:
            equipo = Equipo.query.get(equipo_id)
            if equipo:
                equipo.activo = True
                db.session.commit()

        return redirect(url_for('restaurar'))

    # Recuperar todos los elementos inactivos
    marcas_inactivas = Marca.query.filter_by(activo=False).all()
    accesorios_inactivos = Accesorio.query.filter_by(activo=False).all()
    categorias_inactivas = Categoria.query.filter_by(activo=False).all()
    proveedores_inactivos = Proveedor.query.filter_by(activo=False).all()
    modelos_inactivos = Modelo.query.filter_by(activo=False).all()
    fabricantes_inactivos = Fabricante.query.filter_by(activo=False).all()
    caracteristicas_inactivas = Caracteristica.query.filter_by(activo=False).all()
    equipos_inactivos = Equipo.query.filter_by(activo=False).all()  # Recupera los equipos inactivos

    return render_template('restaurar.html', marcas=marcas_inactivas, modelos=modelos_inactivos, fabricantes=fabricantes_inactivos, categorias=categorias_inactivas, proveedores=proveedores_inactivos, caracteristicas=caracteristicas_inactivas, accesorios=accesorios_inactivos, equipos=equipos_inactivos, form=form)


#-----------------------------------------------------------------------------------------------------------------

@app.route('/categoria')
def categoria():
    categoria = Categoria.query.filter_by(activo=True).all()
    return render_template('categoria.html', categorias=categoria)

@app.route('/agregar-categoria', methods=['GET', 'POST'])
def agregar_categoria():
    form = CategoriaForm()
    if form.validate_on_submit():
        if Categoria.query.filter_by(nombre=form.nombre.data).first():
            form.nombre.errors.append('Esta categoria ya existe.')
        else:
            nueva_categoria = Categoria(
                nombre=form.nombre.data,
            )
            db.session.add(nueva_categoria)
            db.session.commit()
            return redirect(url_for('categoria'))
    return render_template('agregar_categoria.html', form=form)

@app.route('/modificar-categoria/<int:id>', methods=['GET', 'POST'])
def modificar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm(obj=categoria)
    if form.validate_on_submit():
        if Categoria.query.filter_by(nombre=form.nombre.data).first() and categoria.nombre != form.nombre.data:
            form.nombre.errors.append('Esta categoría ya existe.')
        else:
            categoria.nombre = form.nombre.data
            db.session.commit()
            return redirect(url_for('categoria'))
    form.submit.label.text = 'Guardar Cambios'
    return render_template('modificar_categoria.html', form=form, categoria=categoria)


@app.route('/eliminar-categoria', methods=['GET', 'POST'])
def eliminar_categoria():
    form = CategoriaForm()  # Asegúrate de que CategoriaForm esté definido y utilizado
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        categoria = Categoria.query.get(categoria_id)  # Usa Categoria en lugar de Marca
        if categoria:
            categoria.activo = False  # Oculta la categoría en lugar de eliminarla
            db.session.commit()
            return redirect(url_for('eliminar_categoria'))
        else:
            form.errors['categoria_id'] = ['Categoría no encontrada.']
    
    categorias = Categoria.query.filter_by(activo=True).all()  # Filtra solo las categorías activas
    return render_template('eliminar_categoria.html', categorias=categorias, form=form)

#-----------------------------------------------------------------------------------------------------------------

@app.route('/caracteristicas')
def caracteristicas():
    caracteristicas = Caracteristica.query.filter_by(activo=True).all()
    return render_template('caracteristicas.html', caracteristicas=caracteristicas)

@app.route('/agregar_caracteristicas', methods=['GET', 'POST'])
def agregar_caracteristicas():
    form = CaracteristicaForm()
    form.modelo_id.choices = [(modelo.id, modelo.nombre) for modelo in Modelo.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        nueva_caracteristica = Caracteristica(
            modelo_id=form.modelo_id.data,
            peso=form.peso.data,
            resolucion_pantalla=form.resolucion_pantalla.data,
            capacidad_bateria=form.capacidad_bateria.data,
            sistema_operativo=form.sistema_operativo.data,
            precio_lista=form.precio_lista.data,
            camara=form.camara.data,
            descripcion=form.descripcion.data,
            lanzamiento=form.lanzamiento.data,
            activo=True
        )
        db.session.add(nueva_caracteristica)
        db.session.commit()
        return redirect(url_for('caracteristicas'))

    return render_template('agregar_caracteristicas.html', form=form)

@app.route('/modificar-caracteristicas/<int:id>', methods=['GET', 'POST'])
def modificar_caracteristicas(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    form = CaracteristicaForm(obj=caracteristica)

    # Asegúrate de que form.modelo_id.choices está configurado correctamente
    form.modelo_id.choices = [(modelo.id, modelo.nombre) for modelo in Modelo.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        caracteristica.modelo_id = form.modelo_id.data
        caracteristica.peso = form.peso.data
        caracteristica.resolucion_pantalla = form.resolucion_pantalla.data
        caracteristica.capacidad_bateria = form.capacidad_bateria.data
        caracteristica.sistema_operativo = form.sistema_operativo.data
        caracteristica.precio_lista = form.precio_lista.data
        caracteristica.camara = form.camara.data
        caracteristica.descripcion = form.descripcion.data
        caracteristica.lanzamiento = form.lanzamiento.data
        db.session.commit()
        return redirect(url_for('caracteristicas'))

    return render_template('modificar_caracteristicas.html', form=form, caracteristica=caracteristica)

@app.route('/eliminar-caracteristicas', methods=['GET', 'POST'])
def eliminar_caracteristicas():
    form = EmptyForm()  # Usa un formulario vacío para manejar la eliminación
    if request.method == 'POST':
        caracteristica_id = request.form.get('caracteristica_id')
        caracteristica = Caracteristica.query.get(caracteristica_id)  
        if caracteristica:
            caracteristica.activo = False  # Oculta la característica en lugar de eliminarla
            db.session.commit()
            return redirect(url_for('eliminar_caracteristicas'))
        else:
            form.errors['caracteristica_id'] = ['Característica no encontrada.']
    
    caracteristicas = Caracteristica.query.filter_by(activo=True).all()  # Filtra solo las características activas
    return render_template('eliminar_caracteristicas.html', caracteristicas=caracteristicas, form=form)

#-----------------------------------------------------------------------------------------------------------------
@app.route('/accesorios')
def accesorios():
    accesorios = Accesorio.query.filter_by(activo=True).all()
    return render_template('accesorios.html', accesorios=accesorios)

@app.route('/agregar-accesorio', methods=['GET', 'POST'])
def agregar_accesorio():
    form = AccesorioForm()
    # cargar las opciones del campo modelo_id
    form.modelo_id.choices = [(modelo.id, modelo.nombre) for modelo in Modelo.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        if Accesorio.query.filter_by(modelo_id=form.modelo_id.data).first():
            form.modelo_id.errors.append('Este accesorio ya existe para el modelo seleccionado.')
        else:
            nuevo_accesorio = Accesorio(
                modelo_id=form.modelo_id.data,
                cargador=form.cargador.data,
                auriculares=form.auriculares.data,
                chip=form.chip.data,
                funda=form.funda.data,
                activo=True 
            )
            db.session.add(nuevo_accesorio)
            db.session.commit()
            return redirect(url_for('accesorios'))
    return render_template('agregar_accesorio.html', form=form)

@app.route('/modificar-accesorio/<int:id>', methods=['GET', 'POST'])
def modificar_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    form = AccesorioForm(obj=accesorio)
    # Cargar las opciones del campo modelo_id
    form.modelo_id.choices = [(modelo.id, modelo.nombre) for modelo in Modelo.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        if Accesorio.query.filter_by(modelo_id=form.modelo_id.data).first() and accesorio.modelo_id != form.modelo_id.data:
            form.modelo_id.errors.append('Este accesorio ya existe para el modelo seleccionado.')
        else:
            accesorio.modelo_id = form.modelo_id.data
            accesorio.cargador = form.cargador.data
            accesorio.auriculares = form.auriculares.data
            accesorio.chip = form.chip.data
            accesorio.funda = form.funda.data
            db.session.commit()
            return redirect(url_for('accesorios'))
    form.submit.label.text = 'Guardar Cambios'
    return render_template('modificar_accesorio.html', form=form, accesorio=accesorio)

@app.route('/eliminar-accesorios', methods=['GET', 'POST'])
def eliminar_accesorios():
    form = EmptyForm()  # Usa un formulario vacío para manejar la eliminación
    if request.method == 'POST':
        accesorio_id = request.form.get('accesorio_id')
        accesorio = Accesorio.query.get(accesorio_id)
        if accesorio:
            accesorio.activo = False  # Oculta el accesorio en lugar de eliminarlo
            db.session.commit()
            return redirect(url_for('eliminar_accesorios'))
        else:
            form.errors['accesorio_id'] = ['Accesorio no encontrado.']
    
    accesorios = Accesorio.query.filter_by(activo=True).all()  # Filtra solo los accesorios activos
    return render_template('eliminar_accesorios.html', accesorios=accesorios, form=form)

#-----------------------------------------------------------------------------------------------------------------
@app.route('/equipo')
def equipos():
    equipos = Equipo.query.filter_by(activo=True).all()
    return render_template('equipo.html', equipos=equipos)

@app.route('/agregar-equipos', methods=['GET', 'POST'])
def agregar_equipos():
    form = EquipoForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.filter_by(activo=True).all()]
    form.marca_id.choices = [(m.id, m.nombre) for m in Marca.query.filter_by(activo=True).all()]
    form.modelo_id.choices = [(m.id, m.nombre) for m in Modelo.query.filter_by(activo=True).all()]
    form.caracteristica_id.choices = [(c.id, f'{c.precio_lista} - {c.capacidad_bateria}') for c in Caracteristica.query.filter_by(activo=True).all()]
    form.accesorio_id.choices = [(a.id, f'Cargador: {"Sí" if a.cargador else "No"}, Auriculares: {"Sí" if a.auriculares else "No"}') for a in Accesorio.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        if Equipo.query.filter_by(modelo_id=form.modelo_id.data).first():
            form.modelo_id.errors.append('Este equipo ya existe para el modelo seleccionado.')
        else:
            nuevo_equipo = Equipo(
                categoria_id=form.categoria_id.data,
                marca_id=form.marca_id.data,
                modelo_id=form.modelo_id.data,
                caracteristica_id=form.caracteristica_id.data,
                accesorio_id=form.accesorio_id.data,
            )
            db.session.add(nuevo_equipo)
            db.session.commit()
            return redirect(url_for('equipos'))
    return render_template('agregar_equipos.html', form=form)

@app.route('/modificar-equipos/<int:id>', methods=['GET', 'POST'])
def modificar_equipos(id):
    equipo = Equipo.query.get_or_404(id)
    form = EquipoForm(obj=equipo)

    # Cargar las opciones del formulario
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.filter_by(activo=True).all()]
    form.marca_id.choices = [(m.id, m.nombre) for m in Marca.query.filter_by(activo=True).all()]
    form.modelo_id.choices = [(m.id, m.nombre) for m in Modelo.query.filter_by(activo=True).all()]
    form.caracteristica_id.choices = [(c.id, f'{c.precio_lista} - {c.capacidad_bateria}') for c in Caracteristica.query.filter_by(activo=True).all()]
    form.accesorio_id.choices = [(a.id, f'Cargador: {"Sí" if a.cargador else "No"}, Auriculares: {"Sí" if a.auriculares else "No"}') for a in Accesorio.query.filter_by(activo=True).all()]

    if form.validate_on_submit():
        if Equipo.query.filter_by(modelo_id=form.modelo_id.data).first() and equipo.modelo_id != form.modelo_id.data:
            form.modelo_id.errors.append('Este equipo ya existe para el modelo seleccionado.')
        else:
            equipo.categoria_id = form.categoria_id.data
            equipo.marca_id = form.marca_id.data
            equipo.modelo_id = form.modelo_id.data
            equipo.caracteristica_id = form.caracteristica_id.data
            equipo.accesorio_id = form.accesorio_id.data
            db.session.commit()
            return redirect(url_for('equipos'))

    form.submit.label.text = 'Guardar Cambios'
    return render_template('modificar_equipos.html', form=form, equipo=equipo)

@app.route('/eliminar-equipos', methods=['GET', 'POST'])
def eliminar_equipos():
    form = EmptyForm()  # Usa un formulario vacío para manejar la eliminación
    if request.method == 'POST':
        equipo_id = request.form.get('equipo_id')
        equipo = Equipo.query.get(equipo_id)
        if equipo:
            equipo.activo = False  # Oculta el equipo en lugar de eliminarlo
            db.session.commit()
            return redirect(url_for('eliminar_equipos'))
        else:
            form.errors['equipo_id'] = ['Equipo no encontrado.']
    
    equipos = Equipo.query.filter_by(activo=True).all()  # Filtra solo los equipos activos
    return render_template('eliminar_equipos.html', equipos=equipos, form=form)

#-----------------------------------------------------------------------------------------------------------------
@app.route('/inventario')
def inventario():
    inventarios = Inventario.query.all()
    return render_template('inventario.html', inventarios=inventarios)

@app.route('/agregar-inventario', methods=['GET', 'POST'])
def agregar_inventario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        proveedor_id = request.form.get('proveedor_id')
        cantidad = request.form.get('cantidad')
        fecha = request.form.get('fecha')

        # sin validaciones
        nuevo_inventario = Inventario(
            nombre=nombre,
            proveedor_id=proveedor_id,
            cantidad=cantidad,
            fecha=fecha,
        )
        db.session.add(nuevo_inventario)
        db.session.commit()
        return redirect(url_for('inventario'))

    # cargar los modelos y proveedores para el formulario
    modelos = Modelo.query.all()
    proveedores = Proveedor.query.all()
    return render_template('agregar_inventario.html', modelos=modelos, proveedores=proveedores)

@app.route('/modificar-inventario/<int:id>', methods=['GET', 'POST'])
def modificar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nuevo_proveedor_id = request.form.get('proveedor_id')
        nueva_cantidad = request.form.get('cantidad')
        nueva_fecha = request.form.get('fecha')

        # actualizar los datos del inventario
        inventario.nombre = nuevo_nombre
        inventario.proveedor_id = nuevo_proveedor_id
        inventario.cantidad = nueva_cantidad
        inventario.fecha = nueva_fecha
        
        db.session.commit()
        return redirect(url_for('inventario'))

    # Cargar proveedores para el formulario
    proveedores = Proveedor.query.filter_by(activo=True).all()
    return render_template('modificar_inventario.html', inventario=inventario, proveedores=proveedores)

@app.route('/eliminar-inventario', methods=['GET', 'POST'])
def eliminar_inventario():
    if request.method == 'POST':
        inventario_id = request.form.get('inventario_id')
        inventario = Inventario.query.get(inventario_id)
        if inventario:
            db.session.delete(inventario)  # Elimina el inventario de la base de datos
            db.session.commit()
            return redirect(url_for('eliminar_inventario'))
    
    inventarios = Inventario.query.all()  # Muestra todos los inventarios, sin filtrar por activo
    return render_template('eliminar_inventario.html', inventarios=inventarios)

#-----------------------------------------------------------------------------------------------------------------
@app.route('/cliente')
def cliente():
    clientes = Cliente.query.all()  
    return render_template('cliente.html', clientes=clientes)

@app.route('/agregar-cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        dni = request.form.get('dni')
        inventario_id = request.form.get('inventario_id')
        fecha = request.form.get('fecha')

        # Obtener el inventario seleccionado
        inventario = Inventario.query.get(inventario_id)
        if inventario and inventario.cantidad > 0:
            # Reducir la cantidad del inventario
            inventario.cantidad -= 1

            # Crear el nuevo cliente
            nuevo_cliente = Cliente(
                nombre=nombre,
                dni=dni,
                inventario_id=inventario_id,
                fecha=fecha,
            )
            db.session.add(nuevo_cliente)
            db.session.commit()
            return redirect(url_for('cliente'))
        else:
            flash('El producto seleccionado no está disponible en inventario.')

    # Cargar inventarios para el formulario
    inventarios = Inventario.query.all()
    return render_template('agregar_cliente.html', inventarios=inventarios)

@app.route('/modificar-cliente/<int:id>', methods=['GET', 'POST'])
def modificar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nuevo_dni = request.form.get('dni')
        nuevo_inventario_id = request.form.get('inventario_id')
        nueva_fecha = request.form.get('fecha')

        # Actualizar los datos del cliente
        cliente.nombre = nuevo_nombre
        cliente.dni = nuevo_dni
        cliente.inventario_id = nuevo_inventario_id
        cliente.fecha = nueva_fecha

        db.session.commit()
        return redirect(url_for('cliente'))

    # Cargar los inventarios para el formulario
    inventarios = Inventario.query.all()
    return render_template('modificar_cliente.html', cliente=cliente, inventarios=inventarios)

@app.route('/eliminar-cliente', methods=['GET', 'POST'])
def eliminar_cliente():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        cliente = Cliente.query.get(cliente_id)
        if cliente:
            db.session.delete(cliente)  # Elimina el cliente de la base de datos
            db.session.commit()
            return redirect(url_for('cliente'))
    
    clientes = Cliente.query.all()  # Muestra todos los clientes
    return render_template('eliminar_cliente.html', clientes=clientes)