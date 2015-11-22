from flask import render_template, request, redirect, url_for
from flask import session as login_session
from webExample import app
from webExample import db
from webExample import Owners, Categories, Items
import random
import string

from form_classes import Catalog_Item, Category
from wtforms import Field

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


@app.route('/')
def index():
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
    if login_session.get('email') is not None:
        form = Catalog_Item(request.form)
        owner = db.session.query(Owners).filter_by(email=login_session.get('email')).first()
        if request.method == 'POST' and form.validate():
            # add data
            category = db.session.query(Categories).filter_by(id=form.category_id.data).first()
            item = Items(item_name=form.name.data, owner=owner, category=category)
            item.description = form.description.data
            item.picture = form.picture.data
            db.session.add(item)
            db.session.commit()
            url_string = '/category/%s' % item.category.category_name
            return redirect(url_string)
        else:
            form.category_id.data = request.args.get('category')
            form.id.data = owner.id
        return render_template('pages/add-item.html', form=form)


@app.route('/delete-item', methods=['GET', 'POST'])
def delete_item():
    if login_session.get('email') is not None:
        form = Catalog_Item(request.form)

        if request.method == 'POST' and form.validate():
            # delete item
            item = db.session.query(Items).filter_by(id=form.id.data).first()
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
            item.picture = form.picture.data
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