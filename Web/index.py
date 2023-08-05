from flask import Flask, render_template, Blueprint, abort, request, flash, redirect, url_for, jsonify
from Web.auth import  login_required, rol_no_admin
from Web.db import get_db
import datetime
from datetime import date
from time import strftime
import random
from Web.funciones import searchVideoQuery, youtube
from Web.almacen import listar_almacenes_ocupados_ultimos_15dias, mostrar_detalle_fecha

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/historial')
def historial():
    db, c = get_db()
    carnecomprada = []
    carneguardada = []
    # c.execute('SELECT c.id, t.nombre, c.cantidad, c.date, c.tipo, c.idcortecarne, c.idtipocarne FROM carnes c, tipocarne t where DATE_FORMAT(date,"%y-%m-%d") = CURDATE() and t.id=c.idtipocarne')
    c.execute('SELECT c.id, t.nombre, c.cantidad, c.date, c.tipo, c.idcortecarne, c.idtipocarne FROM carnes c, tipocarne t where t.id=c.idtipocarne  order by date desc limit 7')
    carnehistorial = c.fetchall()
    carnehistorial = carnehistorial[::-1]
    carnehistorial = llenar_espacio_corte_carne(carnehistorial)
    for a in carnehistorial:
        if a['tipo'] == 0:
            carnecomprada.append(a)
        else:
            carneguardada.append(a)
    titulo = "Historial del {} (Hoy)".format(datetime.date.today())
    return render_template('index/historial.html', titulo=titulo, carneguardada=carneguardada, carnecomprada=carnecomprada)

def llenar_espacio_corte_carne(arreglo):
    cortes = monstrar_cortes()
    for a in arreglo:
        if a['idcortecarne']:
            for c in cortes:
                if c['id'] == a['idcortecarne']:
                    a['idcortecarne'] = c['nombre']
        else:
            a['idcortecarne'] = ""
    return arreglo


@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # CargarCarneSobrante()
    stats()
    statslineal()
    db, c = get_db()
    # c.execute('SELECT cantidad, tipo FROM carnes where DATE_FORMAT(date, "%Y-%m-%d") = CURDATE()')
    c.execute('SELECT cantidad, tipo, date FROM prueba.carnes order by id asc limit 10')
    carneshoy = c.fetchall()
    carnecompradahoy = sumarcarne(carneshoy, 0)
    carneocupadahoy = sumarcarne(carneshoy, 1)
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        tipocarne = request.form['tipocarne']
        tipo = request.form['tipo']
        # ayer = request.form.getlist('ayer')
        c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (%s, %s, %s, %s)', (tipocarne, cantidad, datetime.datetime.now(), tipo))
        db.commit()
        alerta = '{} kilos de carne guardada exitósamente!'.format(cantidad)
        flash(alerta, "success")
        return redirect(url_for('index.home'))
    return render_template('index/home.html', titulo="Estadísticas", carnecompradahoy=carnecompradahoy, carneocupadahoy=carneocupadahoy)


@bp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    rol_no_admin()
    db, c = get_db()
    c.execute('SELECT * FROM carnes where id=%s', (id,))
    carne = c.fetchone()
    c.execute('SELECT * FROM tipocarne')
    tipo = c.fetchall()
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        tipocarne = request.form['tipocarne']
        tipo = request.form['tipo']
        c.execute('update carnes set cantidad = %s, idtipocarne = %s, tipo = %s where id = %s', (cantidad, tipocarne, tipo, id))
        db.commit()
        error = "Historial modificado."
        flash(error, "success")
        return redirect(url_for('index.historial'))
    return render_template('index/update.html', titulo="Editar", carne=carne, tipo=tipo)

@bp.route('/<id>/delete', methods=['POST'])
@login_required
def delete(id):
    rol_no_admin()
    db, c = get_db()
    c.execute('delete from almacencarnessobra where idcarne = %s', (id,))
    c.execute('delete from carnes where id = %s', (id,))
    db.commit()
    error = "Eliminado exitósamente."
    flash(error, "success")
    return redirect(url_for('index.historial'))

