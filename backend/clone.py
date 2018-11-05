from flask import Flask, jsonify, Blueprint, request
from flask_restful import Resource, Api, reqparse, abort
import json
import datetime


user = [{
    "username": "John",
    "email": "john@haha.com",
    "password": "Hahaha123",
    "fullname": "John rukmana"
},
{
    "username": "jeff",
    "email": "jeff@haha.com",
    "password": "Hahaha123",
    "fullname": "John rukmana"
}]

tweet = [{
    "email": "john@haha.com",
    "tweet": "Ini ceritanya tweet Twitter yah"
},
{
    "email": "jeff@haha.com",
    "tweet": "Ini ceritanya tweet Twitter yah"
}]

with open('user.json', 'w') as outfile:  
    json.dump(user, outfile)

with open('tweet.json', 'w') as outfile:  
    json.dump(tweet, outfile)

with open('user.json') as user_file:
    user = json.load(user_file)

with open('tweet.json') as tweet_file:
    tweet = json.load(tweet_file)
    
def addUser():
    with open('user.json', 'w') as outfileuser:
            json.dump(user, outfileuser)
            outfileuser.close()

def addTweet():
    with open('tweet.json', 'w') as outfiletweet:
            json.dump(tweet, outfiletweet)
            outfiletweet.close()


class loookuser(Resource):
    def get(self):
        return user

class looktweet(Resource):
    def get(self):
        return tweet

class login(Resource):
    def post(self):
        email = request.json["email"]
        password = request.json["password"]

        for data in user:
            if data['email'] == email and data['password'] == password:
                return data, 200
            elif data['email'] == email and data['password'] != password:
                return "Please Check Your Password", 400
            elif data['email'] != email and data['password'] == password:
                return "Please Check Your Email"
        return "Please Sign Up", 404
        

def registeredEmail(mail):
    for data in user:
        if data['email'] == mail:
            abort(400, message = "Email Has Been Registered")

def registeredUser(name):
    for data in user:
        if data['username'] == name:
            abort(400, message = "Username Has Been Registered")

class signup(Resource):
    def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                "email",
                help = "Email Required",
                required = True,
                location = ["json"]
            )
            self.reqparse.add_argument(
                "username",
                help = "Username Required",
                required = True,
                location = ["json"]
            )
            self.reqparse.add_argument(
                "password",
                help = "Password Required",
                required = True,
                location = ["json"]
            )
            self.reqparse.add_argument(
                "fullname",
                help = "Full Name Required",
                required = True,
                location = ["json"]
            )
            super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        registeredEmail(request.json['email'])
        registeredUser(request.json['username'])
        user.append(request.json)
        addUser()        
        return "Account Successfully Made", 201

class tweeting(Resource):
    def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                "email",
                help = "Email Required",
                required = True,
                location = ["json"]
            )
            
            self.reqparse.add_argument(
                "tweet",
                help = "Tweet Required",
                required = True,
                location = ["json"]
            )
            super().__init__()
    def post(self):
         data = request.json
         time = str(datetime.datetime.now())
         tmp = {}
         tmp["datetime"] = time
         req = data.copy()
         req.update(tmp)
         args = self.reqparse.parse_args()
         tweet.append(req)
         addTweet()
         return req,201

    def delete(self):
        email = request.json["email"]
        twit = request.json["tweet"]

        for index in range(len(tweet)):
            if tweet[index]['email'] == email and tweet[index]['tweet'] == twit:
                tweet.pop(index)
                addTweet()
                return "Tweet Has Been Deleted", 200
        return "Tweet Not Found", 404

    def put(self):
         email = request.json["email"]
         oldTwit = request.json["old tweet"]
         newTwit = request.json["new tweet"]
         
         for index in range(len(tweet)):
             if tweet[index]['email'] == email and tweet[index]['tweet'] == oldTwit:
                 tweet[index]['tweet'] = newTwit
                 tweet[index]['time'] = str(datetime.datetime.now())
                 addTweet()
                 return "Tweet Has Been Changed", 201
             return "Tweet Not Found", 400
    
    def get(self):
        tweetList = []
        email = request.json['email']
        for twits in tweet:
            if twits['email'] == email:
                tweetList.append(twits['tweet'])
        return tweetList, 200

tweets_api = Blueprint('resources/tweets', __name__)
api = Api(tweets_api)
api.add_resource(loookuser, 'user')
api.add_resource(looktweet,'tweet')
api.add_resource(login, 'login')
api.add_resource(signup, 'signup')
api.add_resource(tweeting, 'tweeting')