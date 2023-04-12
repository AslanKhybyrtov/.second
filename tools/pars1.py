# from log import *
from config import *
# from googlesh import *
from config.log import *

ParseResult = collections.namedtuple(
    'ParseResult', ('text', 'time', 'url'),
)


class lenta_parser(Thread):
   
    def  __init__(self, id) -> None:
        self.q = google_sheet()
        Thread.__init__(self)
        self.database = []
        self.result =[]
        self.browsers_total(id)

    def browsers_total(self, id, invisable = False):
        import platform
        bit,plat = platform.architecture()
        system = (bit[:2],plat[:3].lower())
        match system:
            case "64","win":
                chrome_drive_path = Service('chromedriver-win-x64.exe')
            case "86","win":  
                chrome_drive_path = Service('chromedriver-win-x86.exe')
            case bit,"elf":
                # линукс
                chrome_drive_path = Service('./chromedriver-linux')
            case "64", "mac":
                chrome_drive_path = Service('./chromedriver-mac-x64')
                #mac
            case _:
                chrome_drive_path = Service('./chromedriver-mac-arm')
                # arm
        options = webdriver.ChromeOptions()
        reg_url = f'http://localhost:3001/v1.0/browser_profiles/{id}/start?automation=1'
        respone = requests.get(reg_url)
        respons_json = respone.json()
        PORT = str(respons_json['automation']['port'])
        options.debugger_address = '127.0.0.1:' + PORT
        options.add_argument('window-size = 1600,900')
        options.add_argument('--disable-logging')
        options.add_argument('--ignore-error')
        if invisable:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=chrome_drive_path,chrome_options=options)
        
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

        # сохранение в гугл таблицы
        print(self.q.append_values(config["Google"]['table_id'], "",[1,100],self.result))

    def run(self):
        self.load_page()
        # self.authorization()
        self.parse_page()
        self.save_result()
        self.driver.quit()

if __name__ == "__main__":
    parser = lenta_parser(57084987)
    parser.run()

