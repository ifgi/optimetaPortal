import os
import unittest
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optimetaPortal.settings')

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_root(self):
        response = self.client.get('/publications/api/publications/')

        self.assertEqual(response.status_code, 200)
        #self.assertEqual(len(response.context['publications']), 5)

        self.assertEqual(response.get('Content-Type'), 'application/json')

        body = response.json()
        self.assertEqual(body['type'], 'FeatureCollection')

        #body["properties"]["name"] == "Example"
