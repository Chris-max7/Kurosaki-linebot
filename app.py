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

line_bot_api = LineBotApi('/574UMAGdu2Tejpy/+Kxt+k2yUsb5Zy+VdTYgVQQsL59iajdCdNvGL6BxOgc0FL35XYjOiTgpo8TngFDv7L8W8mMwjs4YThl8r1BQLKUJNCrjDYwMAp9dC/hsDiFYN6jYuhDP46ofG+N/yGDd0+ynwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('62380b81935e58f3fa2061edf48d89f4')

@app.route("/")
def test():
    return "OK"

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

reply_message = 0
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "ありがとう":
        reply_message = "どういたしまして。"
    elif event.message.text == 'こんにちは' or event.message.text == 'こんばんは' or event.message.text == 'おはよう':
        reply_message = f"{event.message.text}！"
    elif "名前は？" in event.message.text:
        reply_message = "黒崎だよ！"
    else:    
        reply_message = f"あなたは、{event.message.text}と言いました。"
    
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()