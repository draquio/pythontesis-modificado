from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from Web.auth import  login_required, rol_no_admin
from Web.db import get_db
import qrcode
from PIL import Image
import os
bp = Blueprint('codigoqr', __name__, url_prefix='/codigoqr')


@bp.route('/')
@login_required
def index():
    rol_no_admin()
    db, c = get_db()
    c.execute(
        'select * from codigoqr'
    )
    listaqr = c.fetchall()
    return render_template('codigoqr/index.html', listaqr=listaqr, titulo="Códigos QR")


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    rol_no_admin()
    if request.method == 'POST':
        nombre_de_img = request.form['img']
        texto = request.form['texto']
        error = None
        if not titulo:
            error = "Se requiere un Nombre"
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute('insert into codigoqr (img,texto) values (%s, %s)', (nombre_de_img,texto))
            c.execute('SELECT LAST_INSERT_ID()')
            # db.commit()
            imagen = qrcode.make(img)
            estetitulo = "imagens1.png"
            ruta = os.getcwd() + "/Web/imgcodigoqr/" + estetitulo
            print(ruta)
            imagen.save(ruta)
            # print("Titulo : '{}' y descripcion '{}'".format(titulo,descripcion))
            error = 'Código QR "{0}" creado exitósamente'.format(titulo)
            flash(error, "success")
            return redirect(url_for('codigoqr.index'))
            

    return render_template('codigoqr/create.html', titulo="Crear Código QR")
