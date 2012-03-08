
import os
import bottle
import pymongo

bottle.debug(True)

mongo_connection = pymongo.Connection(os.environ['OPENSHIFT_NOSQL_DB_HOST'],
                                      int(os.environ['OPENSHIFT_NOSQL_DB_PORT']))
mongo_db = mongo_connection[os.environ['OPENSHIFT_APP_NAME']]
mongo_db.authenticate(os.environ['OPENSHIFT_NOSQL_DB_USERNAME'],
                      os.environ['OPENSHIFT_NOSQL_DB_PASSWORD'])

def model_getUser(username):
    return mongo_db.users.find_one( { 'username': username } )

def model_getUserBeers(username):
    # php $beers = $this->mongo_db->limit(50)->order_by(array('when' => 'DESC'))->get_where('drank', array('username' => $username));
    return mongo_db.drank.find( { 'username': username } ).sort('when','DESCENDING').limit(50)

def model_getFirehoseBeers():
    # php $beers = $this->mongo_db->limit(50)->order_by(array('when' => 'DESC'))->get('drank');
    return mongo_db.drank.sort('when', 'DESCENDING').limit(50)

def model_createUser(username, password):
    # php $user = array('username' => $username, 'password' => $password);
    # php $this->mongo_db->insert('users', $user);
    mongo_db.users.insert( { 'username': username, 'password' : password } )
    # what did the php version return?
    return None

def model_drinkbeer(username, beerName, when):
    # php $user = array('username' => $username, 'beer' => $beerName, 'when' => $when);
    # php $this->mongo_db->insert('drank', $user);
    mongo_db.drank.insert( { 'username': username, 'beer' : beerName, 'when' : when } )
    # what did the php version return?
    return None


@bottle.get('/user/username/<username>')
def rest_get_user(username):
    # if no username, respond 400
    # downcase username
    # php $user = $this->usermodel->getUser($username);
    # if no user, respond 404
    # respond 200 json $user
    return r'[{"_id":{"$id":"4f2813c9667c765b7f000009"},"username":"openshift","password":"paas"}]'

@bottle.post('/user/username/<username>/password/<password>')
def rest_post_user(username, password):
    # if no username or no password, respond 400
    # downcase username
    # php $result = $this->usermodel->createUser($username, $this->post('password'));
    # if ($result === FALSE) { $this->response(array('status' => 'failed')); }
    # else { $this->response(array('status' => 'success')); }
    return ""

@bottle.get('/userbeers/username/<username>')
def rest_get_userbeers(username):
    # if no username, respond 400
    # downcase username
    # php $user = $this->usermodel->getUserBeers($username);    
    # if no user, respond 404
    # respond 200 json $user
    return r'[{"_id":{"$id":"4f301cd2667c76925a000001"},"username":"openshift","beer":"Leffe Blonde","when":"February 6th, 2012, 1:32:53 PM"},{"_id":{"$id":"4f301c66667c76197f000000"},"username":"openshift","beer":"Westmalle Trappist Dubbel","when":"February 6th, 2012, 1:31:05 PM"},{"_id":{"$id":"4f30072a667c76925a000000"},"username":"openshift","beer":"Westmalle Trappist Dubbel","when":"February 6th, 2012, 12:00:28 PM"},{"_id":{"$id":"4f444c94a4035fa127000000"},"username":"openshift","beer":"Westmalle Trappist Tripel","when":"February 21st, 2012, 9:02:28 PM"},{"_id":{"$id":"4f444059a4035f2329000000"},"username":"openshift","beer":"Belgian Piraate","when":"February 21st, 2012, 8:10:17 PM"},{"_id":{"$id":"4f3c0a6a667c760454000000"},"username":"openshift","beer":"Live Oak Pale Ale","when":"February 15th, 2012, 2:41:43 PM"}]'

