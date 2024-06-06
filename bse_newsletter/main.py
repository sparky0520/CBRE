import random
import time
from action import send_news

send_news()
while True:
    # Choose a random time between 15 and 30 minutes
    interval = random.randint(15, 30)
    interval_seconds = interval * 60
    # Wait for that amount of time
    print(f"Sleeping for {interval} minutes")
    time.sleep(interval_seconds)
    send_news()
