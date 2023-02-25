import configparser
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import time
from selenium.webdriver.common.by import By
import collections
import csv
import os
from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
from selenium.common import exceptions


config = configparser.ConfigParser()
config.read('config/setting.ini')

def config_update():
    with open(r'settings/settings.ini', 'w') as f:
        config.write(f)
    config.read(r'settings/settings.ini')