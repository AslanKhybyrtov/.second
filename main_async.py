from tools import *
from config import *
import asyncio
from tools.bot.pars_2 import *

if __name__ == "__main__":
    a = Twin_parser()
    a.start()
    executor.start_polling(dp)

    pass