@bp.route('/agregar_carne', methods=['GET', 'POST'])
@login_required
def agregar_carne():
    rol_no_admin()
    cortes = monstrar_corte_activos()
    tipo = monstrar_tipocarne()
    if request.method == 'POST':
        tipodecarne = request.form['tipocarne']
        error = None
        if tipodecarne == "1":
            cantidades = request.form.getlist('corte[]')
            cortescarne = request.form.getlist('corte-carne[]')
            if not cantidades[0]:
                error = "Se requiere la cantidad"
            if not cortescarne:
                error = "Se requiere los cortes de carne"
            if error is not None:
                flash(error, "danger")
            else:
                insertar_cortes_carne(cantidades,cortescarne)
                error = "Agregado correctamente"
                flash(error, "success")
        else:
            cantidad = request.form['cantidad']
            if not cantidad:
                error = "Se requiere la cantidad"
            if error is not None:
                flash(error, "danger")
            else:
                insertar_carne(cantidad, tipodecarne)
                error="Agregado correctamente"
                flash(error, "success")
        
    return render_template('index/agregar_carne.html', titulo="Agregar Carne", cortes=cortes, tipo=tipo)

def insertar_cortes_carne(cantidades, cortescarne):
    db, c = get_db()
    for x in range(len(cantidades)):
        c.execute('insert into carnes (idtipocarne, idcortecarne, cantidad, date, tipo) values (%s, %s, %s, %s, %s)', (1, cortescarne[x], cantidades[x], datetime.datetime.now(), 0))
    db.commit()

def insertar_carne(cantidad, tipodecarne):
    db, c = get_db()
    c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (%s, %s, %s, %s)', (tipodecarne, cantidad, datetime.datetime.now(), 0))
    db.commit()


@bp.route('/guardar_carne', methods=['GET', 'POST'])
@login_required
def guardar_carne():
    rol_no_admin()
    almacenes = monstrar_almacenes()
    cortes = monstrar_corte_activos()
    tipo = monstrar_tipocarne()
    if request.method == 'POST':
        tipodecarne = request.form['tipocarne']
        error = None
        if tipodecarne == "1":
            cantidades = request.form.getlist('corte[]')
            cortescarne = request.form.getlist('corte-carne[]')
            almacenguardado = request.form.getlist('lista-almacen[]')
            if not cantidades[0]:
                error = "Se requiere la cantidad"
            if error is not None:
                flash(error, "danger")
            else:
                insertar_guardado_carne_cortes(cantidades, cortescarne, almacenguardado)
                error = "Agregado correctamente"
                flash(error, "success")
        else:
            cantidades = request.form['cantidad']
            almacenguardado = request.form['almacen']
            if not cantidades:
                error = "Se requiere la cantidad"
                flash(error, "danger")
            if error is None:
                insertar_guardado_carne(cantidades, almacenguardado, tipodecarne)
                error = "Agregado correctamente"
                flash(error, "success")
    return render_template('index/guardar_carne.html', titulo="Guardar Carne", almacenes=almacenes, cortes=cortes, tipo=tipo)
def insertar_guardado_carne_cortes(cantidades, cortescarne, almacenguardado):
    db, c = get_db()
    for x in range(len(cantidades)):
        c.execute('insert into carnes (idtipocarne, idcortecarne, cantidad, date, tipo) values (%s, %s, %s, %s, %s)', (1, cortescarne[x], cantidades[x], datetime.datetime.now(), 1))
        id = c.lastrowid
        c.execute('insert into almacencarnessobra (idalmacen, idcarne, date) values (%s, %s, %s)', (almacenguardado[x],id,datetime.datetime.now()))
    db.commit()

def insertar_guardado_carne(cantidades, almacenguardado, tipodecarne):
    db, c = get_db()
    c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (%s, %s, %s, %s)', (tipodecarne, cantidades, datetime.datetime.now(), 1))
    id = c.lastrowid
    c.execute('insert into almacencarnessobra (idalmacen, idcarne, date) values (%s, %s, %s)', (almacenguardado,id,datetime.datetime.now()))
    db.commit()


