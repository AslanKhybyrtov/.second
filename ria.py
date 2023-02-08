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
ParseResult = collections.namedtuple(
    'ParseResult', ('text', 'time', 'url'),
)


class ria_parser(Thread):

    def  __init__(self) -> None:
        Thread.__init__(self)
        options = webdriver.ChromeOptions()
        options.add_argument('window-size = 1600,900')
        #options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=options)
        self.database = []
        self.result =[]

    def load_page(self):#, page: int = None):
        url = "https://ria.ru/"
        self.driver.get(url=url)

    def parse_page(self):
        news1 = self.driver.find_elements(By.XPATH,"//div[@data-article-type='article']/a[1]") # первые 12 новостей 1 блок
        news_link = list(map(lambda x: x.get_attribute("href"),news1))
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
            time_block = self.driver.find_element(By.XPATH, "//div/div[2]/div/div[4]/div[1]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/a").text # +
            print(time_block)
            title = self.driver.find_element(By.XPATH, "//div/div[2]/div/div[4]/div[1]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[2]").text # -
            print(title)
            text = self.driver.find_elements(By.XPATH, "//div[@data-type='text']") #[@class='Что то там'] +
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
            logging.info(url)
            logging.error(traceback.format_exc())

    def save_result(self):
        path = 'ria_save.csv'   
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
        self.parse_page()
        self.save_result()
        self.driver.quit()

if __name__ == "__main__":
    parser = ria_parser()
    parser.run()