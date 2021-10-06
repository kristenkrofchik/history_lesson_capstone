from unittest import TestCase
from app import app
from flask import session

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class HistoryLessonAppTestCase(TestCase):
    """Test routes"""
    def test_main_page(self):
       with app.test_client() as client:
           resp = client.get('/')
           html = resp.get_data(as_text=True)

           self.assertEqual(resp.status_code, 200)
           self.assertIn('<h1>Register/h1', html)
    
    def test_register(self):
        with app.test_client() as client:
            resp = client.post('/register',
                                data={'username': 'test', 'password': 'testtest', 'confirm': 'testtest', 'email': 'test@test.com'})

            self.assertEqual(resp.status_code, 200)

