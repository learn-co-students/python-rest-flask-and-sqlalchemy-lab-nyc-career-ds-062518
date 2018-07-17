# import Flask and jsonify from flask
from flask import Flask, render_template, jsonify
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import *
# from flask_migrate import Migrate

# initialize new flask app
app = Flask(__name__)

# add configurations and database URI
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLAlCHEMY_ECHO']= True

# connect SQLAlchemy to the configured flask app
db = SQLAlchemy(app)

# uncomment models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    tweets = db.relationship('Tweet', backref='users', lazy=True)
    def to_dict(self):
        user = {'id': self.id, 'username': self.username, 'tweets': [tweet.to_dict() for tweet in self.tweets]}
        return user

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates="tweets")
    def to_dict(self):
        tweet = {'id': self.id, 'text': self.text, 'user_id': self.user.id, 'user': self.user.username}
        return tweet



# define routes and their respective functions that return the correct data

@app.route('/api/users')
def all_users():
    x = [user.to_dict() for user in User.query.all()]
    return jsonify(x)

@app.route('/api/users/<int:id>')
def users_by_id(id):
    x = [user.to_dict() for user in User.query.filter(User.id == id)][0]
    return jsonify(x)

@app.route('/api/users/<username>')
def users_by_username(username):
    x = [user.to_dict() for user in User.query.filter(User.username == username.title())][0]
    return jsonify(x)

@app.route('/api/tweets')
def all_tweets():
    x = [tweet.to_dict() for tweet in Tweet.query.all()]
    return jsonify(x)

@app.route('/api/tweets/<int:id>')
def tweets_by_id(id):
    x = [tweet.to_dict() for tweet in Tweet.query.filter(Tweet.id == id)][0]
    return jsonify(x)

@app.route('/api/users/<int:user_id>/tweets')
def tweets_user_by_userid(user_id):
    x = [user.to_dict() for user in User.query.filter(User.id == user_id)][0]
    return jsonify(x)

@app.route('/api/users/<user_name>/tweets')
def tweets_user_by_username(user_name):
    for user in User.query.filter(User.username == user_name.title()):
        user_id = user.id
    tweets = [tweet.to_dict() for tweet in Tweet.query.filter(Tweet.user_id == user_id)]
    # for user in User.query.filter(User.username == user_name.title()):
    #     tweets.append({'user':user.username})
    #     tweets.append({'id':user.id})
    return jsonify(tweets)

@app.route('/api/tweets/<int:tweet_id>/user')
def user_by_tweet_id(tweet_id):
    for tweet in Tweet.query.filter(Tweet.id == tweet_id):
        user_id = tweet.user_id
    user = [user.to_dict() for user in User.query.filter(User.id == user_id)][0]
    return jsonify(user)

# remember that each function must have a unique name





# run the server
if __name__ == "__main__":
    app.run()
