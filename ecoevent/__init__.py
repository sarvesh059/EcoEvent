from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import urllib.parse


params = urllib.parse.quote_plus("Driver={ODBC Driver 17 for SQL Server};Server=tcp:ecoeventserver.database.windows.net,1433;Database=records;Uid=ecoevent-admin;Pwd=project@azure1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '03156e6c886fe494fb59b013'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from ecoevent import routes
