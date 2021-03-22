from selenium import webdriver
from pynput.keyboard import Key ,Controller
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

keyboard = Controller()
chromeDriver = os.path.join("chromedriver.exe")
driver = webdriver.Chrome(chromeDriver)
driver.get('https://stackoverflow.com/questions/tagged/python')