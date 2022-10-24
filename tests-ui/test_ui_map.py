from pprint import pprint
import unittest
from helium import *
from pprint import pprint

class SimpleTest(unittest.TestCase):

    def test_map_page(self):
        start_chrome('localhost:8000/map/', headless=True)

        get_driver().save_screenshot(r'tests-ui/screenshots/map.png')

        self.assertTrue(S('#map').exists())

        leaflet_paths = find_all(S('path.leaflet-interactive'))
        self.assertEqual(len(leaflet_paths), 2) # has two polygons on the map
        for path in leaflet_paths:
            self.assertEqual(path.web_element.get_attribute('stroke'), '#3388ff')

        click(leaflet_paths[0])

        wait_until(lambda: Text('Visit Article').exists())

        self.assertIn('title of article', S('div.leaflet-popup-content').web_element.text)

        get_driver().save_screenshot(r'tests-ui/screenshots/map_popup.png')

        # continue: click(link('Visit Article'))

        kill_browser()
