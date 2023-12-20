from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

PLUGIN_LIBRARY = "lib/build/libmyplugins.so"
engine_file_path = "lib/build/yolov5s.engine"

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
db = SQLAlchemy(app)

categories = ['no-helmet', 'no-mask', 'fire']
