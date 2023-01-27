import requests
import json
url = 'https://api.jsonbin.io/v3/b/63d42f19ace6f33a22c94f26/latest'
headers = {
  'X-Master-Key': '$2b$10$TWMYDoj4.wAMi7q.1XwiieeX.NwIRU68gFC9.ILWiivN2vsPtB0DO',
}

req = requests.get(url,  json=None, headers=headers).json()
y = json.dumps(req)
x = json.loads(y)

number_of_group = x['record']['group']


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
