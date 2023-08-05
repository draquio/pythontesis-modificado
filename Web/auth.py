import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from Web.db import get_db
import time


bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view   

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    rol_no_admin()
    roles = get_rol()
    if request.method == 'POST':
        username = request.form['username']
        idrol = request.form['idrol']
        password = request.form['password']
        solo_texto = validar_texto(username)
        db, c = get_db()
        error = None
        c.execute(
            'select id from User where username = %s', (username,)
        )
        if solo_texto is True:
            error = "Nombre de usuario no puede llevar números"
        if not username:
            error = "Nombre de usuario es requerido"
        if not password:
            error = "Contraseña es requerida"
        elif c.fetchone() is not None:
            error = "Usuario {} se encuentra registrado.".format(username)
        if error is None:
            c.execute(
                'insert into User (username, idrol, password) values (%s, %s, %s)',
                (username, idrol, generate_password_hash(password))
            )
            db.commit()
            error = 'Usuario "{0}" creado'.format(username)
            flash(error, "success")
            return redirect(url_for('auth.users'))
            #return redirect(url_for('auth.register'))

        flash(error, "danger")
    return render_template('auth/register.html', titulo="Registro de Usuarios", roles=roles)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None:
        return redirect(url_for('index.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from User where username = %s', (username,)
        )
        user = c.fetchone()
        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index.home'))

        flash(error, "danger")
        

    return render_template('auth/login.html', titulo="Login")

#Funcion para mostrar Roles en el registro
def get_rol():
    db, c = get_db()
    c.execute(
        'select * from rol'
    )
    rol = c.fetchall()
    if rol is None:
        abort(404, "No existen roles")
    return rol

#Funcion para obtener user para editar
def get_user(id):
    db, c = get_db()
    c.execute(
        'select * from user where id = %s', (id,)
    )
    user = c.fetchone()
    if user is None:
        abort(404, "No existen usuarios")
    return user


def rol_no_admin():
    user_id = session.get('user_id')
    db, c = get_db()
    c.execute(
        'SELECT r.privilegio FROM prueba.user u, prueba.rol r where u.id=%s and u.idrol=r.id', (user_id,)
    )
    rol = c.fetchall()
    for r in rol:
        if r['privilegio'] != 1:
            abort(404, "No puedes acceder, no eres Administrador")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute('SELECT *, r.privilegio FROM user u, rol r where u.id=%s and u.idrol=r.id', (user_id,))
        g.user = c.fetchone()




        

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.index'))

@bp.route('/users')
@login_required
def users():
    rol_no_admin()
    db, c = get_db()
    c.execute(
        'select u.username as username, u.id as id, r.nombrerol as rol, r.privilegio as privilegio from User u, rol r where r.id=u.idrol order by privilegio'
    )
    usuarios = c.fetchall()
    return render_template('auth/users.html', usuarios=usuarios, titulo="Usuarios")


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    rol_no_admin()
    roles = get_rol()
    user = get_user(id)
    titulo = 'Editando usuario "{}"'.format(user['username'])
    if request.method == 'POST':
        username = request.form['username']
        idrol = request.form['idrol']
        error = None
        if not username:
            error = "Usuario es requerido."
        if error is not None:
            flash(error, "danger")
        else:
            db, c = get_db()
            c.execute(
                'update user set username = %s, idrol = %s where id = %s', (username, idrol, id)
            )
            db.commit()
            error = "Usuario modificado."
            flash(error, "success")
            return redirect(url_for('auth.users'))
    return render_template('auth/update.html', user=user, roles=roles, titulo=titulo)


@bp.route('/<int:id>/update/password', methods=['GET', 'POST'])
@login_required
def updatepassword(id):
    rol_no_admin()
    user = get_user(id)
    titulo = 'Editando contraseña de "{}"'.format(user['username'])
    if request.method == 'POST':
        password = request.form['password']
        nuevopassword = request.form['nuevopassword']
        repetirpassword = request.form['repetirpassword']
        print(nuevopassword + " " + repetirpassword)
        error = None
        if not check_password_hash(user['password'], password):
            error = "Su contraseña está mal escrita"
        elif nuevopassword != repetirpassword:
            error = "Debe repetir la nueva contraseña"
        if error is None:
            db, c = get_db()
            print("entra hasta antes de guardar")
            c.execute(
                'update user set password = %s where id = %s', (generate_password_hash(nuevopassword), id)
            )
            db.commit()
            error = 'Contraseña modificada del usuario "{}"'.format(user['username'])
            flash(error, "success")
            return redirect(url_for('auth.users'))
        else:
            flash(error, "danger")
    return render_template('auth/updatepassword.html',user=user, titulo=titulo)


@bp.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    db, c = get_db()
    c.execute(
        'select u.username as username, u.id as id, r.nombrerol as rol from User u, rol r where r.id=u.idrol and u.id = %s', (user_id,)
    )
    user = c.fetchone()
    titulo = 'Bienvenido a tu perfil "{}"'.format(user['username']) 
    return render_template('auth/profile.html', user=user, titulo=titulo)

# Validar solo texto
def validar_texto(texto):
    valor = False
    for t in texto:
        if t.isdigit():
            valor = True
            break
    return valor

# Borrar Users
@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    rol_no_admin()
    db, c = get_db()
    if id != 1:
        c.execute('select username from User where id = %s', (id,))
        usuario = c.fetchone()
        c.execute('delete from user where id = %s', (id,))
        error = 'Usuario "{}" eliminado.'.format(usuario['username'])
        flash(error, "success")
    else:
        error = "Usuario Administrador no se puede eliminar."
        flash(error, "danger")
    db.commit()
    
    return redirect(url_for('auth.users'))