# Función para monstrar recomendados en el Home
@bp.route('/recomendacion', methods=['POST'])
def recomendacion():
    comida = ['Parrillada', 'chancho a la cruz', 'pescado a la parrilla', 'asado', 'pollo a la parrilla', "churrasco", "guarniciones para parrillada", "acompañamientos para asado"] 
    orden = random.randint(0,len(comida)-1)
    ordenvideo = random.randint(0,8)
    videos = searchVideoQuery(comida[orden],youtube,"viewCount")
    resultado = jsonify({
        "titulo"    : videos[ordenvideo]['snippet']['title'],
        "miniatura" : videos[ordenvideo]['snippet']['thumbnails']['high']['url'],
        "id"        : videos[ordenvideo]['id']['videoId'],
        })
    return resultado


# Función para mostrar estadísticos totales de cada carne
@bp.route('/stats',  methods=['POST'])
def stats():
    vaca = listarcarnesemanal(0,1)
    cerdo = listarcarnesemanal(0,2)
    pollo = listarcarnesemanal(0,3)
    resultado = jsonify({
        "cantidadvaca"    : vaca['cantidad'],
        "cantidadpollo"   : pollo['cantidad'],
        "cantidadcerdo"   : cerdo['cantidad'],
        })
    return resultado

# Función para mostrar estadísticos de Carne Comprada y Carne Ocupada
@bp.route('/statslineal',  methods=['POST'])
def statslineal():
    carnecomprada = listarcarne(0)
    carneguardada = listarcarne(1)
    carneocupada = calcular_carne_ocupada(carnecomprada,carneguardada)
    resultado = jsonify({
        "carnecomprada" : carnecomprada,
        "carneguardada" : carneguardada,
        "carneocupada" : carneocupada,
        })
    return resultado

def calcular_carne_ocupada(carne1, carne2):
    if carne1 and carne2:
        resultado = []
        for i in range(len(carne1)):
            cantidad = carne1[i]['cantidad'] - carne2[i]['cantidad']
            if cantidad >= 0:
                resultado.append({'cantidad': cantidad})
            else:
                resultado.append({'cantidad': carne1[i]['cantidad']})
    return resultado

# Función que se conecta con Jquery para mostrar la predicción de cuanto deberia comprar
@bp.route('/prediccion',  methods=['POST'])
def prediccion():
    carne = []
    db, c = get_db()
    for x in range(14):
            c.execute('SELECT sum(cantidad) as cantidad, DATE_FORMAT(date,"%y-%m-%d") as fecha FROM carnes where DATE_FORMAT(date,"%y-%m-%d") = CURDATE() - INTERVAL %s DAY and tipo=0', (x,))
            carnecomprada = c.fetchone()
            c.execute('SELECT sum(cantidad) as cantidad, DATE_FORMAT(date,"%y-%m-%d") as fecha FROM carnes where DATE_FORMAT(date,"%y-%m-%d") = CURDATE() - INTERVAL %s DAY and tipo=1', (x,))
            carneguardada = c.fetchone()
            if carnecomprada['cantidad'] is not None and carneguardada['cantidad'] is not None:
                carneconsumida = carnecomprada['cantidad'] - carneguardada['cantidad'] 
                if carneconsumida >= 0:
                    carnecomprada['cantidad'] = carneconsumida
                    carne.append(carnecomprada)
                else:
                    carne.append(carnecomprada)
            else:
                carne.append(carnecomprada)
    carne = cargarvacios(carne,0)
    resultado = jsonify({
        "carne" : carne,
        })
    return resultado

# Función para que cuando exista un vacio, esto lo cargue Carnes y Fecha
def cargarvacios(carne, contador):
    fechaahora = date.today()
    cont = contador
    for c in carne:
        if c['fecha'] == None:
            c['cantidad'] = 0
        else:
            c['cantidad'] = int(c['cantidad'])
        fecha = fechaahora - datetime.timedelta(days=cont)
        c['fecha'] = str(fecha)
        cont=cont+1
    carne = carne[::-1]
    return carne

def sumarcarne(carnes, entrada):
    total = 0
    for c in carnes:
        if c['tipo'] == entrada:
            total = total + c['cantidad']
    return total

