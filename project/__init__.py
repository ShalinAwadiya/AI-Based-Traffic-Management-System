from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import warnings
import datetime

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

app = Flask(__name__)

app.secret_key = 'sessionData'

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

app.config['TESTING'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_RECORD_QUERIES'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/pythondb'

app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db = SQLAlchemy(app)

import project.com.controller
