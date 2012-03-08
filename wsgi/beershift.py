
import os
import json
import urllib
import bottle
import pymongo
from bson import json_util

bottle.debug(True)

# BreweryDB endpoint for searching beers
# Note: This is the playground endpoint for sample purposes.
#  If you are using this in your own app,
#  you should signup for a brewerydb.com v2 API key
pintlab_url = "http://api.playground.brewerydb.com/search/"
pintlab_key = "A1029384756B"

# connect to the OpenShift MongoDB instance
mongo_connection = pymongo.Connection(os.environ['OPENSHIFT_NOSQL_DB_HOST'],
                                      int(os.environ['OPENSHIFT_NOSQL_DB_PORT']))
mongo_db = mongo_connection[os.environ['OPENSHIFT_APP_NAME']]
mongo_db.authenticate(os.environ['OPENSHIFT_NOSQL_DB_USERNAME'],
                      os.environ['OPENSHIFT_NOSQL_DB_PASSWORD'])

# todo, figure out the bottle json plugin so the json'ing happens correctly and automatically

def model_getUser(username):
    return mongo_db.users.find_one( { 'username': username } )

def model_getUserBeers(username):
    # php $beers = $this->mongo_db->limit(50)->order_by(array('when' => 'DESC'))->get_where('drank', array('username' => $username));
    return list(mongo_db.drank.find( { 'username': username } ).sort('when', pymongo.DESCENDING).limit(50))

def model_getFirehoseBeers():
    # php $beers = $this->mongo_db->limit(50)->order_by(array('when' => 'DESC'))->get('drank');
    return list(mongo_db.drank.find().sort('when', pymongo.DESCENDING).limit(50))

def model_createUser(username, password):
    # php $user = array('username' => $username, 'password' => $password);
    # php $this->mongo_db->insert('users', $user);
    return mongo_db.users.insert( { 'username': username, 'password' : password }, safe=True)

def model_drinkbeer(username, beerName, when):
    # php $user = array('username' => $username, 'beer' => $beerName, 'when' => $when);
    # php $this->mongo_db->insert('drank', $user);
    return mongo_db.drank.insert( { 'username': username, 'beer' : beerName, 'when' : when }, safe=True)



@bottle.get('/user/username/<username>')
def rest_get_user(username):
    r = model_getUser(username.lower())
    if r == None: bottle.abort(404, "No such user")
    bottle.response.content_type = 'application/json'
    return json.dumps(r, default=json_util.default)

@bottle.post('/user/username/<username>/password/<password>')
def rest_post_user(username, password):
    r = model_createUser(username.lower(), password)
    if r == None:
        resp = { 'status': 'failed' }
    else:
        resp = { 'status': 'success' }
    bottle.response.content_type = 'application/json'
    return json.dumps(resp, default=json_util.default)

@bottle.get('/userbeers/username/<username>')
def rest_get_userbeers(username):
    r = model_getUserBeers(username.lower())
    if r == None: bottle.abort(404, "No such user")
    bottle.response.content_type = 'application/json'
    return json.dumps(r, default=json_util.default)

@bottle.get('/firehose')
def rest_get_firehose():
    r = model_getFirehoseBeers()
    if r == None: bottle.abort(404, "No beers")
    bottle.response.content_type = 'application/json'
    return json.dumps(r, default=json_util.default)

@bottle.get('/beers/name/<beername>')
def rest_get_beers(beername):
    u = urllib.urlopen(pintlab_url,
                       urllib.urlencode({ 'key' : pintlab_key,
                                          'type' : 'beer',
                                          'withBreweries' : 'Y',
                                          'q' : beername }))
    u_code = u.getcode()
    if u_code != 200:
        bottle.abort(404, "pintlab result code %s" % u_code)
    return json.load(u)


@bottle.post('/beers/username/<username>/beerName/<beerName>/when/<when>')
def do_post_beers():
    r = model_drinkbeer(username.lower(), beerName, when)
    if r == None:
        resp = { 'status': 'failed' }
    else:
        resp = { 'status': 'success' }
    bottle.response.content_type = 'application/json'
    return json.dumps(resp, default=json_util.default)


@bottle.get('/')
def do_get_root():
    # TODO do the same as BeerShiftWeb/php/application/views/welcome_message_php
    return '<html><body>Hello World</body></html>'



# bottle.run(host='localhost', port=8080, reloader=True)

application = bottle.default_app()

