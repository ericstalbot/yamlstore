
 
import os
from yamlstore import app
from yamlstore.db import db
from yamlstore.auth import user_datastore
import unittest
import flask_security

class Test(unittest.TestCase):

    def setUp(self):
        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' #in memory
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testing'
        app.config['DEBUG'] = True
        
        
        
        self.app = app.test_client()
        
        db.create_all()
        
        self.user = user_datastore.create_user(email='test@test.com', password='password')
        
        db.session.commit()
        
        
        with app.test_request_context():
            flask_security.utils.login_user(self.user)
        
        

    def tearDown(self):
        with app.test_request_context():
            flask_security.utils.logout_user()
        
    def test1(self):
        r = self.app.get('/')
        print r.data
        assert 'hello' in r.data
        

if __name__ == '__main__':
    unittest.main()
    