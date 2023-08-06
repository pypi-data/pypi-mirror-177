import sys
import argparse

from .client import Bot


def parse_args():
    parser = argparse.ArgumentParser(description='Telegram bot for tvmaze.com')
    parser.add_argument(
        "-t",
        action="store",
        dest="token",
        required=True,
        type=str,
        help="Secret telegram bot token",
    )
    return parser.parse_args()


TELEGRAM_TOKEN = parse_args().token

if __name__ == "__main__":
    tg_bot = Bot(TELEGRAM_TOKEN)
    print("Telegram bot has started")
    try:
        tg_bot.start()
    except KeyboardInterrupt:
        print("Telegram bot stopped working")
        sys.exit(0)
