from flask import Flask, render_template, Blueprint, abort, request, flash, redirect, url_for, jsonify
from Web.auth import  login_required, rol_no_admin
from Web.db import get_db
import datetime
from datetime import date
import qrcode
from PIL import Image
import os
# from Web.index import monstrar_almacenes

bp = Blueprint('almacen', __name__, url_prefix='/almacen')
@bp.route('/')
def index():
    db, c = get_db()
    # c.execute('select * from carnessobra where estado=0 and DATE_FORMAT(date,"%y-%m-%d") <= CURDATE() - INTERVAL 1 DAY and DATE_FORMAT(date,"%y-%m-%d") >= CURDATE() - INTERVAL 7 DAY')
    # CarneSinRepositorio = c.fetchall()
    # CarneSinRepositorio = mostrar_detalle_fecha(CarneSinRepositorio)
    almacenes_ocupados = listar_almacenes_ocupados_ultimos_15dias()
    almacenes_ocupados = mostrar_detalle_fecha(almacenes_ocupados)
    almacenes = get_almacen_QR()
    # AgregarDiadelaSemana(CarneSinRepositorio)
    # return render_template('almacen/index.html', titulo="Almacen", CarneSinRepositorio=CarneSinRepositorio, almacenes=almacenes, almacenes_ocupados=almacenes_ocupados)
    return render_template('almacen/index.html', titulo="Almacen", almacenes=almacenes, almacenes_ocupados=almacenes_ocupados)

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    rol_no_admin()
    db, c = get_db()
    c.execute('SELECT * FROM almacen where id=%s', (id,))
    almacen = c.fetchone()
    print(almacen)
    if request.method == 'POST':
        nombre = request.form['nombre']
        error = None
        if not nombre:
            error = "Debe agregar un nombre"
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute('update almacen set nombre = %s where id = %s', (nombre,id,))
            db.commit()
            error = '"{}" Modificado exitosamente.'.format(nombre)
            flash(error, "success")
            return redirect(url_for('almacen.index'))
    return render_template('almacen/update.html', almacen=almacen, titulo="Editar Almacen")
    

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    rol_no_admin()
    if request.method == 'POST':
        nombre = request.form['nombre']
        error = None
        if not nombre:
            error = "Se requiere un Nombre"
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute('insert into almacen (nombre, date, estado) values (%s, %s, %s)', (nombre, datetime.datetime.now(), 0))
            id = c.lastrowid
            imagen = qrcode.make(id)
            nombre_imagen = nombre + ".png"
            ruta = os.getcwd() + "/Web/static/imgqr/" + nombre_imagen
            imagen.save(ruta)
            c.execute('insert into codigoqr (img, texto, idalmacen) values (%s, %s, %s)', (nombre_imagen, nombre, id))
            db.commit()
            
            error = '"{0}" creado exitósamente'.format(nombre)
            flash(error, "success")
            return redirect(url_for('almacen.index'))
            

    return render_template('almacen/create.html', titulo="Crear Almacén")


@bp.route('/imprimir/<int:id>', methods=['GET', 'POST'])
@login_required
def imprimir(id):
    db, c = get_db()
    c.execute('SELECT qr.img as img, a.id as idalmacen, a.nombre FROM codigoqr qr, almacen a where a.id=qr.idalmacen and a.id=%s;', (id,) )
    almacen = c.fetchone()
    print(almacen)
    titulo = ("Imprimir {} ".format(almacen['nombre']))
    return render_template('almacen/imprimir.html', almacen=almacen, titulo=titulo)


@bp.route('/<id>/deleteAlmacenGuardado', methods=['POST'])
@login_required
def deleteAlmacenGuardado(id):
    db, c = get_db()
    c.execute('select idcarne from almacencarnessobra where id = %s', (id,) )
    id_carne = c.fetchone()
    print("Id de carne: ", id_carne)
    c.execute('delete from almacencarnessobra where id = %s', (id,) )
    c.execute('delete from carnes where id = %s', (id_carne['idcarne'],) )
    db.commit()
    error = "Eliminado exitósamente."
    flash(error, "success")
    return redirect(url_for('almacen.index'))

def get_almacen():
    db, c = get_db()
    c.execute('SELECT * FROM almacen')
    almacen = c.fetchall()
    return almacen

def mostrar_almacen_id(id):
    db, c = get_db()
    c.execute('SELECT * FROM almacen where id=%s', (id,))
    almacen = c.fetchone()
    return almacen


def get_almacen_QR():
    db, c = get_db()
    c.execute('SELECT a.id, a.nombre, qr.img, a.date FROM almacen a, codigoqr qr where qr.id=a.id')
    almacen = c.fetchall()
    return almacen

def AgregarDiadelaSemana(carnes):
    nombre_dia=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado','Domingo']
    for c in carnes:
        # print(c['fecha'])
        fecha = datetime(c['fecha'])
        # print(calendar.weekday(c['fecha']))

def get_carnesobra(id):
    db, c = get_db()
    c.execute('select * from carnessobra where id=%s', (id,))
    carne = c.fetchall()
    return carne

def mostrar_detalle_fecha(carnes):
    hoy = date.today().strftime('%Y-%m-%d')
    ayer = str(date.today() - datetime.timedelta(days=1))
    Antesdeayer = str(date.today() - datetime.timedelta(days=2))
    for c in carnes:
        fecha = c['date'].strftime('%Y-%m-%d')
        minutos = c['date'].strftime('%M')  
        #Consultamos si la fecha tiene minutos
        if minutos != "00":
            if fecha == hoy:
                c['date'] = "Hoy ({})".format(c['date'].strftime('%H:%M %p'))
            elif fecha == ayer:
                c['date'] = "Ayer ({})".format(c['date'].strftime('%H:%M %p'))
            elif fecha == Antesdeayer:
                c['date'] = "Antes de ayer ({})".format(c['date'].strftime('%H:%M %p'))
            else:
                c['date'] = c['date'].strftime('%d-%m-%Y')
        else:
            if fecha == hoy:
                c['date'] = "Hoy"
            elif fecha == ayer:
                c['date'] = "Ayer"
            elif fecha == Antesdeayer:
                c['date'] = "Antes de ayer"
            else:
                c['date'] = c['date'].strftime('%d-%m-%Y')
    return carnes
       
def listar_almacenes_ocupados_ultimos_15dias():
    db, c = get_db()
    lista = []
    c.execute('select count(id) as total from almacen')
    longitud = c.fetchone()
    #Tomamos la longitud
    for i in range(longitud['total']):
        idalmacen = i+1
        c.execute('SELECT acs.id as idgeneral, al.nombre, c.idtipocarne, c.cantidad, acs.date, al.id, qr.img FROM almacencarnessobra acs, carnes c, almacen al, codigoqr qr where acs.idalmacen=al.id and acs.idcarne=c.id and qr.idalmacen=al.id and al.id=%s and (acs.date >= DATE_SUB(CURDATE(), INTERVAL 15 DAY)) order by acs.date desc', (idalmacen,))
        almacenes_ocupados = c.fetchall()
        cont = 0
        #Si hay datos entramos
        if almacenes_ocupados:
            for a in almacenes_ocupados:  
                fechamasactual = almacenes_ocupados[0]['date'].strftime('%d-%m-%Y')
                fecha = almacenes_ocupados[cont]['date'].strftime('%d-%m-%Y')
                cont+=1
                #Comparamos la fecha mas actual [0] con las siguientes fechas sin hora.
                if fechamasactual == fecha:
                    lista.append(a)
    return lista
