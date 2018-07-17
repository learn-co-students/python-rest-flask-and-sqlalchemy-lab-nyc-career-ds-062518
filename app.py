from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy


# initialize new flask app
app=Flask(__name__)

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
#for users
@app.route('/api/users')
def users():
    users=User.query.all()
    dict=[user.to_dict() for user in users]
    return jsonify(dict)

@app.route('/api/users/<int:id>')
def id(id):
    user=User.query.filter(User.id == id).first()
    return jsonify(user.to_dict())

@app.route('/api/users/<username>')
def username(username):
    user=User.query.filter(User.username.like(username)).first()
    return jsonify(user.to_dict())

#for tweets
@app.route('/api/tweets')
def tweets():
    tweets=Tweet.query.all()
    dict=[tweet.to_dict() for tweet in tweets]
    return jsonify(dict)


@app.route('/api/tweets/<int:id>')
def tweets_id(id):
    tweeter = Tweet.query.filter(Tweet.id == id).first()
    return jsonify(tweeter.to_dict())

#bonus questions
@app.route('/api/users/<int:user_id>/tweets')
def tweets_user_id(user_id):
    users= User.query.filter(User.id==user_id).first()
    return jsonify(users.to_dict())

@app.route('/api/users/<user_name>/tweets')
def tweet_user_name(user_name):
    user=User.query.filter(User.username.like(user_name)).first()
    user_dict=user.to_dict()
    return jsonify(user_dict['tweets'])

@app.route('/api/tweets/<int:tweet_id>/user')
def tweet_tweet_id(tweet_id):
    tweeter = Tweet.query.filter(Tweet.id == tweet_id).first().to_dict()
    tweeter_tweet =User.query.filter(tweeter['user']== User.username).first()
    return jsonify(tweeter_tweet.to_dict())
    # tweets=Tweet.query.all()
    # tweet_dict=[tweet.to_dict() for tweet in tweets if tweet.id == tweet_id][0]
    # return jsonify(tweet_dict['user'])



# define routes and their respective functions that return the correct data
# remember that each function must have a unique name

if __name__ == '__main__':
    app.run(debug=True)
# run the server
