# import Flask and jsonify from flask
from flask import Flask, jsonify
# import SQLAlchemy from flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# initialize new flask app
app = Flask (__name__)

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
#
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
def users_all():
    user_dict = [name.to_dict() for name in  User.query.all()]
    return jsonify(user_dict)

@app.route('/api/users/<int:id>')
def user_id(id):
    find_id = [ids.to_dict() for ids in User.query.filter(User.id == id).all()][0]
    return jsonify(find_id)

@app.route('/api/users/<username>')
def user_name(username):
    find_username = [name.to_dict() for name in User.query.filter(User.username == username.title()).all()][0]
    return jsonify(find_username)

@app.route('/api/tweets')
def all_tweet():
    tweet= [tweet.to_dict() for tweet in Tweet.query.all()]
    return jsonify(tweet)

@app.route('/api/tweets/<int:id>')
def tweet_id(id):
    tweet_id = [tweet.to_dict() for tweet in Tweet.query.filter(Tweet.id==id).all()][0]
    return jsonify(tweet_id)

@app.route('/api/users/<int:user_id>/tweets')
def tweet_user_id (user_id):
    find_id = User.query.filter(User.id == user_id).first().to_dict()
    return jsonify(find_id)

@app.route('/api/users/<user_name>/tweets')
def user_name_tweets (user_name):
    tweets = User.query.filter(User.username == user_name.title()).first().tweets
    tweets_dicts = [tweet.to_dict() for tweet in tweets]
    return jsonify(tweets_dicts)

@app.route('/api/tweets/<int:tweet_id>/user')
def tweet_id_user(tweet_id):
    t=Tweet.query.filter(Tweet.id == tweet_id).first().user.to_dict()
    return jsonify(t)





# run the server
if __name__ == "__main__":
    app.run()
