import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import time
from selenium.webdriver.common.by import By
import collections
import csv
from log import *
import os
from threading import Thread
from config.con_ import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ParseResult = collections.namedtuple(
    'ParseResult', ('text', 'time', 'url'),
)


class lenta_parser(Thread):
   
    def  __init__(self) -> None:
        Thread.__init__(self)
        options = webdriver.ChromeOptions()
        options.add_argument('window-size = 1600,900')
        #options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=options)
        self.database = []
        self.result =[]
        self.wait= WebDriverWait(self.driver,timeout=15)

    def load_page(self):#, page: int = None):
        url = "https://lenta.ru/"
        self.driver.get(url=url)

    def authorization(self):
        self.driver.find_element(By.XPATH, "//div[3]/div[3]/div[2]/header/div[3]/div[2]/div/button").click()
        time.sleep(5)
        #WebDriverWait(self.driver,timeout=15).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]')))
        email_input = self.driver.find_element(By.XPATH, '//*[@id="login"]')
        time.sleep(5)
        email_input.send_keys(config['Lenta']['login'])
        time.sleep(5)
        password_input = self.driver.find_element(By.XPATH, '//input[@type="password"]')
        time.sleep(5)
        password_input.send_keys(config['Lenta']['password'])
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//div/div/div[2]/div/div/div/div[1]/form/button").click()
        time.sleep(5)

    def parse_page(self):
        news = self.driver.find_elements(By.XPATH,"//section[1]/div[1]/div[1]/div/a") 
        news_link = list(map(lambda x: x.get_attribute("href"),news))
        for link_news in news_link:
            self.driver.get(link_news)
            self.parse_block()
        print(self.result)


    
    def parse_block(self):
        #logging.info(block)
        #logging.info('=' * 100)
        try:
            url = self.driver.current_url
            print(url)
            time_block = self.driver.find_element(By.XPATH, "//div[3]/div[1]/div[1]/div/div/div[1]/a[1]").text
            title = self.driver.find_element(By.XPATH, "//div/div/div/div/h1/span").text
            text = self.driver.find_elements(By.XPATH, "//div/div/div/div/div/p")
            # for texts in text:
            #     texts= texts.text
            #     main_text += texts
            main_text = ''.join(list(map(lambda a: a.text, text)))


            
            self.result.append(
                (url,
                time_block,
                title, 
                main_text))
            
        except Exception as e:
            logging.error(traceback.format_exc())

    def save_result(self):
        path = 'qwerty.csv'   
        if os.path.exists(path):
            with open(path, 'a', encoding='utf-8') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                for data in self.result:
                    writer.writerow(data)
        else:
             with open(path, 'w', encoding='utf-8') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                for data in self.result:
                    writer.writerow(data)

    def run(self):
        self.load_page()
        self.authorization()
        # self.parse_page()
        # self.save_result()
        self.driver.quit()

if __name__ == "__main__":
    parser = lenta_parser()
    parser.run()

