import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Instagram', response.data)

    def test_generate_post(self):
        response = self.client.post('/generate_post', json={'prompt': 'A beautiful sunset'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()