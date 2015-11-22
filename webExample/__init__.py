from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import os


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'm-Ho83cJFux7J3XOJPfoz2IP'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/catalog'

app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['UPLOADS_FOLDER'] = os.path.dirname(__file__) + '/static/images'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'

db = SQLAlchemy(app)

class Owners(db.Model):
    #__tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)


class Categories(db.Model):
    #__tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(250), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    owner = db.relationship(Owners)


class Items(db.Model):
    #__tablename__ = 'db.Model'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(250))
    picture = db.Column(db.String(250))
    insert_date = db.Column(db.DateTime, default=datetime.datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    owner = db.relationship(Owners)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(Categories)

    # def __init__(self, name, description, picture, pub_date=None):
    #     self.name = title
    #     self.description = body
    #     self.picture = picture
    #     if pub_date is None:
    #         pub_date = datetime.utcnow()
    #     self.insert_date = pub_date


import webExample.views
from webExample import auth_routes
