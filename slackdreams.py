import os, re
from os import listdir
from os.path import isfile, join

import json
import pathlib

from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from slack_sdk.web.async_client import AsyncWebClient

THISDIR = pathlib.Path(__file__).parent.absolute()
with open(os.path.join(THISDIR, 'config.json')) as f:
    confkeys = json.load(f)

SLACK_APP_TOKEN = confkeys["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = confkeys["SLACK_BOT_TOKEN"]
ROOTDIR = confkeys["STABLE_DIFFUSION_ROOTDIR"]

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

def slack_msg_with_files(text, file_uploads_data, channel):
    print('uploading')

    upload = client.files_upload_v2(
        file_uploads=file_uploads_data,
        channel=channel,
        initial_comment="Visuals of " + text,
    )

    print("Result of Slack send:\n%s" % upload)

def get_new_files(text):
    outpath = "outputs/txt2img-samples"
    sample_path = os.path.join(outpath, "_".join(re.split(":| ", text)))[:150]
    files_to_upload = [f for f in listdir(sample_path) if isfile(join(sample_path, f))]
    slack_uploads = []
    idx=0
    for img_file in files_to_upload:
        idx += 1
        slack_uploads.append({ "file": join(ROOTDIR, sample_path, img_file), "title": str(idx), })

    return slack_uploads

def run_stable_diffusion(text):

    cmd = ( "/home/pim/.conda/envs/ldm/bin/python "
            + ROOTDIR + "/optimizedSD/optimized_txt2img.py "
            "--turbo --H 512 --W 768 "
            "--n_iter 1 --n_samples 4 --ddim_steps 50 "
            "--ckpt "+ROOTDIR+"/models/ldm/stable-diffusion-v1/model.ckpt "
            "--prompt \""+text+"\"" )

    return os.system(cmd)

@app.event("app_mention")
def mention_handler(body, logger):
    index = body["event"]["text"].find("> ")
    text = body["event"]["text"][index+2:].strip()
    channel_id = body["event"]["channel"]
    run_stable_diffusion(text)
    file_uploads = get_new_files(text)
    slack_msg_with_files( text='Done dreaming: '+text, file_uploads_data=file_uploads, channel=channel_id )

@app.command("/dream")
def dream_command(ack, body, logger):
    ack()
    channel_id = body["channel_id"]
    text = body["text"]
    run_stable_diffusion(text)
    file_uploads = get_new_files(text)
    slack_msg_with_files( text='Done dreaming: '+text, file_uploads_data=file_uploads, channel=channel_id )

if __name__ == "__main__":
    print("Starting Dream Machine")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
