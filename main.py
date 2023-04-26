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

    executor.start_polling(dp)

    event = asyncio.get_event_loop()
    tasks = [event.create_task(w()), event.create_task(l())]
    wait_tasks = asyncio.wait(tasks)
    event.run_until_complete(wait_tasks)
    event.close()

    pass