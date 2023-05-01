from config import *
from bot.state_machine import Bot_states
from bot.ria_async import *
from .lenta_async import *
# from functions import *


HELP_COMMAND = '''
/help - список команд
/start - начать работу
/ria - парсинг риа
/lenta - парсинг лента
'''
w = async_ria_parser(57084048)
l = async_lenta_parser(57084987)


@dp.message_handler(state="*",commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND) 

@dp.message_handler(state="*",commands=['start'])
async def autorisation_id(message: types.Message):
    user_id = message.from_user.id
    with open("data_out/users.json","r") as fl:
        json_data=json.load(fl)
        users_id=list(map(lambda data: data.get("id"),json_data["users"]))
    if user_id in users_id:
        await message.answer(text="Welcome, input next command")
    else:
        # json_data["users"].append({"id":user_id,"state":"AUTORISATION"})
        # with open("data_out/users.json", 'w') as fl:
        #     json.dump(json_data,fl)
        #     await message.answer(text="Вы зарегестрированы. Введите следующую команду")



@dp.message_handler(commands=["ria"])
async def ria_pars(message: types.Message):
    await message.answer(text="Парсинг начался")

    await w.run()
    await message.answer(text="Парсинг завершен")


@dp.message_handler(commands=["lenta"])
async def lenta_pars(message: types.Message):
    await message.answer(text="Парсинг начался")
    
    await l.run()
    await message.answer(text="Парсинг завершен")


async def auto():
    with open("data_out/users.json","r") as fl:
        starter_data = json.load(fl)
    users = starter_data.get("users")
    for i in users:
        # bot.send_message(chat_id=i.get("id"),text)
        s = dp.current_state(chat=i.get("id"))
        match i.get("state"):
            case "AUTORISATION":
                s.set_state(Bot_states.AUTORISATION)
            
        print(i.get("id"), i.get("state"))






    


