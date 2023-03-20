import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from slack_sdk.web.async_client import AsyncWebClient

SLACK_APP_TOKEN="xapp-1-A0501C01GSC-4990359212273-07c020548263e3235bcb4d4d7e3d976120d5ed576402da4dc7c7cfa71526bfcf"
SLACK_BOT_TOKEN="xoxb-804402372193-4978877842851-mIwYKtXvKD3QzzVFp6s5fzWR"

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

def slack_msg_with_files(message, file_uploads_data, channel):
    print('uploading')

    upload = client.files_upload_v2(
        file_uploads=file_uploads_data,
        channel=channel,
        initial_comment=message,
    )
    print("Result of Slack send:\n%s" % upload)

app.event("app_mention")
def mention_handler(body, say):
    print("hallo")
    say('Hello World!')

@app.command("/dream")
def dream_command(ack, body, logger):
    ack()

    channel = body["channel_name"]
    channel_id = body["channel_id"]
    text = body["text"]

    cmd = "ls"
    returned_value = os.system(cmd)  # returns the exit code in unix
    print('returned value:', returned_value)
    response = client.chat_postMessage(
        channel=channel,
        text=f"Hi <@{returned_value}>!"
    )

    file_uploads = [
        {
            "file": "./logotn.png",
            "title": "1st",
        },
    ]

    slack_msg_with_files(
        message='visualizing: '+text,
        file_uploads_data=file_uploads,
        channel=channel_id
    )

    logger.info(body)

if __name__ == "__main__":
    print("starting bot")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
