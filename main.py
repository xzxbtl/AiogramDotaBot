import os
import importlib
from aiogram import Bot, Dispatcher,Router
import asyncio
import logging
from env.config_reader import config
from datetime import datetime

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
router = Router()

current_dir = os.path.dirname(__file__)

# Импорт всех handlerov из handlers
for root, dirs, files in os.walk(os.path.join(current_dir, "handlers")):
    for handler_file in files:
        if handler_file.endswith(".py") and handler_file != "__init__.py":
            handler_module_name = f"{root.replace(os.sep, '.')[len(current_dir)+1:]}.{handler_file[:-3]}"
            handler_module = importlib.import_module(handler_module_name)
            if hasattr(handler_module, 'register_handlers'):
                handler_module.register_handlers(dp)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
