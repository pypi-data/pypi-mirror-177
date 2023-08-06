#!/usr/bin/env python
# -----------------------------------------------------------------------------
# moonlightd [moonlightd]
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
import html
import logging
import os
import re
import unicodedata

import requests
from telegram import ForceReply, Update
from telegram.constants import ParseMode, MessageLimit
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

COMMAND_HELP = "help"
COMMAND_HOLMES = "holmes"
COMMAND_WATSON = "watson"
COMMAND_SUN = "sun"
COMMAND_WEATHER = "weather"

COMMAND_DESCS = {
    'codepages': {
        COMMAND_HOLMES: (
            "inspect Unicode character(s)",
            " [STRING]...\nBreak input STRINGs down to separate characters and show Unicode details for each.",
        ),
        COMMAND_WATSON: (
            "display ASCII-7 codepage",
            "\nPrint all ASCII 7-bit characters along with corresponding hexadecimal codes.",
        ),
    },
    'misc': {
        COMMAND_SUN: (
            "show sunrise/sunset times in specified location",
            ' [LOCATION]\nShow current sun times in LOCATION [default: "Moscow"]. Accepts various location formats, e.g. "MSK", "Москва".',
        ),
        COMMAND_WEATHER: (
            "show current weather in specified location",
            ' [LOCATION]\nShow current weather in LOCATION [default: "Moscow"]. Accepts various location formats, e.g. "MSK", "Москва".',
        ),
    }
}


async def holmes_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    logging.info(
        f"Command from {update.effective_user.username}: {update.message.text})"
    )
    string = "moоnlightd🌚"
    use_defualt = True
    if len(argv := re.split(r"\s", update.message.text, 1)) > 1:
        string = ''.join(argv[1:])
        use_defualt = False
    msg = ""

    max_chars = 50
    cur_char_idx = 0
    for i, c in enumerate(string):
        cur_char_idx += 1
        ucp = f"{ord(c):02X}"
        utf8 = c.encode().hex()
        char = html.escape(c.replace('\n', ' '))

        line = "\n".join(
            (
                f"<code>U+{(ucp.rjust(5))}</code> │ <code>{char}</code> │ {unicodedata.category(c)}: {unicodedata.name(c, f'(unnamed code point)')}",
                "",
            )
        )
        if (
            cur_char_idx >= max_chars
            or len(msg) + len(line) > MessageLimit.TEXT_LENGTH - 36
        ):
            msg += "...[TRUNCATED]\n"
            break
        msg += line

    if use_defualt:
        await update.message.reply_html(f'No args -- using demo input string <code>"{string}"</code>')
    await update.message.reply_html(msg)


async def watson_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_html("<pre>" + html.escape(r"""
│  U+0  \0 │ U+20 SP │ U+40  @ │ U+60  ` │
│  U+1 SOH │ U+21  ! │ U+41  A │ U+61  a │
│  U+2 STX │ U+22  " │ U+42  B │ U+62  b │
│  U+3 ETX │ U+23  # │ U+43  C │ U+63  c │
│  U+4 EOT │ U+24  $ │ U+44  D │ U+64  d │
│  U+5 ENQ │ U+25  % │ U+45  E │ U+65  e │
│  U+6 ACK │ U+26  & │ U+46  F │ U+66  f │
│  U+7  \a │ U+27  ' │ U+47  G │ U+67  g │
│  U+8  \b │ U+28  ( │ U+48  H │ U+68  h │
│  U+9  \t │ U+29  ) │ U+49  I │ U+69  i │
│  U+A  \n │ U+2A  * │ U+4A  J │ U+6A  j │
│  U+B  \v │ U+2B  + │ U+4B  K │ U+6B  k │
│  U+C  \f │ U+2C  , │ U+4C  L │ U+6C  l │
│  U+D  \r │ U+2D  - │ U+4D  M │ U+6D  m │
│  U+E  SO │ U+2E  . │ U+4E  N │ U+6E  n │
│  U+F  SI │ U+2F  / │ U+4F  O │ U+6F  o │
│ U+10 DLE │ U+30  0 │ U+50  P │ U+70  p │
│ U+11 DC1 │ U+31  1 │ U+51  Q │ U+71  q │
│ U+12 DC2 │ U+32  2 │ U+52  R │ U+72  r │
│ U+13 DC3 │ U+33  3 │ U+53  S │ U+73  s │
│ U+14 DC4 │ U+34  4 │ U+54  T │ U+74  t │
│ U+15 NAK │ U+35  5 │ U+55  U │ U+75  u │
│ U+16 SYN │ U+36  6 │ U+56  V │ U+76  v │
│ U+17 ETB │ U+37  7 │ U+57  W │ U+77  w │
│ U+18 CAN │ U+38  8 │ U+58  X │ U+78  x │
│ U+19  EM │ U+39  9 │ U+59  Y │ U+79  y │
│ U+1A SUB │ U+3A  : │ U+5A  Z │ U+7A  z │
│ U+1B ESC │ U+3B  ; │ U+5B  [ │ U+7B  { │
│ U+1C  FS │ U+3C  < │ U+5C  \ │ U+7C  | │
│ U+1D  GS │ U+3D  = │ U+5D  ] │ U+7D  } │
│ U+1E  RS │ U+3E  > │ U+5E  ^ │ U+7E  ~ │
│ U+1F  US │ U+3F  ? │ U+5F  _ │ U+7F DEL│
""") + "</pre>")


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    logging.info(
        f"Command from {update.effective_user.username}: {update.message.text})"
    )
    location = "Moscow"
    if len(argv := re.split(r"\s", update.message.text)) >= 2:
        location = ' '.join(argv[1:])
    try:
        response = requests.get(
            f"http://wttr.in/{location}?format=%l;%c%t;%w&M",
            headers={"User-Agent": "curl"},
            timeout=5,
        )
        if response.status_code == 200:
            msg_lines = html.escape(response.text).split(";")
            msg_lines[0] = "<b>Location:</b> "+msg_lines[0]
            msg = '\n'.join(msg_lines)
            logging.info(f"Successfully retrieved weather")
        else:
            msg = f"Failed to retrieve weather (HTTP {response.status_code})"
            logging.info(f"Failed to retrieve weather: HTTP {response.status_code})")
    except Exception as e:
        msg = f"Failed to retrieve weather ({e.__class__.__qualname__})"
        logging.info(f"Failed to retrieve weather: {e})")
    await update.message.reply_html(msg)


