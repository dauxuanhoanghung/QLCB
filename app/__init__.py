from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

db = 'qlcb'
pwd = 'Hung28122002@'

app = Flask(__name__)
app.secret_key = 'Hung28122002!@#$%^&Phuc14042002'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/' % quote(pwd) + db + '?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['page_size'] = 8

db = SQLAlchemy(app=app)
login_mana = LoginManager(app=app)
babel = Babel(app=app)
cloudinary.config(cloud_name='dm5nn54wh', api_key='836445152769358', api_secret='dxV48f7EsDEvsA4jeIRvjDBWbqM')


@babel.localeselector
def load_locale():
    return 'vi'
