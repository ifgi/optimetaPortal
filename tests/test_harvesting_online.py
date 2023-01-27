import unittest
from publications.tasks import harvest_oai_endpoint
from django.test import TestCase,Client
import os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optimetaPortal.settings')

class SimpleTest(TestCase):

    def setUp(self):
        self.client = Client()
    
    @unittest.skipIf(settings.TEST_HARVESTING_ONLINE != True, "going online for harvesting is not activated")
    def test_optimeta_demo_server_harvesting(self):
        url = "https://service.tib.eu/optimeta/index.php/optimeta/oai/?verb=ListRecords&metadataPrefix=oai_dc"
        harvest_oai_endpoint(url)
    
    @unittest.skipIf(settings.TEST_HARVESTING_ONLINE != True, "going online for harvesting is not activated")
    def test_api_root(self):
        response = self.client.get('/api/v1/publications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

        body = response.json()
        self.assertEqual(body['type'], 'FeatureCollection')
        self.assertEqual(len(body['features']), 2)
        self.assertEqual(len(body['features'][0]['properties']), 33)
        self.assertEqual(body['features'][0]['properties']['title'], 'Using textual volunteered geographic information to model nature-based activities: A case study from Aotearoa New Zealand')
        self.assertEqual(body['features'][0]['properties']['publicationDate'], '2022-07-21')