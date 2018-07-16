# import Flask and jsonify from flask
# import SQLAlchemy from flask_sqlalchemy

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# initialize new flask app
app = Flask(__name__)

# add configurations and database URI
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
# remember that each function must have a unique name
@app.route('/api/users')
def users():
    users = User.query.all()
    users_dict = [user.to_dict() for user in users]
    return jsonify(users_dict)

@app.route('/api/users/<int:id>')
def user_id(id):
    users = User.query.all()
    users_dict = [user.to_dict() for user in users if user.id == id][0]
    return jsonify(users_dict)

@app.route('/api/users/<username>')
def username(username):
    users = User.query.all()
    users_dict = [user.to_dict() for user in users if user.username.lower() == username.lower()][0]
    return jsonify(users_dict)

@app.route('/api/tweets')
def tweets():
    tweets = Tweet.query.all()
    tweets_dict = [tweet.to_dict() for tweet in tweets]
    return jsonify(tweets_dict)

@app.route('/api/tweets/<int:id>')
def tweet_id(id):
    tweets = Tweet.query.all()
    tweets_dict = [tweet.to_dict() for tweet in tweets if tweet.id == id][0]
    return jsonify(tweets_dict)

# Tweets that belong to a user by user_id
    # URL: '/api/users/<int:user_id>/tweets'
@app.route('/api/users/<int:user_id>/tweets')
def user_id_tweets(user_id):
    users = User.query.all()
    users_dict = [user.to_dict() for user in users if user.id == user_id][0]
    return jsonify(users_dict)


# Tweets that belong to a user by a user's name
    # URL:'/api/users/<user_name>/tweets'
@app.route('/api/users/<username>/tweets')
def username_tweets(username):
    users = User.query.all()
    users_dict = [user.to_dict() for user in users if user.username.lower() == username.lower()][0]
    return jsonify(users_dict['tweets'])

# A single User that is associated to a tweet by its id
    # URL: '/api/tweets/<int:tweet_id>/user'
@app.route('/api/tweets/<int:tweet_id>/user')
def user_tweet_id(tweet_id):
    users = User.query.all()
    users_dict = [user.to_dict() for user in users]
    for user in users_dict:
        for tweet in user['tweets']:
            if tweet['id']==tweet_id:
                return jsonify(user)

# run the server
if __name__ == '__main__':
    app.run(debug=True)
