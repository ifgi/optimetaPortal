from datetime import date
import os
from django.test import Client, TestCase
from publications.models import Publication
from django.contrib.gis.geos import Point, MultiPoint, LineString, Polygon, GeometryCollection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optimetaPortal.settings')

class SimpleTest(TestCase):
    
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        pub1 = Publication.objects.create(
            title="Publication One",
            abstract="This is a first publication. It's good.",
            publicationDate=date(2022, 10, 10),
            geometry=GeometryCollection(
                Point(0, 0),
                MultiPoint(Point(10, 10), Point(20, 20)),
                LineString([Point(11, 12), Point(31, 32)]),
                Polygon( ((52, 8), (55, 8), (55, 9), (52, 8)) ))
        )
        pub1.save()
        pub2 = Publication.objects.create(
            title="Publication Two",
            abstract="Seconds are better than firsts.",
            publicationDate=date(2022, 10, 24),
            geometry=GeometryCollection(Point(1, 1))
        )
        pub2.save()

    @classmethod
    def clearTestData(cls):
        Publication.objects.all().delete()

    def test_api_redirect(self):
        response = self.client.get('/api')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/v1/')

        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/v1/')

    def test_api_root(self):
        response = self.client.get('/api/v1/publications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

        results = response.json()['results']

        self.assertEqual(results['type'], 'FeatureCollection')
        self.assertEqual(len(results['features']), 2)

        self.assertEqual(len(results['features'][0]['properties']), 9)
        self.assertEqual(results['features'][0]['properties']['title'], 'Publication One')
        self.assertEqual(results['features'][0]['properties']['publicationDate'], '2022-10-10')

    def test_api_first_publication(self):
        all = self.client.get('/api/v1/publications/').json()
        id = all['results']['features'][0]['id']
        response = self.client.get('/api/v1/publications/%s.json' % id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

        body = response.json()
        self.assertEqual(body['type'], 'Feature')
        self.assertEqual(body['geometry']['type'], 'GeometryCollection')

        self.assertEqual(len(body['geometry']['geometries']), 4)
        self.assertEqual(body['geometry']['geometries'][2]['type'], 'LineString')
        self.assertEqual(body['geometry']['geometries'][2]['coordinates'][0], [11.0, 12.0])
        self.assertEqual(body['properties']['title'], 'Publication One')
        self.assertEqual(body['properties']['publicationDate'], '2022-10-10')

    def test_api_publication_99_missing(self):
        response = self.client.get('/api/v1/publications/99.json')
        self.assertEqual(response.status_code, 404)