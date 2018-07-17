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

#uncomment models
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
def func_1():
    return jsonify([user.to_dict() for user in db.session.query(User).all()])
@app.route('/api/users/<int:id>')
def func_2(id):
    return jsonify([user.to_dict() for user in db.session.query(User).all() if user.id == id][0])
@app.route('/api/users/<username>')
def func_3(username):
    return jsonify([user.to_dict() for user in db.session.query(User).all() if user.username.upper() == username.upper()][0])
@app.route('/api/tweets')
def func_4():
    return jsonify([tweet.to_dict() for tweet in db.session.query(Tweet).all()])
@app.route('/api/tweets/<int:id>')
def func_5(id):
    return jsonify([tweet.to_dict() for tweet in db.session.query(Tweet).all() if tweet.id == id][0])
@app.route('/api/users/<int:user_id>/tweets')
def func_6(user_id):
    return jsonify([user.to_dict() for user in db.session.query(User).all() if user.id == user_id][0])
@app.route('/api/users/<user_name>/tweets')
def func_7(user_name):
    tweets_list = [user.tweets for user in db.session.query(User).all() if user.username.upper() == user_name.upper()]
    return jsonify([a_tweet.to_dict() for tweet in tweets_list for a_tweet in tweet])
@app.route('/api/tweets/<int:tweet_id>/user')
def func_8(tweet_id):
    return jsonify([tweet.user.to_dict() for tweet in db.session.query(Tweet).all() if tweet.id == tweet_id][0])

# run the server
if __name__ == '__main__':
    app.run(debug = True)
