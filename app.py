# import Flask and jsonify from flask
from flask import Flask, jsonify
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# initialize new flask app
app = Flask(__name__)

# add configurations and database URI

app.config['DEBUG']= True
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///app.db'
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
    return jsonify([user.to_dict() for user in User.query.all()])

@app.route('/api/users/<int:id>')
def user_id(id):
    return jsonify([user.to_dict() for user in User.query.all() if user.id == id][0])

@app.route('/api/users/<username>')
def username(username):
    return jsonify([user.to_dict() for user in User.query.all() if username.lower() ==user.username.lower()][0])

@app.route('/api/tweets')
def tweets():
    return jsonify([tweet.to_dict() for tweet in Tweet.query.all()])

@app.route('/api/tweets/<int:id>')
def tweet(id):
    return jsonify([tweet.to_dict() for tweet in Tweet.query.all() if tweet.id == id][0])

@app.route('/api/users/<int:user_id>/tweets')
def user_tweet(user_id):
    # all_users = [user.to_dict() for user in User.query.all()]
    return jsonify([user.to_dict() for user in User.query.all() if user.id == user_id][0])
    # return jsonify([user for user in all_users for i in range(0,lenif all_users["tweets"][i]["user_id"] == user_id])

@app.route('/api/users/<user_name>/tweets')
def username_tweet(user_name):
    all_tweets = [tweet.to_dict() for tweet in Tweet.query.all()]
    return jsonify([tweet for tweet in all_tweets if tweet["user"].lower() == user_name.lower()])

@app.route('/api/tweets/<int:tweet_id>/user')
def tweet_id(tweet_id):
    all_users = [user.to_dict() for user in User.query.all()]
    return jsonify([user for user in all_users if user["tweets"][0]["id"]==tweet_id][0])


# # # run the server
if __name__ == "__main__":
    app.run(debug=True)
