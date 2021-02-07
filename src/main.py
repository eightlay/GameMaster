from telegram.ext import Updater
import logging

from settings import TG_TOKEN
import telegram_handler


def main():
    # Logging system
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, filename='bot.log')

    # Updater and dispatcher
    updater = Updater(token=TG_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Telegram handler object
    tg = telegram_handler.TG(dispatcher)

    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
