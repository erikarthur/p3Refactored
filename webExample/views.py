from flask import render_template, request, redirect, url_for
from flask import session as login_session
from webExample import app
from webExample import db
from webExample import Owners, Categories, Items
import random
import string
from flask.ext.uploads import delete, init, save, Upload
import uuid

from form_classes import Catalog_Item, Category
from wtforms import Field
import os
from werkzeug import secure_filename
import datetime


@app.route('/')
def index():
    """
    Returns list of up to 10 items that have been added most recently
    :return:
    """
    categories = db.session.query(Categories).order_by(Categories.category_name).all()
    latest_items = db.session.query(Items).order_by(Items.insert_date.desc()).limit(10)
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    # login_session['state'] = state

    if login_session.get('email') is not None:
        email = login_session['email']
    else:
        email = False

    return render_template(
        "pages/latest-items.html", categories=categories,
        latest_items=latest_items,
        home='/', STATE=state, email=email)


@app.route('/category/<name>')
def get_category_items(name):
    """
    Returns a list of items in a catgory
    :param name: this is the name of the category to quest
    """
    categories = db.session.query(Categories).order_by(Categories.category_name).all()
    categoryFilter = db.session.query(Categories).filter_by(category_name=name).first()
    category = db.session.query(Items).filter_by(category=categoryFilter).all()

    if login_session.get('email') is not None:
        email = login_session['email']
    else:
        email = False

    return render_template(
        "pages/item-page.html", categories=categories, category=category,
        name=name, server='/category/',
        home='/', email=email, category_number=categoryFilter.id)


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    """
    Adds a new category to catalog
    :return:
    """
    if login_session.get('email') is not None:
        form = Category(request.form)

        if request.method == 'POST' and form.validate():
            # add data
            owner = db.session.query(Owners).filter_by(email=form.email.data).one()
            category = Categories(category_name=form.category_name.data, owner=owner)
            db.session.add(category)
            db.session.commit()
            url_string = '/category/%s' % category.category_name
            return redirect(url_string)
        else:
            form.email.data = login_session.get('email')
            return render_template('pages/add-category.html', form=form)


@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    """
    Adds new item to database.  Category is on request object.
    :return:
    """
    if login_session.get('email') is not None:
        form = Catalog_Item(request.form)
        owner = db.session.query(Owners).filter_by(email=login_session.get('email')).first()
        if request.method == 'POST' and form.validate():
            # add data

            # get the category object
            category = db.session.query(Categories).filter_by(id=form.category_id.data).first()

            # create a new Item
            item = Items(item_name=form.name.data, owner=owner, category=category)

            # add the descriptoin
            item.description = form.description.data

            # add the filename to the database and upload the file
            # need to validate the file name
            if request.files['picture'].filename is not None:

                filename = request.files['picture'].filename
                filename = secure_filename(filename)

                # returns a UUID with the file extension
                filename = ensure_unique_filename(filename)

                # builds a URL to put in the database
                item.picture = url_for('static', filename="images/" + filename)

                # read the data and write to a file
                image_data = request.files['picture'].read()
                open(os.path.join(os.path.dirname(__file__), 'static/images/',
                                  filename), 'w').write(image_data)

            # add the item and commit to db
            db.session.add(item)
            db.session.commit()

            # build a url for redirection.  Goes back to the same category the
            # item was added in.
            url_string = '/category/%s' % item.category.category_name
            return redirect(url_string)
        else:
            form.category_id.data = request.args.get('category')
            form.id.data = owner.id
        return render_template('pages/add-item.html', form=form)


def ensure_unique_filename(filename):
    file_name_parts = os.path.splitext(filename)
    filename = '%s%s' % (uuid.uuid4().hex, file_name_parts[1], )
    while os.path.exists(os.path.join(os.path.dirname(__file__), 'static/images/', filename)):
        filename = '%s%s' % (uuid.uuid4().hex, file_name_parts[1], )

    return filename


@app.route('/delete-item', methods=['GET', 'POST'])
def delete_item():
    if login_session.get('email') is not None:
        form = Catalog_Item(request.form)

        if request.method == 'POST' and form.validate():
            # delete item
            item = db.session.query(Items).filter_by(id=form.id.data).first()
            try:
                if os.path.basename(item.picture) is not 'default_item.png':
                    os.remove(os.path.join(
                        os.path.dirname(__file__), 'static/images/',
                        os.path.basename(item.picture)))
            except OSError:
                pass

            url_string = '/category/%s' % item.category.category_name
            db.session.delete(item)
            db.session.commit()
            return redirect(url_string)
        else:
            item = db.session.query(Items).filter_by(id=request.args.get('item_id')).first()
            heading = 'Delete Item'
            form.name.data = item.item_name
            form.description.data = item.description
            form.picture.data = item.picture
            form.id.data = request.args.get('item_id')
            form.category_id = item.category_id
            form.submit.data = 'Delete Item'
            return render_template('pages/delete-item.html', form=form, heading=heading)


@app.route('/edit-item', methods=['GET', 'POST'])
def edit_item():
    if login_session.get('email') is not None:
        form = Catalog_Item(request.form)

        if request.method == 'POST' and form.validate():
            # delete item
            item = db.session.query(Items).filter_by(id=form.id.data).first()
            item.item_name = form.name.data
            item.description = form.description.data
            item.insert_date = datetime.datetime.now()
            if request.files['picture'].filename != "":
                # delete file if one exists
                try:
                    if os.path.basename(item.picture) != u'default_item.png':
                        os.remove(os.path.join(
                            os.path.dirname(__file__), 'static/images/',
                            os.path.basename(item.picture)))
                except OSError:
                    pass

                filename = request.files['picture'].filename
                filename = secure_filename(filename)

                # returns a UUID with the file extension
                filename = ensure_unique_filename(filename)

                # builds a URL to put in the database
                item.picture = url_for('static', filename="images/" + filename)

                # read the data and write to a file
                image_data = request.files['picture'].read()
                open(os.path.join(os.path.dirname(__file__), 'static/images/',
                                  filename), 'w').write(image_data)

            db.session.add(item)
            db.session.commit()
            url_string = '/category/%s' % item.category.category_name
            return redirect(url_string)
        else:
            item = db.session.query(Items).filter_by(id=request.args.get('item_id')).first()
            heading = 'Edit Item'
            form.name.data = item.item_name
            form.description.data = item.description
            form.picture.data = item.picture
            form.id.data = request.args.get('item_id')
            form.category_id = item.category_id
            form.submit.data = 'Save Changes'
            return render_template('pages/edit-item.html', form=form, heading=heading)