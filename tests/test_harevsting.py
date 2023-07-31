import os
from django.test import Client, TestCase
from publications.tasks import parse_xml
import httpretty

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optimetaPortal.settings')

class SimpleTest(TestCase):   
  
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        def harvest_data(url):        
            data = open(url)
            content = data.read()
            parse_xml(content)
        # adapt path to your setup
        url1 = os.path.join(os.getcwd(),'harvesting\\journal_1\\oai_dc.xml')
        url2 = os.path.join(os.getcwd(),'harvesting\\journal_1\\article_01.html')
        url3 = os.path.join(os.getcwd(),'harvesting\\journal_1\\article_02.html')
        httpretty.enable(verbose=True, allow_net_connect=False)  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET, "http://localhost:8330/index.php/opti-geo/article/view/1",
                            body= open(url2).read()
        )
        httpretty.register_uri(httpretty.GET, "http://localhost:8330/index.php/opti-geo/article/view/2",
                            body= open(url3).read()
        )
        harvest_data(url1)

    def test_api_root(self):
        response = self.client.get('/api/publications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

        body = response.json()
        self.assertEqual(body['type'], 'FeatureCollection')
        self.assertEqual(len(body['features']), 2)
        self.assertEqual(len(body['features'][0]['properties']), 9)
        self.assertEqual(body['features'][0]['properties']['title'], 'Test 1: One')
        self.assertEqual(body['features'][0]['properties']['publicationDate'], '2022-07-01')

    def test_api_publication_1(self):
        response = self.client.get('/api/publications/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

        body = response.json()
        self.assertEqual(body['type'], 'Feature')
        self.assertEqual(body['geometry']['type'], 'GeometryCollection')
        self.assertEqual(body['geometry']['geometries'][0]['type'], 'LineString')
        self.assertEqual(body['properties']['title'], 'Test 1: One')
        self.assertEqual(body['properties']['publicationDate'], '2022-07-01')
        self.assertEqual(body['properties']['timeperiod_startdate'],['2022-06-01'])
        self.assertEqual(body['properties']['url'],'http://localhost:8330/index.php/opti-geo/article/view/1')
        
    def test_api_publication_2(self):
        response = self.client.get('/api/publications/2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

        body = response.json()
        self.assertEqual(body['type'], 'Feature')
        self.assertEqual(body['geometry']['type'], 'GeometryCollection')
        self.assertEqual(body['geometry']['geometries'][0]['type'], 'Polygon')
        self.assertIsNone(body['properties']['doi'])
        self.assertEqual(body['properties']['timeperiod_enddate'],['2022-03-31'])
        self.assertEqual(body['properties']['url'],'http://localhost:8330/index.php/opti-geo/article/view/2')