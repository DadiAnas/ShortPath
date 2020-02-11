# init.py
import mysql.connector as mysql
from flask import Flask
from flask_material import Material
import networkx as nx


# connnect to database et get a cursor
def db():
    host = "localhost"
    user = "root"
    password = ""#settings.MYSQL_DATABASE_PASSWORD
    database = 'distancevilles'

    config = {
        'user': user,
        'password': password,
        'host': host,
        'database': database,
        'raise_on_warnings': True
    }

    return  mysql.connect(**config)
db = db()
cursor = db.cursor(buffered=True)


# Flask execution function
def create_app():
    app = Flask(__name__, static_url_path='/static')
    #Material(app)

    # blueprint for main parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

