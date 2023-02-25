from log import *
from config.con_ import *

ParseResult = collections.namedtuple(
    'ParseResult', ('text', 'time', 'url'),
)


class ria_parser(Thread):

    def  __init__(self, id) -> None:
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
        url = "https://ria.ru/"
        self.driver.get(url=url)

    def authorization(self):
        self.driver.find_element(By.XPATH, "//div[2]/div[1]/div[1]/div[3]/a[1]").click()
        try:
            time.sleep(3)
            email_input = self.driver.find_element(By.XPATH, '//*[@id="modalAuthEmailField"]')
            email_input.send_keys(config['Ria']['login'])
            password_input = self.driver.find_element(By.XPATH, '//*[@id="modalAuthPassword"]')
            password_input.send_keys(config['Ria']['password'])
            WebDriverWait(self.driver,timeout=15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modalAuthSubmit"]/button')))
            self.driver.find_element(By.XPATH, '//*[@id="modalAuthSubmit"]/button').click()
            time.sleep(3)
        except exceptions.NoSuchElementException:
            print("Уже авторизован")
            self.driver.get("https://ria.ru/")
        except:
            logging.error(traceback.format_exc())


    

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
        self.authorization()
        # self.parse_page()
        # self.save_result()
        self.driver.quit()

if __name__ == "__main__":
    parser = ria_parser(57084048)
    parser.run()