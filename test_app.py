import unittest
from app import create_app, db
from app.models import User

class BasicTests(unittest.TestCase):

    def setUp(self):
        """Set up the test environment before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # Set up the database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test the homepage"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task List', response.data)

    def test_registration(self):
        """Test user registration"""
        response = self.client.post('/register', data=dict(
            username='testuser',
            email='sakethrajaram@gmail.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)

    def test_login(self):
        """Test login functionality"""
        # First, register a new user
        self.client.post('/register', data=dict(
            username='testuser',
            email='test@test.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)

        # Then, attempt to log in
        response = self.client.post('/login', data=dict(
            email='test@test.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Task', response.data)

if __name__ == "__main__":
    unittest.main()
