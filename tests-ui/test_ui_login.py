import unittest
from helium import *

class SimpleTest(unittest.TestCase):

    def test_login_page(self):
        start_firefox('localhost:8000/publications/login/')

        write('optimeta@dev.dev', into='email')

        get_driver().save_screenshot(r'tests-ui/screenshots/login-email.png')

        click("Send")

        wait_until(lambda: Text('Success!').exists())

        self.assertIn('Check your email', S('body').web_element.text)

        get_driver().save_screenshot(r'tests-ui/screenshots/login-success.png')

        kill_browser()
