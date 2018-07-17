from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

db.init_app(app)



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

#ROUTES - APIs

#User Routes

@app.route('/api/users')
def api_users():
    return jsonify([user.to_dict() for user in User.query.all()])

@app.route('/api/users/<int:id>')
def api_users_by_id(id):
    user = User.query.get(id)
    return jsonify(user.to_dict())

@app.route('/api/users/<username>')
def api_users_by_username(username):
    user = User.query.filter(User.username.ilike(username)).first()
    return jsonify(user.to_dict())


#Tweet Routes

@app.route('/api/tweets')
def api_tweets():
    return jsonify([tweet.to_dict() for tweet in Tweet.query.all()])

@app.route('/api/tweets/<int:id>')
def api_tweets_by_id(id):
    tweet = Tweet.query.get(id)
    return jsonify(tweet.to_dict())


#Nested Routes

@app.route('/api/users/<int:id>/tweets')
def api_tweets_by_user_id(id):
    user = User.query.get(id)
    return jsonify(user.to_dict())

@app.route('/api/users/<username>/tweets')
def api_tweets_by_username(username):
    user = User.query.filter(User.username.ilike(username)).first()
    return jsonify(user.to_dict()['tweets'])

@app.route('/api/tweets/<int:id>/user')
def api_user_by_tweet_id(id):
    tweet = Tweet.query.get(id)
    return jsonify(tweet.user.to_dict())




if __name__ == '__main__':
    app.run(debug=True)
