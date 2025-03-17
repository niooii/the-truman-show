from datetime import datetime

def getTimeStampedString(string: str) -> str:
    timestamp = datetime.now().timestamp()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%m-%d-%Y %H:%M:%S")
    return '[' + str_date_time + '] ' + string

def log(string: str):
    print(getTimeStampedString(string))

def err(msg: str):
    log(f"ERROR: {msg}")
    input("Press enter to continue..")
    exit(1)