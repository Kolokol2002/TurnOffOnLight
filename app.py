import argparse

parser = argparse.ArgumentParser(description='Params for group')

parser.add_argument("-g", "--group", help="Prints number your group.", default=14)

args = parser.parse_args()

number_of_group = int(args.group)


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
