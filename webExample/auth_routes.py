from flask import Flask, render_template, json, request, redirect
from flask import jsonify, url_for, flash, make_response
from flask import session
import requests
import os
from flask import Response
import psycopg2
import random
import contextlib
import json
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from webExample import app

cs_file_path = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
CLIENT_ID = json.loads(
    open(cs_file_path, 'r').read())['web']['client_id']


@app.route('/gconnect', methods=['POST'])
def gconnect():
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

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

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

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    returnData = {'auth_service': 'Google', 'picture': data['picture'],
                  'name': data['name'], 'email': data['email'],
                  'social_id': session['gplus_id']}

    json_returned = json.dumps(returnData)
    return json_returned


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
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
    app_id = json.loads(open(cs_file_path, 'r').read())[
        'web']['app_id']
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

    jsonReturn = json.dumps(returnData)
    # flash("Now logged in as %s" % session['username'])
    return jsonReturn

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

@app.route('/gdisconnect')
def gdisconnect():
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
