from flask import request
from flask import make_response
from flask import session
import os
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from webExample import app
from webExample import db
from webExample import Owners


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Logs a user into Google Plus. Code pretty much lifted from
    UD330 on github and the lecture.  I've added a few small changes
    to send user data back to client and create a record for the user
    in the database on successful login
    """
    # Validate state token
    try:
        testVar = session['state']
    except KeyError:
        session['state'] = request.args.get('state')

    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    # request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        cs_file_path = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
        oauth_flow = flow_from_clientsecrets(cs_file_path, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get the client id from a local file
    cs_file_path = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
    CLIENT_ID = json.loads(
        open(cs_file_path, 'r').read())['web']['client_id']


    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get current values for access token and gplus id from session
    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = access_token
    # session['credentials'] = credentials
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # store user info in session object for use else in the app
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    # check if this is a new user and if so add him/her to database
    check_email(session.get('email'), session.get('username'))

    # return some data to the client side for use in the front end
    return json.dumps(
        {'auth_service': 'Google', 'picture': data['picture'],
         'name': data['name'], 'email': data['email'],
         'social_id': session['gplus_id']})


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
    Logins a user into FB with an access token.  Code pretty much lifted from
    UD330 on github and the lecture.
    """
    try:
        testVar = session['state']
    except KeyError:
        session['state'] = request.args.get('state')

    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    # print "access token received %s " % access_token

    cs_file_path = os.path.join(os.path.dirname(__file__), 'fb_client_secrets.json')
    app_id = json.loads(
        open(cs_file_path, 'r').read())['web']['app_id']
    app_secret = json.loads(
        open(cs_file_path, 'r').read())['web']['app_secret']

    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email,picture' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data["email"]
    session['facebook_id'] = data["id"]

    # The token must be stored in the session in order to properly
    # logout, let's strip out the information before the equals sign in
    # our token

    stored_token = token.split("=")[1]
    session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=20&width=20' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]

    returnData = {}
    returnData['auth_service'] = "Facebook"
    returnData['picture'] = session['picture']
    returnData['name'] = session['username']
    returnData['email'] = session['email']
    returnData['social_id'] = session['facebook_id']

    check_email(session.get('email'), session.get('username'))

    jsonReturn = json.dumps(returnData)
    # flash("Now logged in as %s" % session['username'])
    return jsonReturn

@app.route('/fbdisconnect', methods=['POST'])
def fbdisconnect():
    """
    Logs a user out of FB. Code pretty much lifted from
    UD330 on github and the lecture.
    """
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token, )
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    session.clear()
    return "you have been logged out"

@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    """
    Logs a user out of GooglePlus. Code pretty much lifted from
    UD330 on github and the lecture.
    """
    # Only disconnect a connected user.
     # session['access_token'] = access_token
    access_token = session['access_token']
    # credentials = session.get('credentials')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        session.clear()
        response = make_response(
            json.dumps('Logged outr.', 200))
        response.headers['Content-Type'] = 'application/json'
        return response


def check_email(email, name):
    """
    Checks if an email address exists for user in db after oauth
    :param email: oauth email
    :param name: oauth name if record needs to be added
    """
    owner = db.session.query(Owners).filter_by(email=email).first()
    if owner is None:
        # add owner to database
        new_owner = Owners(owner_name=name, email=email)
        db.session.add(new_owner)
        db.session.commit()
    return
