from TelegramBot import TelegramBot
from constants import GROUP_ID
from secrets import TELEGRAM_API_TOKEN




if __name__ == "__main__":
    bot = TelegramBot(TELEGRAM_API_TOKEN)
    r = bot.get_message()
    print(r)

    s = bot.send_message("hello world", GROUP_ID)
    print(s)