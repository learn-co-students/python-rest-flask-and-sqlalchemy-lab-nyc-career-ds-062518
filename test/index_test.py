import os, unittest, tempfile, sys, json
sys.path.insert(0, '..')
from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_users_index(self):
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        users = [{'id': 1, 'tweets': [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}], 'username': 'Jeff'}, {'id': 2, 'tweets': [{'id': 4, 'text': 'RPDR is the best show', 'user': 'Rachel', 'user_id': 2}, {'id': 5, 'text': 'I just made the coolest NPM package!', 'user': 'Rachel', 'user_id': 2}, {'id': 6, 'text': 'Running is so fun!', 'user': 'Rachel', 'user_id': 2}], 'username': 'Rachel'}, {'id': 3, 'tweets': [{'id': 7, 'text': 'I love hogs', 'user': 'Daniel', 'user_id': 3}, {'id': 8, 'text': 'Hogs are the best way to teach react', 'user': 'Daniel', 'user_id': 3}, {'id': 9, 'text': 'Programming is lyfe', 'user': 'Daniel', 'user_id': 3}], 'username': 'Daniel'}]
        self.assertEqual(json_data, users)

    def test_users_by_id(self):
        response = self.app.get('/api/users/1')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        user = {'id': 1, 'tweets': [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1},
        {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}], 'username': 'Jeff'}
        self.assertEqual(json_data, user)

    def test_users_by_name(self):
        response = self.app.get('/api/users/jeff')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        user = {'id': 1, 'tweets': [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}], 'username': 'Jeff'}
        self.assertEqual(json_data, user)

    def test_tweets_index(self):
        response = self.app.get('/api/tweets')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        tweets = [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}, {'id': 4, 'text': 'RPDR is the best show', 'user': 'Rachel', 'user_id': 2}, {'id': 5, 'text': 'I just made the coolest NPM package!', 'user': 'Rachel', 'user_id': 2}, {'id': 6, 'text': 'Running is so fun!', 'user': 'Rachel', 'user_id': 2}, {'id': 7, 'text': 'I love hogs', 'user': 'Daniel', 'user_id': 3}, {'id': 8, 'text': 'Hogs are the best way to teach react', 'user': 'Daniel', 'user_id': 3}, {'id': 9, 'text': 'Programming is lyfe', 'user': 'Daniel', 'user_id': 3}]
        self.assertEqual(json_data, tweets)

    def test_tweet_by_id(self):
        response = self.app.get('/api/tweets/1')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        tweet = {'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}
        self.assertEqual(json_data, tweet)

    def test_users_id_tweets(self):
        response = self.app.get('/api/users/1/tweets')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        user1_tweets = {'id': 1, 'tweets': [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}], 'username': 'Jeff'}
        self.assertEqual(json_data, user1_tweets)

    def test_users_name_tweets(self):
        response = self.app.get('/api/users/jeff/tweets')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        user1_tweets = [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}]
        self.assertEqual(json_data, user1_tweets)

    def test_tweets_by_id_user(self):
        response = self.app.get('/api/tweets/1/user')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        json_data = json.loads(raw)
        user = {'id': 1, 'tweets': [{'id': 1, 'text': 'Data Science is awesome', 'user': 'Jeff', 'user_id': 1}, {'id': 2, 'text': 'Python is pretty neat', 'user': 'Jeff', 'user_id': 1}, {'id': 3, 'text': "Wishing I was chillin' in mexico rn", 'user': 'Jeff', 'user_id': 1}], 'username': 'Jeff'}
        self.assertEqual(json_data, user)


if __name__ == '__main__':
    unittest.main()
