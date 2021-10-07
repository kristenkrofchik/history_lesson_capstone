import os
from unittest import TestCase

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False]

os.environ['DATABASE_URL'] = "postgresql:///history-lesson-test"

from app import app

db.create_all()

class HistoryLessonAppTestCase(TestCase):
    """Test routes"""
    def test_main_page_redirection(self):
       with app.test_client() as client:
           resp = client.get('/')

           self.assertEqual(resp.status_code, 302)
           self.assertEqual(resp.location, 'http://localhost/register')
    
    def test_home_redirect_followed(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Register</h1>', html)
            
    

