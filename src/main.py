import time
import json
from bot import Bot
from log import err

if __name__ == "__main__":
    try:
        with open("bots.json", 'r') as f:
            data = json.load(f)

        for bot_json in data:
            bot = Bot(bot_json)
            bot.run()

        while True:
            time.sleep(2000000)
        
    except FileNotFoundError:
        err("Need a bots.json file.")

    except Exception as e:
        err(f"Unknown error {e}")