from flask import Flask, request, json, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal, fields
import datetime
import os
from flask_cors import CORS, cross_origin
import jwt

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:please@localhost:17711/Twitter'
app.config['SECRET_KEY'] = os.urandom(24)
jwtSecretKey = "apajadah"

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

        # check if email exist in db
        req_email = request_data.get('email')
        req_password = request_data.get('password')
        userDB = User.query.filter_by(email=req_email, password=req_password).first()
        if userDB is not None:
        # if userDB is not None:
            payload = {
                "email": userDB.email,
                "username" : userDB.username,
                "password" : userDB.password,
                "secretcode": "lebahganteng"
            }

            encoded = jwt.encode(payload, jwtSecretKey, algorithm='HS256')
            print(encoded)
            return encoded, 200    
            # json_format = {
            #     'username': fields.String,
            #     'fullname': fields.String,
            #     'email': fields.String,
            #     'id': fields.String
            # }
            # user_json = json.dumps(marshal(userDB, json_format))
            # return user_json, 200
        else:
            return "CHECK YOUR USERNAME OR PASSWORD AGAIN", 404

    else:
        return 'METHOD NOT ALLOWED', 405

def set_cookies(username):
    resp = make_response('')
    resp.set_cookie('username', username)
    return resp

@app.route('/getProfile', methods=['POST'])
def getProfile():
    if request.method == 'POST':
        decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
        # request_data = request.get_json()
        # check if email exist in db
        req_username = decoded["username"]
        print("test")
        userDB = User.query.filter_by(username=req_username).first()
        if userDB is not None:
            json_format = {
                'id': fields.String,
                'username': fields.String,
                'fullname': fields.String,
                'email': fields.String,
                'bio': fields.String,
                'photoprofile': fields.String
            }
            user_json = json.dumps(marshal(userDB, json_format))
            return user_json, 200
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

    # request_data = request.get_json()
    req_username = request_data.get('username')

    # check inside the DB
    userDB = Tweets.query.join(User, User.id==Tweets.person_id).add_columns(User.id,User.username,User.fullname,User.photoprofile,Tweets.content,Tweets.date).all()
    userArr = []

    for dataUser in userDB:
        test = {
            "id": dataUser[1],
            "username": dataUser[2],
            "fullname": dataUser[3],
            "photoprofile": dataUser[4],
            "content": dataUser[5],
            "date": dataUser[6]
        }
        userArr.append(test)

    # convert to JSON
    json_format = {
        'id': fields.Integer,
        'username': fields.String,
        'fullname': fields.String,
        'photoprofile': fields.String,
        'content': fields.String,
        'date': fields.DateTime
    }
    tweets_json = json.dumps(marshal(userArr, json_format))
    print(tweets_json)
    return tweets_json, 200

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
@app.route('/deletetweet', methods=['DELETE'])
def delete_tweet():
    request_data = request.get_json()
    req_username = request_data.get('username')

    if request.method == 'DELETE':
        userDB = Person.query.filter_by(username=req_username).first()
        userTweets = userDB.tweets

        print(userTweets)
        print(userTweets[0])
        db.session.delete(userTweets[0])
        db.session.commit()
        return 'Fatality', 200

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