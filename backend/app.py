from flask import Flask, Blueprint, request
from clone import tweets_api
from flask_cors import CORS
import debugger
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
import clone
import os
import json
from flask_restful import marshal, fields

POSTGRES = {
    'user' : 'postgres',
    'pw' : 'please',
    'db' : 'Twitter',
    'host' : '127.0.0.1',
    'port' : '17711'
    }

app = Flask(__name__)
CORS(app)
app.register_blueprint(tweets_api, url_prefix = '/api/v1/')

# app.config['SQLACHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config.update(dict(
    SECRET_KEY="bebas",
    WTF_CSRF_SECRET_KEY="apa aja"
))
# 'postgresql://postgres:daniel171212'
db = SQLAlchemy(app)

#class buat ngeget
class user(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    fullname = db.Column(db.String())
    email = db.Column(db.String())
    passwords = db.Column(db.String())
    tweet = db.Column(db.String())

    def __init__(self,username,fullname,email,passwords,tweet):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.passwords = passwords
        self.tweet = tweet

#class buat ngepost
class postForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    fullname = StringField('Fullname',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    passwords = StringField('Passwords',validators=[DataRequired()])
    tweet = StringField('Tweet',validators=[DataRequired()])

tweet_json = {
    'id' : fields.Integer,
    'username' : fields.String,
    'fullname' : fields.String,
    'email' : fields.String,
    'passwords' : fields.String,
    'tweet' : fields.String
    }

# resource_fields = {
#     'id' : fields.Integer,
#     'username' : fields.String,
#     'fullname' : fields.String,
#     'email' : fields.String,
#     'passwords' : fields.String,
#     'tweet' : fields.String
#     }

@app.route('/getTweet')
def view_data():
    tweet = user.query.all()
    print(tweet)
    print (json.dumps(marshal(tweet, tweet_json)))
    return json.dumps(marshal(tweet, tweet_json))
    return 'sukses',200
    
# def get_tweet():
#     tweet = user.query.all()
#     print(tweet)
#     return 'sukses bos',200

@app.route('/postTweet', methods=['POST'])
def post_tweet():
    addtweet = postForm()
    if request.method == 'POST':
        at = user(
            addtweet.username.data,
            addtweet.fullname.data,
            addtweet.email.data,
            addtweet.passwords.data,
            addtweet.tweet.data
        )
        db.session.add(at)
        db.session.commit()
        print(request.get_json())
        return 'bisa bos',201
    else:
        return 'hello'

@app.route('/')
def hello():
    return "Hello"

if __name__ == '__main__':
    app.run(debug = True)