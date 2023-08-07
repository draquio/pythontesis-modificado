import os
from flask import Flask
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='millave',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
        DATABASE_PORT=os.environ.get('FLASK_DATABASE_PORT'),
    )

    from . import db
    db.init_app(app)
    from . import auth
    from . import rol
    from . import index
    from . import error
    from . import receta
    from . import funciones
    from . import codigoqr
    from . import almacen
    app.register_blueprint(auth.bp)
    app.register_blueprint(rol.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(error.bp)
    app.register_blueprint(receta.bp)
    app.register_blueprint(codigoqr.bp)
    app.register_blueprint(almacen.bp)
    
    return app
    

