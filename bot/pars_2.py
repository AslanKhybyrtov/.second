# from log import *
from config import *
# from googlesh import *
from config.log import *
import asyncio
ParseResult = collections.namedtuple(
    'ParseResult', ('text', 'time', 'url'),
)


class Twin_parser(Thread):

    
    async def  __init__(self, id) -> None:
        self.q = google_sheet()
        self.database = []
        self.result =[]
        self.browsers_total(id)

    async def browsers_total(self, id, invisable = False):
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

    async def ria_load_page(self):#, page: int = None):
        url = "https://ria.ru/"
        self.driver.get(url=url)

    async def lenta_load_page(self):#, page: int = None):
        url = "https://lenta.ru/"
        self.driver.get(url=url)


    async def ria_authorization(self):
        try:
            self.driver.find_element(By.XPATH, "//a[@data-modal-open='authorization']").click()
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

    async def lenta_authorization(self):
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

    

    async def ria_parse_page(self):
        news1 = self.driver.find_elements(By.XPATH,"//div[@data-article-type='article']/a[1]") # первые 12 новостей 1 блок
        news_link = list(map(lambda x: x.get_attribute("href"),news1))
        for link_news in news_link:
            self.driver.get(link_news)
            self.parse_block()
        print(self.result)

    async def lenta_parse_page(self):
        news = self.driver.find_elements(By.XPATH,"//section[1]/div[1]/div[1]/div/a") 
        news_link = list(map(lambda x: x.get_attribute("href"),news))
        for link_news in news_link:
            self.driver.get(link_news)
            self.parse_block()
        print(self.result)

    
    async def ria_parse_block(self):
        try:
            url = self.driver.current_url
            print(url)
            time_block = self.driver.find_element(By.XPATH, "//div[@class='article__info-date']/a").text 
            print(time_block)
            title = self.driver.find_element(By.XPATH, "//div[@class='article__title']").text 
            print(title)
            text = self.driver.find_elements(By.XPATH, "//div[@data-type='text']")
            main_text = ''.join(list(map(lambda a: a.text, text)))
            
 
            
            self.result.append(
                [url,
                time_block,
                title, 
                main_text])
            
        except Exception as e:
            logging.info(url)
            logging.error(traceback.format_exc())

    async def lenta_parse_block(self):
        try:
            url = self.driver.current_url
            print(url)
            time_block = self.driver.find_element(By.XPATH, "//div[3]/div[1]/div[1]/div/div/div[1]/a[1]").text
            title = self.driver.find_element(By.XPATH, "//div/div/div/div/h1/span").text
            text = self.driver.find_elements(By.XPATH, "//div/div/div/div/div/p")
            main_text = ''.join(list(map(lambda a: a.text, text)))

            self.result.append(
                (url,
                time_block,
                title, 
                main_text))
            
        except Exception as e:
            logging.error(traceback.format_exc())

    async def ria_save_result(self):
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

        # сохранение в гугл таблицы
        print(self.q.append_values(config["Google"]['table_id'], "Лист1",[1,100],self.result))
        
    async def lenta_save_result(self):
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


    if __name__ == "__main__":
    
        event_l = asyncio.get_event_loop()
        tasks = [event_l.create_task(ria_load_page()), event_l.create_task(lenta_load_page())]
        wait_tasks = asyncio.wait(tasks)
        event_l.run_until_complete(wait_tasks)
        event_l.close()

        event_2 = asyncio.get_event_loop()
        tasks = [event_2.create_task(ria_authorization(57084048)), event_2.create_task(lenta_authorization(57084987))]
        wait_tasks = asyncio.wait(tasks)
        event_2.run_until_complete(wait_tasks)
        event_2.close()

        event_3 = asyncio.get_event_loop()
        tasks = [event_3.create_task(ria_parse_page()), event_3.create_task(lenta_parse_page())]
        wait_tasks = asyncio.wait(tasks)
        event_3.run_until_complete(wait_tasks)
        event_3.close()

        event_4 = asyncio.get_event_loop()
        tasks = [event_4.create_task(ria_parse_block()), event_4.create_task(lenta_parse_block())]
        wait_tasks = asyncio.wait(tasks)
        event_4.run_until_complete(wait_tasks)
        event_4.close()

        event_5 = asyncio.get_event_loop()
        tasks = [event_5.create_task(ria_save_result()), event_5.create_task(lenta_save_result())]
        wait_tasks = asyncio.wait(tasks)
        event_5.run_until_complete(wait_tasks)
        event_5.close()

    
