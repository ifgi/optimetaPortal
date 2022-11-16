import unittest
from django.test import SimpleTestCase
from django.urls import reverse  
from helium import *
import os

class PrivacypageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/privacy/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("publications:privacy"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("publications:privacy"))
        self.assertTemplateUsed(response, "privacy.html")

    def test_template_content(self):
        response = self.client.get(reverse("publications:privacy"))
        self.assertContains(response, "Privacy Policy")
        
class SimpleTest(unittest.TestCase):
    
    start_firefox('localhost:8000/')
    click("privacy")    
    get_driver().save_screenshot(os.path.join(os.getcwd(), 'tests-ui/screenshots/privacy.png'))
    kill_browser()