# Listarcarnesemala se usa para listar el total de carnes en los estadísticos
def listarcarnesemanal(tipo, idtipocarne):
    db, c = get_db()
    c.execute('select sum(cantidad) as cantidad from carnes where yearweek(date) = yearweek(curdate()) and tipo=%s and idtipocarne=%s', (tipo,idtipocarne))
    carne = c.fetchone()
    
    if carne['cantidad'] is not None:
        carne['cantidad'] = int(carne['cantidad'])
    else:
        carne['cantidad'] = int(0)
    return carne

# listarcarne se usa para listar carnes en el estadistico Chart
def listarcarne(tipo):
    carne = []
    db, c = get_db()
    for x in range(7):
        c.execute('SELECT sum(cantidad) as cantidad, DATE_FORMAT(date,"%y-%m-%d") as fecha FROM carnes where DATE_FORMAT(date,"%y-%m-%d") = CURDATE() - INTERVAL %s DAY and tipo=%s', (x+1,tipo))
        carne.append(c.fetchone())
    carne = cargarvacios(carne,1)
    return carne



#Agregar campo corte de Carne en javascript
@bp.route('/agregarcampocorte',  methods=['POST'])
def agregarcampocorte():
    cortes = monstrar_corte_activos()
    return jsonify(cortes)

#Listar almacenes en el guardado de carnes
@bp.route('/listaralmacenes',  methods=['POST'])
def listaralmacenes():
    almacenes = monstrar_almacenes()
    return jsonify(almacenes)

def monstrar_almacenes():
    db, c = get_db()
    c.execute('select * from almacen')
    almacenes = c.fetchall()
    return almacenes

def monstrar_cortes():
    db, c = get_db()
    c.execute('select * from cortecarne')
    cortes = c.fetchall()
    return cortes

def monstrar_corte_id(id):
    db, c = get_db()
    c.execute('select * from cortecarne where id=%s', (id,))
    corte = c.fetchone()
    return corte

def monstrar_corte_activos():
    db, c = get_db()
    c.execute('select * from cortecarne where estado=0')
    cortes = c.fetchall()
    return cortes

def monstrar_tipocarne():
    db, c = get_db()
    c.execute('select * from tipocarne')
    carnes = c.fetchall()
    return carnes


#Funcion para predecir cortes y tipo de carne cada una
@bp.route('/predecircortesytipo',  methods=['POST'])
def predecircortesytipo():
    carnes = []
    cortes = []
    db, c = get_db()
    nombre_cortes = monstrar_cortes()
    cont=0
    # for i in range(len(nombre_cortes)):
    for i in range(3):
        for x in range(40):
            c.execute('SELECT sum(cantidad) as cantidad, DATE_FORMAT(date,"%y-%m-%d") as fecha, idcortecarne as corte, idtipocarne as tipo FROM prueba.carnes where DATE_FORMAT(date,"%y-%m-%d") = CURDATE() - INTERVAL %s DAY and tipo=0 and idtipocarne=%s', (x, i+1))
            carnecomprada = c.fetchone()
            c.execute('SELECT sum(cantidad) as cantidad, DATE_FORMAT(date,"%y-%m-%d") as fecha, idcortecarne as corte, idtipocarne as tipo FROM prueba.carnes where DATE_FORMAT(date,"%y-%m-%d") = CURDATE() - INTERVAL %s DAY and tipo=1 and idtipocarne=%s', (x, i+1))
            carneguardada = c.fetchone()
            #Si es None lo pone a 0, caso contrario lo convierte en int
            if carnecomprada['cantidad'] is not None and carneguardada['cantidad'] is not None:
                cantidadconsumo = carnecomprada['cantidad'] - carneguardada['cantidad']
                if cantidadconsumo <= 0:
                    cantidadconsumo = carnecomprada['cantidad']
                if carnecomprada['corte'] is not None and carneguardada['corte'] is not None:
                    cortes.append({"cantidad":int(cantidadconsumo), "fecha":carnecomprada['fecha'],"corte":carnecomprada['corte'], "tipo":carnecomprada['tipo']})
                else:
                    carnes.append({"cantidad":int(cantidadconsumo), "fecha":carnecomprada['fecha'], "tipo":carnecomprada['tipo']})
                cont=cont+1 
    resultado = jsonify({
        "cortes" : cortes,
        "carnes" : carnes,
        "nombre_cortes" : nombre_cortes,
        })
    return resultado


