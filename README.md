# The Truman Show

Tools to simulate discord server interaction with user accounts.  

# Usage
Create a `bots.json` file in the same directory as the program.  
Example `bots.json`:
```json
[
    {
        "auth": "fast_typer_auth",
        "wpm": 120,
        "tasks": [
            {
                "channelId": "channelid",
                "minWaitSecs": 30,
                "waitSecsVariance": 60,
                // Path to a list of messages in the same directory
                "messagesList": "text.txt"
            },
            {
                "channelId": "channelid2",
                "minWaitSecs": 60,
                "waitSecsVariance": 120,
                "messagesList": "text.txt"
            }
        ]
    },
    {
        "auth": "slow_typer_auth",
        "wpm": 60,
        "tasks": [
            {
                "channelId": "channelid",
                "minWaitSecs": 200,
                "waitSecsVariance": 400,
                "messagesList": "text.txt"
            }
        ]
    }
]
```

Example message lists file:  
```
How is everyone doing today?
Oh wow!
Bruh
????
wtf
What is yalls favorite fruit?
```
For now, all messages will have their first word become lowercase, and stripped of commas and punctuation.  