@bottle.get('/firehose')
def rest_get_firehose():
    # php $beers = $this->usermodel->getFirehoseBeers();
    # if no beers, respond 404
    # respond 200 json $beers
    return r'[{"_id":{"$id":"4f4fe41ca4035fdf02000002"},"username":"lefromage","beer":"Bokrijks Kruikenbier","when":"March 1st, 2012, 10:03:23 PM"},{"_id":{"$id":"4f3192b4667c76197f00000b"},"username":"djuengst","beer":"Dark Lager","when":"February 7th, 2012, 4:08:03 PM"},{"_id":{"$id":"4f318d86667c76925a000007"},"username":"lushbag25","beer":"Holy Sheet","when":"February 7th, 2012, 3:45:58 PM"},{"_id":{"$id":"4f3075bd667c76925a000003"},"username":"alex","beer":"Gaelic Ale","when":"February 6th, 2012, 7:52:12 PM"},{"_id":{"$id":"4f3075b1667c76197f000003"},"username":"alex","beer":"Gaelic Ale","when":"February 6th, 2012, 7:52:00 PM"},{"_id":{"$id":"4f301cd2667c76925a000001"},"username":"openshift","beer":"Leffe Blonde","when":"February 6th, 2012, 1:32:53 PM"},{"_id":{"$id":"4f301c66667c76197f000000"},"username":"openshift","beer":"Westmalle Trappist Dubbel","when":"February 6th, 2012, 1:31:05 PM"},{"_id":{"$id":"4f30072a667c76925a000000"},"username":"openshift","beer":"Westmalle Trappist Dubbel","when":"February 6th, 2012, 12:00:28 PM"},{"_id":{"$id":"4f302ddd667c76197f000002"},"username":"apple","beer":"Amstel Light","when":"February 6th, 2012, 11:45:31 AM"},{"_id":{"$id":"4f30b92c667c76197f000007"},"username":"cici","beer":"Naughty Girl","when":"February 6th, 2012, 11:39:55 PM"},{"_id":{"$id":"4f47a3faa4035ff12d000001"},"username":"llq","beer":"Green Beer","when":"February 24th, 2012, 10:51:38 PM"},{"_id":{"$id":"4f444c94a4035fa127000000"},"username":"openshift","beer":"Westmalle Trappist Tripel","when":"February 21st, 2012, 9:02:28 PM"},{"_id":{"$id":"4f4450e7a4035fe718000004"},"username":"lefromage","beer":"Dark Lager","when":"February 21st, 2012, 8:20:23 PM"},{"_id":{"$id":"4f4450dba4035fe718000003"},"username":"lefromage","beer":"Heineken","when":"February 21st, 2012, 8:20:11 PM"},{"_id":{"$id":"4f444059a4035f2329000000"},"username":"openshift","beer":"Belgian Piraate","when":"February 21st, 2012, 8:10:17 PM"},{"_id":{"$id":"4f444ceca4035fa127000001"},"username":"lefromage","beer":"Wild West Beer","when":"February 21st, 2012, 8:03:23 PM"},{"_id":{"$id":"4f444cdba4035fe718000002"},"username":"lefromage","beer":"West Highland","when":"February 21st, 2012, 8:03:06 PM"},{"_id":{"$id":"4f444c99a4035fe718000001"},"username":"lefromage","beer":"West Highland","when":"February 21st, 2012, 8:01:56 PM"},{"_id":{"$id":"4f3c0a6a667c760454000000"},"username":"openshift","beer":"Live Oak Pale Ale","when":"February 15th, 2012, 2:41:43 PM"},{"_id":{"$id":"4f3c0ae9667c76e431000000"},"username":"diwant","beer":"Firemans #4","when":"February 15th, 2012, 1:43:35 PM"},{"_id":{"$id":"4f36c7d5667c76e56e000001"},"username":"danjay","beer":"IPA","when":"February 11th, 2012, 2:56:05 PM"}]'

@bottle.get('/beers/name/<beername>')
def rest_get_beers(beername):
    # search pintlab for beername
    return ""

@bottle.post('/beers/')
def do_post_beers():
    # parameter username
    # parameter beerName
    # parameter when
    # lowercase username
    # php $result = $this->usermodel->drinkBeer($username, $this->post('beerName'), $this->post('when'));
    # if ($result === FALSE) { $this->response(array('status' => 'failed')); }
    # else { $this->response(array('status' => 'success')); }
    return ""

application = bottle.default_app()

# bottle.run(host='localhost', port=8080)
