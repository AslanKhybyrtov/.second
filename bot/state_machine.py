from config import *

class Bot_states(StatesGroup):

    
    START_STATE=State()

    LOGIN =State()
    PASSWORD = State()
    REGIST_LOGIN=State()
    REGIST_PASSWORD=State()
    AUTORISATION=State()
