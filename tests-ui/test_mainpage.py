import unittest
import os
from helium import *




class MainpageTest(unittest.TestCase):
    
    start_firefox('localhost:8000/')  
    get_driver().save_screenshot(os.path.join(os.getcwd(), 'tests-ui/screenshots/UserMenu.png'))
    kill_browser()
