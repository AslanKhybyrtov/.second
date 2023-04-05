# Подключаем библиотеки
import httplib2 
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials	
from config.con_ import *
class google_sheet():

    def __init__(self) -> None:
        self.creds = None
        self.creditions_check()
        self.__service = discovery.build('sheets', 'v4', credentials=self.creds) # Выбираем работу с таблицами и 4 версию API 

    def creditions_check(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        if os.path.exists('config/token.json'):
            self.creds = Credentials.from_authorized_user_file(
                'config/token.json', SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('config/token.json', 'w') as token:
                token.write(self.creds.to_json())

    def _create_table(self, name, title):
        
        spreadsheet = self.__service.spreadsheets().create(body = {'properties': {
                    'title': input("Entery Table name: ")
                }},fields='spreadsheetId').execute()
        spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
        print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
    
    def _create_list(self, spreadsheetId, title:str):
        ''' Добавление листа'''

        results = self.__service.spreadsheets().batchUpdate(
            spreadsheetId = spreadsheetId,
            body = {
        "requests": [
            {
            "addSheet": {
                "properties": {
                "title": f"{title}",
                }
            }
            }
        ]
        }).execute()
        print('страница создана')

    def lists_(self, spreadsheetId):
        
        # Получаем список листов, их Id и название
        spreadsheet = self.__service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
        sheetList = spreadsheet.get('sheets')
        for sheet in sheetList:
            print(sheet['properties']['sheetId'], sheet['properties']['title'])
            
        # sheetId = sheetList[0]['properties']['sheetId']

        # print('Мы будем использовать лист с Id = ', sheetId)

        # results = self.__service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        # "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        # "data": [
        #     {"range": "Лист номер один!B2:D5",
        #     "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
        #     "values": [
        #                 ["Ячейка B2", "Ячейка C2", "Ячейка D2"], # Заполняем первую строку
        #                 ['25', "=6*6", "=sin(3,14/2)"]  # Заполняем вторую строку
        #             ]}
        # ]
        # }).execute()

    def colomn(self,spreadsheetId,sheetId):
        results = self.__service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "requests": [
                    # Задать ширину столбца A: 20 пикселей
                    {
                    "updateDimensionProperties": {
                        "range": {
                        "sheetId": sheetId,
                        "dimension": "COLUMNS",  # Задаем ширину колонки
                        "startIndex": 0, # Нумерация начинается с нуля
                        "endIndex": 1 # Со столбца номер startIndex по endIndex - 1 (endIndex не входит!)
                        },
                        "properties": {
                        "pixelSize": 20 # Ширина в пикселях
                        },
                        "fields": "pixelSize" # Указываем, что нужно использовать параметр pixelSize  
                    }
                    },

                    # Задать ширину столбцов B и C: 150 пикселей
                    {
                    "updateDimensionProperties": {
                        "range": {
                        "sheetId": sheetId,
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": 3
                        },
                        "properties": {
                        "pixelSize": 150
                        },
                        "fields": "pixelSize"
                    }
                    },

                # Задать ширину столбца D: 200 пикселей
                {
                "updateDimensionProperties": {
                    "range": {
                    "sheetId": sheetId,
                    "dimension": "COLUMNS",
                    "startIndex": 3,
                    "endIndex": 4
                    },
                    "properties": {
                    "pixelSize": 200
                    },
                    "fields": "pixelSize"
                }
                }
                ]
                }).execute()
    
    def frame(self,spreadsheetId,sheetId):
