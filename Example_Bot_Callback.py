from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('KlQ0S8Yi/OppZKUM9IX4FrztDxbP++YGbiwOSjEoekXZ6KcfxJbUASKDAJLvbSaL7riClvEZ5H8UkaSJ/dOk8vXZAUDM8rFFJkudhdRgJU8I8y8qiIVBpBGkMDEl5xkYmaxRFWJ9FF/0QC1dy90PYwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('11d48b7e7d2226fe00fcebe4cb9d14b1')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()