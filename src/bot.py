import requests
from log import log, err
from task import Task
import threading

class Bot:
    auth: str
    name: str
    wpm: int
    tasks: list[Task] = []
    threads: list[threading.Thread]
    
    def __init__(self, json_data):
        self.auth = json_data["auth"]
        self.name = self.fetchName()
        self.log("logged in")
        self.wpm = json_data["wpm"]
        self.threads = []
        self.tasks = []

        for task_data in json_data["tasks"]:
            self.tasks.append(Task(task_data, self.auth, self.name, self.wpm))

    def run(self):
        for task in self.tasks:
            thread = threading.Thread(daemon=True, target=task.run)
            self.threads.append(thread)
            thread.start()

    def log(self, msg: str):
        log(f"[{self.name}] {msg}")
        
    def fetchName(self) -> str:
        header = {
            'authorization': self.auth,
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        r = requests.get("https://discord.com/api/v9/users/@me", headers=header)

        if int(r.status_code / 100) == 2:
            data = r.json()
            return data["username"]
        else:
            err(f"bad token \"{self.auth}\"")
