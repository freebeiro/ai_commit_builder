import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
           self.app = app.test_client()
           self.app.testing = True

           def test_home_success(self):
               response = self.app.get('/')
               self.assertEqual(response.status_code, 200)
               self.assertEqual(response.data.decode(), "Hello, World!")
               
           def test_error(self):
               response = self.app.get('/error')
               self.assertEqual(response.status_code, 400)
               self.assertIn("This is an error message", response.get_json().get("error"))

if __name__ == "__main__":
    unittest.main()
