from tools import *
from config import *
from bot import *




if __name__ == "__main__":
    # a = lenta_parser()
    # b = ria_parser()
    # a.start()
    # b.start()
    # w = async_ria_parser(57084048)
    # l = async_lenta_parser(57084987)

    
    
    event = asyncio.get_event_loop()
    event.run_until_complete(auto())
    # event.close()

    executor.start_polling(dp,loop=event)