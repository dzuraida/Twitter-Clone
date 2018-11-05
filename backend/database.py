from flask import Flask, request, json, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal, fields
import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:please@localhost:17711/Twitter'
POSTGRES = {
    'user' : 'postgres',
    'pw' : 'please',
    'db' : 'Twitter',
    'host' : '127.0.0.1',
    'port' : '17711'
    }
app.config.update(dict(
    SECRET_KEY="bebas",
    WTF_CSRF_SECRET_KEY="apa aja"
))

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    fullname = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    bio = db.Column(db.String(250))
    photoprofile = db.Column(db.String())
    tweets = db.relationship('Tweets', backref='owner')

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

@app.route('/signup', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        request_data = request.get_json()
        # print(request_data)

        # construct data to be sent to DB
        sent_data = User(
            username = request_data.get('username'),
            fullname = request_data.get('fullname'),
            email = request_data.get('email'),
            password = request_data.get('password'),
            bio = request_data.get('bio'),
            photoprofile = request_data.get('photoprofile')
        )

        # add to db
        db.session.add(sent_data)
        db.session.commit()

        return 'SUCCESS', 201
    else:
        return 'Method Not ALLOWED', 405

# login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_data = request.get_json()

        # check if username exist in db
        req_email = request_data.get('email')
        req_password = request_data.get('password')
        userDB = User.query.filter_by(username=req_email, password=req_password).first()
        if userDB is not None:
            return "LOGIN SUCCESS", 200
        else:
            return "CHECK YOUR USERNAME OR PASSWORD AGAIN", 404

    else:
        return 'METHOD NOT ALLOWED', 405

# @app.route('/setcookie')
# def set_cookie():
#     resp = make_response('')
#     resp.set_cookie('username', username)
#     return resp

# tweeting
@app.route('/tweeting', methods=['POST'])
def tweeting():
    if request.method == 'POST':
        request_data = request.get_json()

    # check if username in existed DB
    req_username = request_data.get('username')
    req_tweet = request_data.get('tweet')
    userDB = User.query.filter_by(username=req_username).first()
    if userDB is not None:
        tweet = Tweets(
            content = req_tweet,
            owner = userDB
        )

        # add to db
        db.session.add(tweet)
        db.session.commit()

        return 'YOU ARE TWEETING', 201
    else:
        return 'YOU SHOULD BE LOGIN FIRST',500

# get tweet
@app.route("/Tweet", methods=['POST'])
def get_tweet():
    
    request_data = request.get_json()
    print(request_data)

    # request_data = request.get_json()
    req_username = request_data.get('username')

    # check inside the DB
    userDB = User.query.filter_by(username=req_username).first()
    user_tweets = userDB.tweets

    # convert to JSON
    json_format = {
        'content': fields.String,
        'date': fields.DateTime
    }
    tweets_json = json.dumps(marshal(user_tweets, json_format))
    return tweets_json

# editing route
@app.route('/editprofile', methods=['PUT'])
def edit_profile():
    request_data = request.get_json()
    req_username = request_data.get('username')

    # new data
    new_username = request_data.get('new_username')
    new_fullname = request_data.get('new_fullname')
    new_email = request_data.get('new_email')
    new_bio = request_data.get('new_bio')
    new_photoprofile = request_data.get('new_photoprofile')

    if request.method == 'PUT':
        userDB = User.query.filter_by(username=req_username).first()
        userDB.username = new_username
        userDB.fullname = new_fullname
        userDB.email = new_email
        userDB.bio = new_bio
        userDB.photoprofile = new_photoprofile
        db.session.commit()
        return 'DATA EDITED', 200
    else:
        return 'FAILED EDIT DATA',405

@app.route('/editpassword', methods=['PUT'])
def edit_password():
    request_data = request.get_json()
    req_username = request_data.get('username')
    req_password = request_data.get('password')
    req_validate = request_data.get('validate')

    # new data
    new_password = request_data.get('new_password')

    if request.method == 'PUT':
        userDB = User.query.filter_by(username=req_username).first()
        if userDB is not None and userDB.password == req_password: 
            if new_password == req_validate:
                userDB.password = new_password
                db.session.commit()
                return 'PASSWORD CHANGED', 200
            else:
                return 'VALIDATE YOUR PASSWORD'
    else:
        return 'FAILED CHANGE PASSWORD',405

# delete tweet routing
# @app.route('/delete', methods=['DELETE'])
# def delete_tweet():

# set session
@app.route('/setsession')
def set_session():
    session['username'] = '@dira'
    return 'session has been set',200

@app.route('/readsession')
def read_session():
    if 'username' in session:
        return 'session ' + session['username'] + ' does exist'
    else:
        return 'session does not exist, please log in'
        
@app.route('/dropsession')
def drop_session():
    session.pop('username', None)
    return 'session has been dropped'

# cookie
@app.route('/setcookie')
def set_cookie():
    username = '@dira'
    resp = make_response('')
    resp.set_cookie('username', username)
    return resp

@app.route('/readcookie')
def read_cookie():
    cookie = request.cookie.get('username')
    return 'the cookie is '+cookie, 200

if __name__ == '__main__':
    app.run(debug=True)