#!/usr/bin/env python
# -----------------------------------------------------------------------------
# moonlightd [moonlightd]
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------

import logging
import os
import re

import requests
from telegram import ForceReply, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

COMMAND_HELP = 'help'
COMMAND_WEATHER = 'weather'

COMMAND_DESCS = {
    COMMAND_WEATHER: ('show current weather', ' [LOCATION]\n  show current weather in LOCATION [default: MSK].'),
}


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    logging.info(f'Command from {update.effective_user.username}: {update.message.text})')
    location = 'MSK'
    if len(argv := re.split(r'\s', update.message.text)) == 2:
        location = argv[1]
    try:
        response = requests.get(f'http://wttr.in/{location}?format=%l:;%c%t;%w&M', headers={'User-Agent': 'curl'})
        if response.status_code == 200:
            msg = '\n'.join(response.text.split(';'))
            logging.info(f'Successfully retrieved weather')
        else:
            msg = f"Failed to retrieve weather (HTTP {response.status_code})"
            logging.info(f'Failed to retrieve weather: HTTP {response.status_code})')
    except Exception as e:
        msg = f"Failed to retrieve weather ({e.__class__.__qualname__})"
        logging.info(f'Failed to retrieve weather: {e})')
    await update.message.reply_html(msg)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_help(update)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await reply_help(update)

async def reply_help(update: Update) -> None:
    command_name = None
    command_desc = None
    if len(argv := re.split(r'\s', update.message.text)) == 2:
        command_name = argv[1].lstrip('/')
        command_desc = COMMAND_DESCS.get(command_name, [None, None])[1]

    if not command_desc:
        msg = '<b>COMMANDS</b>\n\n'
        msg += '\n'.join({f'/{k} -- {v[0]}' for k, v in COMMAND_DESCS.items()})
        msg += '\n\nUse /help COMMAND_NAME for the details'
    else:
        msg = f'<b>USAGE:</b>  /{command_name} {command_desc}'

    await update.message.reply_html(msg)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logging.info(f'Message in {update.effective_chat.username} from {update.effective_user.username}: {update.message.text})')
    except Exception as e:
        logging.error(f'Logging failed: {e}')


def main() -> None:
    application = Application.builder().token(os.getenv('TELEGRAM_API_KEY')).build()
    application.add_handler(CommandHandler(COMMAND_WEATHER, weather_command))
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler(COMMAND_HELP, help_command))
    application.add_handler(MessageHandler(~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    main()
