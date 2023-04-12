from config import *
# from state_machine import *
# from functions import *

HELP_COMMAND = '''
/help - список команд
/start - начать работу'''



@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND) 

@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.answer(text="Welcome") 
    await message.delete()

    with open("data_out/users.txt") as users_id:
        reading_id=users_id.read().split(',')
        if user_id in reading_id:
            return False
        else:
            users_id.write(f"{users_id},")
            return True
        
    user_id = message.from_user.id
    if await append_user_in_data(user_id):
        await message.answer(text= "Пользователь Добавлен")
    else:
        await message.answer(text= "Пользователь уже авторизован")
    
    


