import unittest
import os
from helium import *
import time


class MainpageTest(unittest.TestCase):
    start_firefox('localhost:8000/')
    click(Button("Timeline"))    
    time.sleep(2)
    get_driver().save_screenshot(os.path.join(os.getcwd(), 'tests-ui', 'screenshots', 'Timeline.png'))
    time.sleep(2)
    if Text("Timeline Visualisation").exists():
        click(Link("The First Article-2010-10-10"))
    time.sleep(2)
    click(Button("Timeline"))
    time.sleep(2)
    kill_browser()