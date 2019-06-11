from flask import Flask, request, abort
import pandas as pd
import random
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#from linebot.models import (
#    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage
#)

app = Flask(__name__)

line_bot_api = LineBotApi('kuvtbHE3VKJsPYb8G47DQ9lc3m5KCBvx+uUmLdEFke8MNPDOYotdnJN8mVCYOefG9yPyqTYYk66XP6hg9N2f9ti1gC+vUMBbp2dQOgs8xqAHH3Vbj6tJhUtOCbfhpg7hp6X2vYBVnfEuFQBVLhLILwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('46842775f02df624850c42d1de35085f')

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
greetings = "歡迎使用Bot予置評，請選擇您所喜歡的分類"
clickbait = "->繼續閱讀請回more"
greeted = False
df = pd.read_pickle("newslens_1.pkl")
database = {}
for n, (title,content) in enumerate(zip(df['title'],df['content'])):

    content = ''.join(content)
    if len(content) < 20:
        continue
    else:
        database[len(database)] = {"title":title,"content":content}
meassages = ["hey"]
past = []

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    #msg = msg.encode('utf-8')
    #msg_reply= ImageSendMessage(original_content_url="https://github.com/Splend1d/2019LingProject/blob/master/twtags_lda.png?raw=true",
    #    preview_image_url="https://github.com/Splend1d/2019LingProject/blob/master/twtags_lda.png?raw=true")
    #msg_reply = TemplateSendMessage(
    #alt_text='Confirm template',
    #template=ConfirmTemplate(
    #    text='Are you sure?',
    #    actions=[
    #        PostbackTemplateAction(
    #            label='postback',
    #            text='postback text',
    #           data='action=buy&itemid=1'
    #        ),
#             # MessageTemplateAction(
#                 label='message',
#                 text='message text'
#             )
#         ]
#     )
# )
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    #content = "{}: {}".format(event.source.user_id, event.message.text)
        #TextSendMessage(text=event.message.text))
    global greeted
    print(">:",msg)
    if not greeted:
        reply = greetings
        greeted = True
    elif msg == "news":
        rnd = random.randint(0,len(database))
        reply = database[rnd]["title"] + clickbait
        past.append(rnd)
    elif msg == "more":
        try:
            rnd = past[-1]
        except:
            reply = "not implemented error"
        else:
            reply = database[rnd]["content"][
    else:
        reply = "not implemented error"
        #TextSendMessage(text=event.message.text))

    line_bot_api.reply_message(
            event.reply_token,
            #msg_reply,
            TextSendMessage(text=reply[0:2000]))
import os
if __name__ == "__main__":

    app.run(debug=True, port=80)
