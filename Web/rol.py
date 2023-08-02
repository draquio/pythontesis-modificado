from flask import (
    Blueprint, flash, g, render_template, request, url_for, redirect
)
from werkzeug.exceptions import abort
from Web.auth import  login_required, rol_no_admin
from Web.db import get_db

bp = Blueprint('rol', __name__, url_prefix='/rol')

@bp.route('/')
@login_required
def index():
    rol_no_admin()
    db, c = get_db()
    c.execute(
        'select * from rol'
    )
    listarol = c.fetchall()
    return render_template('rol/index.html', listarol=listarol, titulo="Rol")

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    rol_no_admin()
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        nombrerol = request.form['nombrerol']
        privilegio = request.form['privilegio']
        error = None
        solo_texto = validar_texto(nombrerol)
        if solo_texto is True:
            error = "El nombre de rol no puede llevar números"
        if not descripcion:
            error = "Se requiere descripción de Rol"
        if not nombrerol:
            error = "Se requiere un Nombre de Rol"
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute(
                'insert into rol (nombrerol, descripcion, privilegio) values (%s, %s, %s)', (nombrerol, descripcion, privilegio)
            )
            db.commit()
            error = 'Rol "{0}" creado exitósamente'.format(nombrerol)
            flash(error, "success")
            return redirect(url_for('rol.index'))
            

    return render_template('rol/create.html', titulo="Crear Rol")

def get_rol(id):
    db, c = get_db()
    c.execute(
        'select * from rol r where %s=r.id', (id,)
    )
    
    rol = c.fetchone()
    if rol is None:
        abort(404, "El rol de id {0} no existe".format(id))
    return rol

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    rol_no_admin()
    if id == 1:
        flash("No puedes modificar el rol de Administrador", "warning")
        return redirect(url_for('rol.index')) 
    rol = get_rol(id)
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        nombrerol = request.form['nombrerol']
        privilegio = request.form['privilegio']
        error = None
        solo_texto = validar_texto(nombrerol)
        if solo_texto is True:
            error = "El nombre de rol no puede llevar números"
        if not descripcion:
            error = "La descripción es requerida."
        if not nombrerol:
            error = "El Nombre de Rol es requerido"
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute(
                'update rol set nombrerol = %s, descripcion = %s, privilegio = %s where id = %s', (nombrerol, descripcion, privilegio, id)
            )
            db.commit()
            error = "Rol modificado."
            flash(error, "success")
            return redirect(url_for('rol.index'))
    return render_template('rol/update.html', rol=rol, titulo="Modificar Rol")


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    rol_no_admin()
    db, c = get_db()
    c.execute('select count(*) as total FROM user where idrol=%s', (id,))
    # c.execute('SELECT * FROM carnes where id=%s', (id,))
    rolocupado = c.fetchone()
    c.execute('select nombrerol from rol where id = %s', (id,))
    rol = c.fetchone()
    if rolocupado['total'] == 0:
        c.execute('delete from rol where id = %s', (id,))
        error = 'Rol "{}" eliminado.'.format(rol["nombrerol"])
        flash(error, "success")
    else:
        if rolocupado['total'] >= 2:
            error = 'No es posible eliminar el Rol "{}" debido a que lo están ocupando {} usuarios'.format(rol["nombrerol"], rolocupado['total'])
        else:
            error = 'No es posible eliminar el Rol "{}" debido a que lo está ocupando {} usuario'.format(rol["nombrerol"], rolocupado['total'])
        flash(error, "danger")
    db.commit()
    
    return redirect(url_for('rol.index'))
    #return render_template('rol/index.html', alerta="alert-success")


# Validar solo texto
def validar_texto(texto):
    valor = False
    for t in texto:
        if t.isdigit():
            valor = True
            break
    return valor