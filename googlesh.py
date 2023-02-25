# Подключаем библиотеки
import httplib2 
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials	

class google_sheet():

    def __init__(self) -> None:
        
        self.__CREDENTIALS_FILE = 'chrome-axe-377911-17d1def18bbd.json'  # Имя файла с закрытым ключом

        # Читаем ключи из файла
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_name(self.__CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

        httpAuth = self.__credentials.authorize(httplib2.Http()) # Авторизуемся в системе
        self.__service = discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

    def _create_table(self):
        spreadsheet = self.__service.spreadsheets().create(body = {
                'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
                'sheets': [{'properties': {'sheetType': 'GRID',
                                        'sheetId': 0,
                                        'title': 'Лист номер один',
                                        'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
            }).execute()
        spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
        print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
    def __create_list(self, spreadsheetId):
    
        # Добавление листа
        results = self.__service.spreadsheets().batchUpdate(
            spreadsheetId = spreadsheetId,
            body = 
        {
        "requests": [
            {
            "addSheet": {
                "properties": {
                "title": "Еще один лист",
                "gridProperties": {
                    "rowCount": 20,
                    "columnCount": 12
                }
                }
            }
            }
        ]
        }).execute()
        print('создание страниц')

    def lists_(self, spreadsheetId):
        # Получаем список листов, их Id и название
        spreadsheet = self.__service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
        sheetList = spreadsheet.get('sheets')
        for sheet in sheetList:
            print(sheet['properties']['sheetId'], sheet['properties']['title'])
            
        sheetId = sheetList[0]['properties']['sheetId']

        print('Мы будем использовать лист с Id = ', sheetId)

        results = self.__service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "Лист номер один!B2:D5",
            "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
            "values": [
                        ["Ячейка B2", "Ячейка C2", "Ячейка D2"], # Заполняем первую строку
                        ['25', "=6*6", "=sin(3,14/2)"]  # Заполняем вторую строку
                    ]}
        ]
        }).execute()
##### =================>Это отдельная функция
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

    def cell(self,spreadsheetId,sheetId):
        # Объединяем ячейки A2:D1
    ##### =================>Это отдельная функция
        results = self.__service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheetId,
        body = {
            "requests": [
                {'mergeCells': {'range': {'sheetId': sheetId,
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 1,
                            'endColumnIndex': 4},
                    'mergeType': 'MERGE_ALL'}}
            ]
        }).execute()

    def header(self,spreadsheetId,sheetId):
    ##### =================>Это отдельная функция
    # Добавляем заголовок таблицы
        results = self.__service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED",
    # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "Лист номер один!B1",
            "majorDimension": "ROWS", # Сначала заполнять строки, затем столбцы
            "values": [["Заголовок таблицы" ] 
                    ]}
        ]
        }).execute()

    def format_cell(self,spreadsheetId,sheetId):
    ##### =================>Это отдельная функция
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

    def result_1list(self,spreadsheetId):
    ##### =================>Это отдельная функция
        ranges = ["Лист номер один!C2:C2"] # 
            
        results = self.__service.spreadsheets().get(spreadsheetId = spreadsheetId, 
                                        ranges = ranges, includeGridData = True).execute()
        print('Основные данные')
        print(results['properties'])
        print('\nЗначения и раскраска')
        print(results['sheets'][0]['data'][0]['rowData'] )
        print('\nВысота ячейки')
        print(results['sheets'][0]['data'][0]['rowMetadata'])
        print('\nШирина ячейки')
        print(results['sheets'][0]['data'][0]['columnMetadata'])

    def result_list2(self,spreadsheetId):
    ##### =================>Это отдельная функция
        ranges = ["Лист номер один!A2:F8"] # 
                
        results = self.__service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                ranges = ranges, 
                                                valueRenderOption = 'FORMATTED_VALUE',  
                                                dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
        print(sheet_values)


