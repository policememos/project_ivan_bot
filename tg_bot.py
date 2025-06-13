import asyncio
import sys
from os import getenv
import logging

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения,
    handlers=[
        logging.FileHandler("tg_bot_users.log", encoding="utf-8"),  # Важно: encoding="utf-8"
        logging.StreamHandler()  # Вывод в консоль
    ]
)
logger = logging.getLogger('TG_BOT')

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")


# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    user = message.from_user  # Получаем данные пользователя

    first_name = user.first_name  # Имя (если есть)
    last_name = user.last_name  # Фамилия (если есть)
    username = user.username
    logger.info("start<- %s, %s, %s | Имя, Фамилия, Никнейм", first_name, last_name, username)

    await message.answer(f"Привет! Ваш chat id: {html.bold(message.chat.id)}")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())