##### =================>Это отдельная функция
    # Рисуем рамку
        results = self.__service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheetId,
        body = {
            "requests": [
                {'updateBorders': {'range': {'sheetId': sheetId,
                                'startRowIndex': 1,
                                'endRowIndex': 3,
                                'startColumnIndex': 1,
                                'endColumnIndex': 4},
                    'bottom': {  
                    # Задаем стиль для верхней границы
                                'style': 'SOLID', # Сплошная линия
                                'width': 1,       # Шириной 1 пиксель
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}, # Черный цвет
                    'top': { 
                    # Задаем стиль для нижней границы
                                'style': 'SOLID',
                                'width': 1,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'left': { # Задаем стиль для левой границы
                                'style': 'SOLID',
                                'width': 1,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'right': { 
                    # Задаем стиль для правой границы
                                'style': 'SOLID',
                                'width': 1,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'innerHorizontal': { 
                    # Задаем стиль для внутренних горизонтальных линий
                                'style': 'SOLID',
                                'width': 1,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'innerVertical': { 
                    # Задаем стиль для внутренних вертикальных линий
                                'style': 'SOLID',
                                'width': 1,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}
                                
                                }}
            ]
        }).execute()

    def cell(self,spreadsheetId,sheetId, ranges:tuple):
        """заголовок свойства

        Args:
            spreadsheetId (_type_): id таблица
            sheetId (_type_): id страницы
            ranges (tuple): (начало строки, конец строки, начало колонки, конец колонки)
        """
        
        results = self.__service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheetId,
        body = {
            "requests": [
                {'mergeCells': {'range': {'sheetId': sheetId,
                            'startRowIndex': ranges[0],
                            'endRowIndex': ranges[1],
                            'startColumnIndex': ranges[2],
                            'endColumnIndex': ranges[3]},
                    'mergeType': 'MERGE_ALL'}}
            ]
        }).execute()

    def headers(self,spreadsheetId,sheetId, ranges, values):
        """Заголовки

        Args:
            spreadsheetId (_type_): id таблицы
            sheetId (_type_): название страницы
            ranges (_type_): куда записывается заголовок указываем номер строки для 1 и 2 колонки
            values (_type_): сам заголовок
        """

    # Добавляем заголовок таблицы
        results = self.__service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED",
    # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": 
            {"range": f"{sheetId}!A1:W1",
            "majorDimension": "ROWS", # Сначала заполнять строки, затем столбцы
            "values":[values] 
                    }
        
        }).execute()

    def format_cell(self,spreadsheetId,sheetId):
        # Установка формата ячеек
        results = self.__service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheetId,
        body = 
    {
    "requests": [
        {
        "repeatCell": 
        {
            "cell": 
            {
            "userEnteredFormat": 
            {
                "horizontalAlignment": 'CENTER',
                "backgroundColor": {
                    "red": 0.8,
                    "green": 0.8,
                    "blue": 0.8,
                    "alpha": 1
                },
                "textFormat":
                {
                "bold": True,
                "fontSize": 14
                }
            }
            },
            "range": 
            {
            "sheetId": sheetId,
            "startRowIndex": 1,
            "endRowIndex": 2,
            "startColumnIndex": 1,
            "endColumnIndex": 4
            },
            "fields": "userEnteredFormat"
        }
        }
    ]
        }).execute()

    def result_list(self,spreadsheetId,list_name, ranges):
        """

        Args:
            spreadsheetId (_type_): id таблицы
            ranges (_type_): диапозон
            list_name (_type_): название страницы
        """
        ranges = [f"{list_name}!A{ranges[0]}:W{ranges[1]}"] 
                
        results = self.__service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                ranges = ranges, 
                                                valueRenderOption = 'FORMATTED_VALUE',  
                                                dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
        return sheet_values


    def append_values (self,spreadsheet_id, list_name, ranges, values ):
        """данные для ввода

        Args:
            spreadsheet_id (_type_): id таблицы
            range_ (_type_): куда записывается
            values (_type_): что записывается [[*value1],[value2]]
        """
        body = {'values': values}
        result = self.__service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{list_name}!A{ranges[0]}:W{ranges[1]}", 
            valueInputOption="USER_ENTERED", 
            body=body).execute()

if __name__ == "__main__":
    q = google_sheet()
    # q._create_list(config["Google"]['table_id'], "list_q")
    # q._create_table("qwerty", "list1")
    # q.lists_(config["Google"]['table_id'])
    # q.headers(config["Google"]['table_id'], "Лист1",[1,1], ["qw"])
    # print(q.result_list(config["Google"]['table_id'], "Лист1",[1,10]))
    # q.append_values(config["Google"]['table_id'], "Лист1",[1,10],[["rty"],[2345]])


