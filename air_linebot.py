# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextSendMessage,ImageSendMessage,StickerSendMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,URITemplateAction,PostbackTemplateAction, events
from linebot.models import messages
from linebot.models.messages import ImageMessage,TextMessage,LocationMessage
import time
import json
from linebot.models.responses import Content
from pymongo import MongoClient, collection
import random
from air_functions import air_aqi
# create flask server
# hotbooks = 1
app = Flask(__name__)

secretFile=json.load(open("secretFile.json",'r'))
channelAccessToken=secretFile['channelAccessToken']
channelSecret=secretFile["channelSecret"]

line_bot_api =LineBotApi(channelAccessToken)
handler=WebhookHandler(channelSecret)


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
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
# #     # get user info & message
#     user_id = event.source.user_id
#     msg = event.message.text
#     user_name = line_bot_api.get_profile(user_id).display_name
#     # line_bot_api.reply_message(event.reply_token, 
#     #                             [TextSendMessage(text = '本機自動回覆'),
#     #                             StickerSendMessage(package_id='6325',sticker_id='10979908')])
    
#     # # push text_msg
#     # line_bot_api.push_message(user_id,
#     #                             TextSendMessage(text = '您好^^'))
#     # get msg details
#     print('msg from [', user_name, '](', user_id, ') : ', msg)
#     storedID = {'_id':user_id,'userName':user_name,'Log':msg}
#     # mongo.kingstone_stored(storedID)
#     print(msg)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message == '@使用說明':
        line_bot_api.reply_message(event.reply_token,
                            [TextSendMessage(text = '您好！歡迎使用空氣服務小幫手，請傳送"位置資訊"，獲取本日空氣品質資訊唷！'),
                            ImageSendMessage(original_content_url="https://i.imgur.com/6dF6v17.jpg",preview_image_url="https://i.imgur.com/6dF6v17.jpg")])
                            
@handler.add(MessageEvent,message=LocationMessage)
def handle_location(event):
    # location = event.message
    longitude = event.message.longitude
    latitude = event.message.latitude
    aqi = round(air_aqi([latitude,longitude]))
    print('經度:',longitude,'緯度:',latitude)
    print('aqi:',aqi)
    # aqi = 5000
    if aqi <= 50 :
        line_bot_api.reply_message(event.reply_token,
                            [TextSendMessage(text = '今日AQI：%s，空氣品質良好，可以正常戶外運動喔！'%(str(aqi)))])
    elif 51 < aqi <= 100:
        line_bot_api.reply_message(event.reply_token,
                            [TextSendMessage(text = '今日AQI：%s，空氣品質普通，可以正常戶外運動喔！'%(str(aqi)))])
    elif 101 < aqi <= 150:
        line_bot_api.reply_message(event.reply_token,
                            [TextSendMessage(text = '今日AQI：%s，空氣品質不佳，過敏性體質的朋友要注意喔！'%(str(aqi)))])
    elif 151 < aqi <= 200:
        line_bot_api.reply_message(event.reply_token,
                            [TextSendMessage(text = '今日AQI：%s，空氣品質不健康，所有朋友要注意！盡量不要長時間戶外活動!!'%(str(aqi)))])
    elif 201 < aqi <= 300:
        line_bot_api.reply_message(event.reply_token,
                            [TextSendMessage(text = '今日AQI：%s，空氣品質非常不健康，所有朋友要注意！不要長時間戶外活動!!能在室內活動是最好的!!'%(str(aqi)))])
    elif aqi > 301:
        line_bot_api.reply_message(event.reply_token,
                            [TextSendMessage(text = '今日AQI：%s，危害品質空氣! 危害品質空氣! 請注意!!!室內緊閉門窗，停止在外活動!!'%(str(aqi)))])
    # print(location)

# run app
if __name__ == "__main__":
    app.run(host='localhost',debug=True, port=12345)
