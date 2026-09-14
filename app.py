from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    VideoMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import os

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
herta_bot_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        herta_bot_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

import random

@herta_bot_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        text = event.message.text
        if text == '轉圈圈':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text = '轉圈圈遊戲進行中，請自行探索~')]
                )
            )
        else:
            rand = random.randint(1, 3)
            if(rand == 1):
                herta = random.randint(1, 218)
                if(herta == 1):
                    url = request.url_root.replace('http', 'https') + '/static/kurukuru.mp4'
                    prev_url = request.url_root.replace('http', 'https') + '/static/kurukuru.png'
                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[VideoMessage(original_content_url = url, preview_image_url = prev_url)]
                        )
                    )
                else:
                    url = request.url_root.replace('http', 'https') + '/static/kurukuru-2.mp4'
                    prev_url = request.url_root.replace('http', 'https') + '/static/kurukuru-2.png'
                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[VideoMessage(original_content_url = url, preview_image_url = prev_url)]
                        )
                    )

if __name__ == "__main__":
    app.run()
