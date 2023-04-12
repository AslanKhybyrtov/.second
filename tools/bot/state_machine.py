from config import *

class Bot_states(Helper):
    MODE=HelperMode.snake_case
    
    START_STATE=ListItem()

    LOGIN =ListItem()
    PASSWORD = ListItem()
    REGIST_LOGIN=ListItem()
    REGIST_PASSWORD=ListItem()
    AUTORISATION=ListItem()