@bp.route('/cortes')
@login_required
def cortes():
    # rol_no_admin()
    cortes_carne = monstrar_cortes()
    cortes = []
    cortes_desactivados = []
    for c in cortes_carne:
        if c['estado'] == 0:
            cortes.append(c)
        else:
            cortes_desactivados.append(c)
    return render_template('index/cortes.html', titulo="Cortes de Carne", cortes=cortes, cortes_desactivados=cortes_desactivados)

@bp.route('/<int:id>/cambiar_estado', methods=['POST'])
@login_required
def cambiar_estado(id):
    rol_no_admin()
    db, c = get_db()
    seleccionado = monstrar_corte_id(id)
    if seleccionado['estado'] == 0:
        estado = 1
        mensaje = 'Corte "{}" desactivado'.format(seleccionado['nombre'])
        flash(mensaje, "danger")
    else:
        estado = 0
        mensaje = 'Corte "{}" activado'.format(seleccionado['nombre'])
        flash(mensaje, "success")
    c.execute('update cortecarne set estado = %s where id = %s', (estado,id) )
    db.commit()
    
    return redirect(url_for('index.cortes'))

@bp.route('/crear_corte', methods=['GET', 'POST'])
@login_required
def crear_corte():
    rol_no_admin()
    if request.method == 'POST':
        nombre = request.form['nombre']
        error = None
        if not nombre:
            error = "Debe agregar un nombre de corte de carne"
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute(
                'insert into cortecarne (nombre, estado) values (%s, 0)', (nombre,)
            )
            db.commit()
            error = 'Corte "{0}" creado exitósamente'.format(nombre)
            flash(error, "success")
            return redirect(url_for('index.cortes'))
    return render_template('index/crear_corte.html', titulo="Crear cortes de carne")

@bp.route('/<int:id>/update_cortes', methods=['GET', 'POST'])
@login_required
def update_cortes(id):
    rol_no_admin()
    corte = monstrar_corte_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        error = None
        if not nombre:
            error = "Debe agregar un nombre de corte de carne"
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute('update cortecarne set nombre = %s where id = %s', (nombre,id))
            db.commit()
            error = 'Corte "{}" modificado exitosamente'.format(nombre)
            flash(error, "success")
            return redirect(url_for('index.cortes'))
    return render_template('index/update_cortes.html', corte=corte, titulo="Modificar Corte")


@bp.route('/seleccionar_almacen/<int:id>', methods=['GET', 'POST'])
def seleccionar_almacen(id):
    almacenes_ocupados = listar_almacenes_ocupados_ultimos_15dias()
    almacenes = []
    almacen = []
    total = 0
    if almacenes_ocupados:
        for a in almacenes_ocupados:
            if a['id'] == id:
                tipocarne = mostrar_tipocarne_nombre(a['idtipocarne'])
                almacenes.append({
                    "nombre": a['nombre'],
                    "cantidad": int(a['cantidad']),
                    "date": a['date'],
                    "tipocarne": tipocarne,
                })
        for a in almacenes_ocupados:
            if a['id'] == id:
                total = total + int(a['cantidad'])
        if almacenes:
            almacen.append({
                        "nombre": almacenes[0]['nombre'],
                        "cantidad": total,
                        "date": almacenes[0]['date'],
                        "tipocarne": tipocarne,
                    })
            resultado = mostrar_detalle_fecha(almacen)
        else:
            almacen.append({
                        "nombre": "No registro de almacén en los últimos 7 días",
                        "tipocarne": "No registrado",
                    })
            resultado = almacen
    # resultado = mostrar_detalle_fecha(almacen)
    return jsonify(resultado)
    

def mostrar_tipocarne_nombre(idtipocarne):
    carnes = monstrar_tipocarne()
    for c in carnes:
        if c['id'] == idtipocarne:
            nombre = c['nombre']
            break
    return nombre
            