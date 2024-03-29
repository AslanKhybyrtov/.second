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
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import aiogram
from aiogram import Bot, Dispatcher, executor, types
import string
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import json

config = configparser.ConfigParser()
config.read('config/setting.ini')

def config_update():
    with open(r'settings/settings.ini', 'w') as f:
        config.write(f)
    config.read(r'settings/settings.ini')


bot = Bot(config["Telegramm_bot"]["Token_Aiogram"])
dp = Dispatcher(bot, storage=MemoryStorage())
