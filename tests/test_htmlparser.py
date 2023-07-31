from bs4 import BeautifulSoup
from django.test import TestCase
from publications.tasks import parse_html


class SimpleTest(TestCase):
          
    def test_parse_html(self):
        html_doc = """
        <meta name="DC.Coverage" xml:lang="en" content="Earth, Europe, Republic of France, Pays de la Loire"/>
        <meta name="DC.SpatialCoverage" scheme="GeoJSON" content="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;properties&quot;:{&quot;provenance&quot;:{&quot;description&quot;:&quot;geometric shape created by user (drawing)&quot;,&quot;id&quot;:11}},&quot;geometry&quot;:{&quot;type&quot;:&quot;LineString&quot;,&quot;coordinates&quot;:[[0.19995063543319705,47.83528342275264],[-0.6350103020668031,47.80577611936812]]}}],&quot;administrativeUnits&quot;:[{&quot;name&quot;:&quot;Earth&quot;,&quot;geonameId&quot;:6295630,&quot;bbox&quot;:&quot;not available&quot;,&quot;administrativeUnitSuborder&quot;:[&quot;Earth&quot;],&quot;provenance&quot;:{&quot;description&quot;:&quot;administrative unit created by user (acceppting the suggestion of the geonames API , which was created on basis of a geometric shape input)&quot;,&quot;id&quot;:23}},{&quot;name&quot;:&quot;Europe&quot;,&quot;geonameId&quot;:6255148,&quot;bbox&quot;:{&quot;east&quot;:41.73303985595703,&quot;south&quot;:27.6377894797159,&quot;north&quot;:80.76416015625,&quot;west&quot;:-24.532675386662543},&quot;administrativeUnitSuborder&quot;:[&quot;Earth&quot;,&quot;Europe&quot;],&quot;provenance&quot;:{&quot;description&quot;:&quot;administrative unit created by user (acceppting the suggestion of the geonames API , which was created on basis of a geometric shape input)&quot;,&quot;id&quot;:23}},{&quot;name&quot;:&quot;Republic of France&quot;,&quot;geonameId&quot;:3017382,&quot;bbox&quot;:{&quot;east&quot;:9.56009360694225,&quot;south&quot;:41.3335556861592,&quot;north&quot;:51.0889894407743,&quot;west&quot;:-5.14127657354623},&quot;administrativeUnitSuborder&quot;:[&quot;Earth&quot;,&quot;Europe&quot;,&quot;Republic of France&quot;],&quot;provenance&quot;:{&quot;description&quot;:&quot;administrative unit created by user (acceppting the suggestion of the geonames API , which was created on basis of a geometric shape input)&quot;,&quot;id&quot;:23}},{&quot;name&quot;:&quot;Pays de la Loire&quot;,&quot;geonameId&quot;:2988289,&quot;bbox&quot;:{&quot;east&quot;:0.916650657911376,&quot;south&quot;:46.2666616230696,&quot;north&quot;:48.5679940644253,&quot;west&quot;:-2.62573947290169},&quot;administrativeUnitSuborder&quot;:[&quot;Earth&quot;,&quot;Europe&quot;,&quot;Republic of France&quot;,&quot;Pays de la Loire&quot;],&quot;provenance&quot;:{&quot;description&quot;:&quot;administrative unit created by user (acceppting the suggestion of the geonames API , which was created on basis of a geometric shape input)&quot;,&quot;id&quot;:23}}],&quot;temporalProperties&quot;:{&quot;unixDateRange&quot;:&quot;[1654041600000,1654214399000]&quot;,&quot;provenance&quot;:{&quot;description&quot;:&quot;temporal properties created by user&quot;,&quot;id&quot;:31}}}" />
        <meta name="geo.placename" content="Pays de la Loire" />
        <meta name="DC.box" content="name=Pays de la Loire; northlimit=48.567994064425; southlimit=46.26666162307; westlimit=-2.6257394729017; eastlimit=0.91665065791138; projection=EPSG3857" />
        <meta name="ISO 19139" content="<gmd:EX_GeographicBoundingBox><gmd:westBoundLongitude><gco:Decimal>-2.6257394729017</gco:Decimal></gmd:westBoundLongitude><gmd:eastBoundLongitude><gco:Decimal>0.91665065791138</gco:Decimal></gmd:eastBoundLongitude><gmd:southBoundLatitude><gco:Decimal>46.26666162307</gco:Decimal></gmd:southBoundLatitude><gmd:northBoundLatitude><gco:Decimal>48.567994064425</gco:Decimal></gmd:northBoundLatitude></gmd:EX_GeographicBoundingBox>" />
        """
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        self.json_object = parse_html(self.soup)
        self.assertEqual(self.json_object['type'], 'FeatureCollection')
        self.assertEqual(self.json_object["features"][0]["geometry"]["type"], 'LineString')
        self.assertIsNotNone(self.json_object)
    
    def test_parse_html_without_spatial_data(self):
        html_doc = """
        <meta name="DC.Identifier.pageNumber" content="1-2"/>
        <meta name="DC.Identifier.URI" content="https://josis.org/index.php/josis/article/view/1"/>
        <meta name="DC.Language" scheme="ISO639-1" content="en"/>
        <meta name="DC.Rights" content="Copyright (c) 2010 Journal of Spatial Information Science"/>
        """

        self.soup = BeautifulSoup(html_doc, 'html.parser')
        self.json_object = parse_html(self.soup)
        self.assertEqual(len(self.json_object),0)