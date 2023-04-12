from config import *

async def append_user_in_data(user_id):
    with open("data_out/users.txt") as users_id:
        reading_id=users_id.read().split(',')
        if user_id in reading_id:
            return False
        else:
            users_id.write(f"{users_id},")
            return True