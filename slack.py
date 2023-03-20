import os
import schedule
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN="xoxb-804402372193-4978877842851-mIwYKtXvKD3QzzVFp6s5fzWR"

logging.basicConfig(level=logging.DEBUG)

def sendMessage(slack_client, msg):
    try:
        slack_client.chat_postMessage(
        channel='#dreaming',
        text=msg
    )#.get()
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)

if __name__ == "__main__":
    slack_client = WebClient(SLACK_BOT_TOKEN)
    logging.debug("authorized slack client")

    msg = "Good Morning!"
    schedule.every(5).seconds.do(lambda: sendMessage(slack_client, msg))

    logging.info("entering loop")

    while True:
        schedule.run_pending()
        time.sleep(5) # sleep for 5 seconds between checks on the scheduler
