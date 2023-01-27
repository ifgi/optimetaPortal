import unittest
import os
from helium import start_firefox,get_driver,click,Text,Button,kill_browser

class LoginconfirmationTest(unittest.TestCase):
    
    start_firefox('localhost:8000/loginconfirm/')  
    get_driver().save_screenshot(os.path.join(os.getcwd(), 'tests-ui', 'screenshots', 'UserMenu.png'))
    if Text("Welcome to Optimeta!").exists():
        click(Button("×"))
    kill_browser()
    