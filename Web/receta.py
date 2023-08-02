from flask import (
    Blueprint, flash, g, render_template, request, url_for, redirect
)
from Web.auth import  login_required, rol_no_admin
from Web.db import get_db
from Web.funciones import searchVideoQuery, mostrar_video
import datetime
from apiclient.discovery import build
youtube = build('youtube', 'v3', developerKey="AIzaSyDadJbuTMoB_wExqYvFtQppynh6sgMM3GI")


bp = Blueprint('receta', __name__, url_prefix='/receta')
@bp.route('/')
@login_required
def index():
  return render_template('recetas/index.html', titulo="Recetas")

@bp.route('/recetas')
@login_required
def guardadas():
  db, c = get_db()
  c.execute('select * from receta where %s=iduser', (g.user['id'],))
  recetas = c.fetchall()
  recetas = recetas[::-1]
  return render_template('recetas/recetas.html', titulo="Recetas Guardadas", recetas=recetas)

@bp.route('/buscar', methods=['POST'])
@login_required
def buscar():
  if request.method == 'POST':
    tag = request.form['receta']
    relevancia = request.form['relevancia']
    videos = searchVideoQuery(tag,youtube,relevancia)
    return render_template('recetas/index.html', titulo="Recetas", videos=videos)

@bp.route('/ver_video/<id>', methods=['GET', 'POST'])
@login_required
def ver_video(id):
  db, c = get_db()
  c.execute('select * from receta where %s=id_v and %s=iduser', (id,g.user['id'],))
  receta = c.fetchone()
  validacion = 0
  if receta is None:
    validacion = 1
  video = mostrar_video(youtube, id)
  if request.method == 'POST':
    db, c = get_db()
    fecha = datetime.datetime.now()
    c.execute('insert into Receta (id_v,title,thumbnail,date,iduser) values (%s, %s, %s, %s,%s)', (id,video['title'],video['thumbnails']['standard']['url'],fecha,g.user['id']))
    db.commit()
    alerta = 'Receta: "{0}" guardada exitósamente!'.format(video['title'])
    flash(alerta, "success")
    return redirect(url_for('receta.guardadas'))
  else:
    fecha = video['publishedAt']
    partes = fecha.split("T")[0].split("-")
    video['publishedAt'] = "/".join(reversed(partes))
    return render_template('recetas/video.html', titulo=video['title'], video=video, id=id, validacion=validacion)

@bp.route('/<idv>/delete', methods=['POST'])
@login_required
def delete(idv):
    db, c = get_db()
    c.execute(
        'delete from receta where id_v = %s and iduser=%s', (idv,g.user['id']) 
    )
    db.commit()
    error = "Receta eliminada."
    flash(error, "warning")
    return redirect(url_for('receta.guardadas'))