async def sun_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    logging.info(
        f"Command from {update.effective_user.username}: {update.message.text})"
    )
    location = "Moscow"
    if len(argv := re.split(r"\s", update.message.text)) >= 2:
        location = ' '.join(argv[1:])
    try:
        response = requests.get(
            f"http://v2.wttr.in/{location}?FT",
            headers={"User-Agent": "curl"},
            timeout=5,
        )
        if response.status_code == 200:
            msg_line_parts = list(html.escape(re.sub(r'\s+', ' ', l).strip()).split(':', 1) for l in response.text.replace('|', '\n').splitlines()[-8:])
            msg_line_parts.insert(0, msg_line_parts.pop())
            msg_line_parts.insert(3, ('', '-'*40))
            msg = '\n'.join(f"{'<b>'+l+':</b>' if l else '':s} {f'<code>{r}</code>' if re.match('^ *[0-9]{2}:', r) else r}" for l, r in msg_line_parts)
            logging.info(f"Successfully retrieved sun times")
        else:
            msg = f"Failed to retrieve sun times (HTTP {response.status_code})"
            logging.info(f"Failed to retrieve sun timesHTTP {response.status_code})")
    except Exception as e:
        msg = f"Failed to retrieve sun times ({e.__class__.__qualname__})"
        logging.info(f"Failed to retrieve sun times: {e})")
    await update.message.reply_html(msg)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    logging.info(
        f"Command from {update.effective_user.username}: {update.message.text})"
    )
    await reply_help(update)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    logging.info(
        f"Command from {update.effective_user.username}: {update.message.text})"
    )
    await reply_help(update)


async def reply_help(update: Update) -> None:
    command_name = None
    command_desc = None
    if len(argv := re.split(r"\s", update.message.text)) == 2:
        command_name = argv[1].lstrip("/")
        for group in COMMAND_DESCS.values():
            command_desc = group.get(command_name, [None, None])[1]
            if command_desc:
                break

    if not command_desc:
        msg = ''
        for group_name, commands in COMMAND_DESCS.items():
            msg += f"<b>{group_name}</b>\n"
            msg += "\n".join({f"  /{k} -- {v[0]}" for k, v in commands.items()}) + '\n\n'
        msg += "Use /help COMMAND_NAME for the command details, e.g.: <code>/help weather</code>"
    else:
        msg = f"/{command_name} {command_desc}"

    await update.message.reply_html(msg)


async def invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    logging.info(
        f"(Invalid) command from {update.effective_user.username}: {update.message.text})"
    )
    await update.message.reply_text('Invalid command. Run /help to see the command list.')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    try:
        logging.info(
            f"Message in {update.effective_chat.username} from {update.effective_user.username}: {update.message.text})"
        )
    except Exception as e:
        logging.error(f"Logging failed: {e}")


def main() -> None:
    application = Application.builder().token(os.getenv("TELEGRAM_API_KEY")).build()

    application.add_handler(CommandHandler(COMMAND_HOLMES, holmes_command))
    application.add_handler(CommandHandler(COMMAND_WATSON, watson_command))
    application.add_handler(CommandHandler(COMMAND_SUN, sun_command))
    application.add_handler(CommandHandler(COMMAND_WEATHER, weather_command))

    application.add_handler(CommandHandler(COMMAND_HELP, help_command))
    application.add_handler(CommandHandler("start", start_command))

    application.add_handler(MessageHandler(filters.COMMAND, invalid_command))
    application.add_handler(MessageHandler(~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    main()
