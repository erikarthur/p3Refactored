from flask import Flask, render_template, json, request, redirect
from flask import jsonify, url_for, flash, make_response
from flask import session as login_session
import requests
import os
from flask import Response
import psycopg2
import random
import string
import contextlib
import json
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from wtforms import Form, TextField, validators

from form_classes import Category, Catalog_Item

from catalog import app
from database_functions import connect, get_cursor

cs_file_path = os.path.join(os.path.dirname(__file__), 'settings.json')

with open(cs_file_path) as data_file:
    data = json.load(data_file)
    server_str = 'http://%s:%d' % (data['servers']['server'],
                                   data['servers']['serverPort'])
    web_str = 'http://%s:%d' % (data['servers']['web'],
                                   data['servers']['webPort'])

cs_file_path = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
CLIENT_ID = json.loads(
    open(cs_file_path, 'r').read())['web']['client_id']


def get_categories():
    """Returns the catagores in the catalog"""
    with get_cursor() as cursor:
        cursor.execute("select *"
                       "from categories order by category asc;")

        categories = cursor.fetchall()

    return categories


def get_latest_items():
    """Returns the most recent 10 items in the catalog.  """
    with get_cursor() as cursor:
        cursor.execute("SELECT item_name, item_description, item_picture FROM "
                       "items order by item_insert_date desc limit 10;")

        latest_items = cursor.fetchall()

    return latest_items


def get_category(name):
    with get_cursor() as cursor:
        cursor.execute('select item_name, item_description, '
                       'item_picture, owner_email, owner_name  '
                       'from category_view where category = %s;',
                       (name, ))
        category_items = cursor.fetchall()

        return category_items


@app.route('/')
def hello_world():

    categories = get_categories()
    latest_items = get_latest_items()

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template(
        "pages/latest-items.html", categories=categories,
        latest_items=latest_items, server='http://192.168.0.119:8000/category/',
        home='http:/192.168.0.119:8000', STATE=state)


@app.route('/category/<name>')
def get_category_items(name):

    categories = get_categories()
    category = get_category(name)

    return render_template(
        "pages/item-page.html", categories=categories, category=category,
        name=name, server='/category/',
        home='/')


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():

    if login_session['email']:
        form = Category(request.form)

        if request.method == 'POST' and form.validate():
            # add data
            with get_cursor() as cursor:
                cursor.execute(
                    'select owner_id from owners where owner_email = %s;',
                    (login_session['email'],))
                print login_session['email']
                output = cursor.fetchall()
                user_id = output[0][0]

                cate = form.data['category_name']
                cursor.execute(
                    'INSERT INTO categories VALUES (default, %s, %s, now());',
                    (cate,user_id,))
            return redirect( url_for('hello_world') )
        return render_template('pages/add-category.html', form=form)



