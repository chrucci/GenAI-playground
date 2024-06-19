import unittest
from app.app import app


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        app.testing = True
        self.client = app.test_client()

    def test_hello_name_route(self):
        # Test the /hello/<name> route with a sample name
        name = "Chris"
        response = self.client.get(f"/hello/{name}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytearray(f"Hello, {name}!", "utf-8"), response.data)

    def test_bad_route(self):
        # Test the /bad route with a sample name
        response = self.client.get("/bad")
        self.assertEqual(response.status_code, 404)

    # Additional tests can be added here, such as testing for incorrect routes or methods


if __name__ == "__main__":
    unittest.main()
