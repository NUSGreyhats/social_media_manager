from TelegramBot import TelegramBot
from constants import GROUP_ID
from secrets import TELEGRAM_API_TOKEN




if __name__ == "__main__":
    bot = TelegramBot(TELEGRAM_API_TOKEN)
    r = bot.get_message()
    print(r)

    # s = bot.send_message("hello world", GROUP_ID)
    # print(s)

    s = bot.send_image("Test image post", GROUP_ID, r"D:\Downloads\greycat.jpg")
    print(s)