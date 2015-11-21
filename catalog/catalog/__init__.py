__author__ = 'erik'

from flask import Flask
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'm-Ho83cJFux7J3XOJPfoz2IP'

from catalog import views
from catalog import auth_routes
