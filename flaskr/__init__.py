from flask import Flask
from flask_mysqldb import MySQL

## __name__ is the name of the module. When running directly from python, it will be '__main__'
app = Flask(__name__)

## configuration of database

app.config["MYSQL_USER"] = ''
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = ''
app.config["MYSQL_HOST"] = ''

db = MySQL(app)

from flaskr import routes
