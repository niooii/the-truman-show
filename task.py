import random
import time
import requests
from log import log, err

def lines(path: str) -> list[str]:
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        err(f"so where is \"{path}\"")
    except UnicodeDecodeError:
        err("remove emojis")

def processMsg(msg: str) -> str:
    words = msg.split()
    lower_first = f"{words[0].lower()} {" ".join(words[1:])}".rstrip()
    return lower_first.replace("'", "").replace(",", "").replace("’", "").replace("you", "u").replace("your", "ur").replace("youre", "ur").replace("Im", "im")

# represents one task running for a bot user
class Task:
    channel_id: int
    min_wait_secs: float
    wait_secs_variance: float
    messages: list[str]
    wpm: int
    auth: str
    name: str

    def __init__(self, json_data, auth: str, name: str, wpm: int):
        self.channel_id = int(json_data["channelId"])
        self.min_wait_secs: int = json_data["minWaitSecs"]
        self.wait_secs_variance = json_data["waitSecsVariance"]
        self.messages = list(map(processMsg, [msg for msg in lines(json_data["messagesList"]) if len(msg.strip()) != 0]))
        self.auth = auth
        self.wpm = wpm
        self.name = name

    def log(self, msg: str):
        log(f"[{self.name} ({self.channel_id})] {msg}")

    def run(self):
        while True:
            self.log(f"shuffling messages..")
            random.shuffle(self.messages)

            messages = self.messages.copy()

            while len(messages) != 0:
                self.sendMsg(messages.pop())
                sleep_time = random.random() * self.wait_secs_variance + self.min_wait_secs
                self.log(f"waiting {sleep_time} secs..")
                time.sleep(sleep_time)

    def sendMsg(self, msg: str):
        header = {
            'authorization': self.auth,
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }

        def typingTime(msg: str) -> float:
            secs_per_char = 1.0/((self.wpm * 5.0) / 60.0)
            return len(msg) * secs_per_char
        
        typing_time = typingTime(msg)
        self.log(f"typing for {typing_time} secs..")
        requests.post(f"https://discord.com/api/v9/channels/{self.channel_id}/typing", headers=header);

        time.sleep(typing_time)
        
        payload = {
            'content': msg
        }

        r = requests.post(f"https://discord.com//api/v9/channels/{self.channel_id}/messages", data=payload, headers=header)

        if int(r.status_code / 100) == 2:
            self.log(f"sent \"{msg}\".")
        else:
            self.log(f"error sending.")
            self.log(f"response: {r}")