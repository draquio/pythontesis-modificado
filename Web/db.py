import mysql.connector 
 
import click 
from flask import current_app, g 
from flask.cli import with_appcontext 
from .schema import instructions 
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from datetime import timedelta, date
import random

 
def get_db():
    if 'db' not in g: 
        g.db = mysql.connector.connect( 
            host=current_app.config['DATABASE_HOST'], 
            user=current_app.config['DATABASE_USER'], 
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE'],
            port=current_app.config["DATABASE_PORT"],
        )
        g.c = g.db.cursor(dictionary=True) 
    return g.db, g.c
 
def close_db(e=None): 
    db = g.pop('db', None) 
 
    if db is not None: 
        db.close() 
 
def init_db():
    db, c = get_db()
    #Insertando BD
    for i in instructions:
        c.execute(i)
    db.commit()

   #Creado Rol, Admin y tipos de carnes
    c.execute('insert into rol (nombrerol, descripcion, privilegio) values ("Administrador", "Administrador de todo el sistemna", 1)')
    c.execute('insert into rol (nombrerol, descripcion, privilegio) values ("Asistente", "Asistente del sistema", 2)')
    
    

    
    c.execute('insert into user (username, idrol, password) values ("Admin", 1, %s)', (generate_password_hash("123"),))
    c.execute('insert into tipocarne (nombre) values ("Vaca")')
    c.execute('insert into tipocarne (nombre) values ("Cerdo")')
    c.execute('insert into tipocarne (nombre) values ("Pollo")')
    c.execute('insert into cortecarne (nombre, estado) values ("Bife de Chorizo", 0)')
    c.execute('insert into cortecarne (nombre, estado) values ("Cuadril", 0)')
    c.execute('insert into cortecarne (nombre, estado) values ("Tira de lomo", 0)')
    for x in range(40):
        fecha = datetime.datetime.now() - timedelta(days=x)
        valor = random.randint(8,12)
        valor2 = random.randint(1,5)
        # c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (1, %s,%s,0)', (valor,fecha))
        # c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (1, %s,%s,1)', (valor2,fecha))
        #agregar cortes de carne para probar
        valorcorte = random.randint(2,5)
        valorcorteguardado = random.randint(1,valorcorte)
        tipodecorte = random.randint(1,3)
        c.execute('insert into carnes (idtipocarne, idcortecarne, cantidad, date, tipo) values (1,%s,%s,%s,0)', (tipodecorte,valorcorte,fecha))
        c.execute('insert into carnes (idtipocarne, idcortecarne, cantidad, date, tipo) values (1,%s,%s,%s,1)', (tipodecorte,valorcorteguardado,fecha))
        #Pollo
        valorpollo = random.randint(2,4)
        valorpolloguardado = random.randint(1,valorpollo)
        c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (3, %s,%s,0)', (valorpollo,fecha))
        c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (3, %s,%s,1)', (valorpolloguardado,fecha))
        #Cerdo
        valorcerdo = random.randint(2,4)
        valorcerdoguardado = random.randint(1,valorcerdo)
        c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (2, %s,%s,0)', (valorcerdo,fecha))
        c.execute('insert into carnes (idtipocarne, cantidad, date, tipo) values (2, %s,%s,1)', (valorcerdo,fecha))
    db.commit()
 

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db() 
    click.echo('Base de datos inicializada')
    click.echo('Usuario: Admin')
    click.echo('Contraseña: 123')
 
def init_app(app):
    app.teardown_appcontext(close_db) 
    app.cli.add_command(init_db_command) 




# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,2,CURDATE() - INTERVAL 1 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,8,CURDATE() - INTERVAL 2 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,5,CURDATE() - INTERVAL 3 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,6,CURDATE() - INTERVAL 4 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,7,CURDATE() - INTERVAL 5 DAY,0);

# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,8,CURDATE() - INTERVAL 6 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,9,CURDATE() - INTERVAL 7 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,6,CURDATE() - INTERVAL 8 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,7,CURDATE() - INTERVAL 9 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,11,CURDATE() - INTERVAL 10 DAY,0);

# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,8,CURDATE() - INTERVAL 11 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,7,CURDATE() - INTERVAL 12 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,9,CURDATE() - INTERVAL 13 DAY,0);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,7,CURDATE() - INTERVAL 14 DAY,0);






# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,2,CURDATE() - INTERVAL 1 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,3,CURDATE() - INTERVAL 2 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,7,CURDATE() - INTERVAL 3 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,5,CURDATE() - INTERVAL 4 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,4,CURDATE() - INTERVAL 5 DAY,1);

# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,6,CURDATE() - INTERVAL 6 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,8,CURDATE() - INTERVAL 7 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,8,CURDATE() - INTERVAL 8 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,9,CURDATE() - INTERVAL 9 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,10,CURDATE() - INTERVAL 10 DAY,1);

# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,6,CURDATE() - INTERVAL 11 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,8,CURDATE() - INTERVAL 12 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,7,CURDATE() - INTERVAL 13 DAY,1);
# insert into prueba.carnes (idtipocarne, cantidad,date,tipo) values (1,8,CURDATE() - INTERVAL 14 DAY,1);