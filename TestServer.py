import unittest
from flaskHttpServer import app, admins, subscribers, admin_message
from bcrypt import hashpw, gensalt, checkpw


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

        # ✅ Use a fixed salt for test reproducibility
        global salt
        salt = gensalt()

        # Reset global state before each test
        admins.clear()
        admins.update({"admin": hashpw("password".encode("utf-8"), salt)})
        subscribers.clear()
        subscribers.update({"test": hashpw("123".encode("utf-8"), salt)})

        global admin_message
        admin_message = None

    # ---------- LOGIN TESTS ----------
    def test_login_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_valid_subscriber_login(self):
        # ✅ Send plain password so bcrypt.checkpw() works
        response = self.app.post('/', data={
            'username': 'test',
            'password': '123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, test!', response.data)

    def test_invalid_login(self):
        response = self.app.post('/', data={
            'username': 'wrong',
            'password': 'nope'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid username or password', response.data)

    def test_wrong_password(self):
        response = self.app.post('/', data={
            'username': 'test',
            'password': 'wrong'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Incorrect password', response.data)

    # ---------- SIGNUP TESTS ----------
    def test_signup_new_user(self):
        response = self.app.post('/sign_up', data={
            'username': 'newuser',
            'password': 'pass'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, newuser!', response.data)
        self.assertIn('newuser', subscribers)

    def test_signup_missing_fields(self):
        response = self.app.post('/sign_up', data={
            'username': '',
            'password': ''
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Please enter both username and password', response.data)

    def test_signup_existing_user(self):
        response = self.app.post('/sign_up', data={
            'username': 'test',
            'password': 'another'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Username already exists', response.data)

    # ---------- ADMIN TESTS ----------
    def test_admin_login(self):
        response = self.app.post('/', data={
            'username': 'admin',
            'password': 'password'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Admin admin!', response.data)

    def test_admin_post_message(self):
        response = self.app.post('/admin/admin/post_message', data={
            'message': 'Hello Users!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Message posted', response.data)

    def test_admin_view_subscribers(self):
        response = self.app.get('/admin/admin/subscribers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Current Subscribers', response.data)
        self.assertIn(b'test', response.data)

    def test_admin_remove_user(self):
        response = self.app.get('/admin/admin/remove_user/test', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'removed successfully', response.data)
        self.assertNotIn('test', subscribers)
    
    def test_admin_remove_nonexistent_user(self):
        response = self.app.get('/admin/admin/remove_user/nonexistent', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'not found', response.data)
        
    # ---------- USER ACTIONS ----------
    def test_user_change_password(self):
        response = self.app.post('/welcome/test', data={
            'password': '123',
            'new_password': 'newpass',
            'confirm_password': 'newpass'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password updated successfully', response.data)

        # ✅ Verify the new password works using bcrypt.checkpw
        new_hashed_pw = subscribers['test']
        self.assertTrue(checkpw('newpass'.encode('utf-8'), new_hashed_pw))

    def test_user_unsubscribe(self):
        response = self.app.post('/welcome/test', data={
            'password': '123',
            'confirm_unsubscribe': 'yes'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('test', subscribers)


if __name__ == '__main__':
    unittest.main()
