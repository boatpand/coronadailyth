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

import requests
import random
import datetime
import schedule

app = Flask(__name__)

URL = "https://corona.lmao.ninja/v2/countries/THA"
response = requests.get(URL)
data = response.json()

# line webhook : https://coronadailyth.herokuapp.com/webhook
line_bot_api = LineBotApi('RfDEGr9qfOkcWQ6zB4kQMdjuq8d7F+4GK1rGS4Ncx5j8uzGoiqPgm6II3WeC07q4mo7oJDyl5BV10KOi4PUVboYQS3VOSAF4CdWqt8Gb91xCdO/ntyiMasuBL1gp2CMKjtxVvxOCWWaWtC3FmBBKNAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('60155d582adb7f366c127dd4237c5ac7')

####################### new ########################
@app.route('/')
def index():
    return "Hello world!"

@app.route('/webhook', methods=['POST'])
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

now = datetime.datetime.now() + datetime.timedelta(0.291667)
date = now.strftime("%d/%m/%Y")
t = now.strftime("%X")

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "covid":
        msg0 = "ข้อมูลประจำวันที่ " + str(date) + " เวลา " + str(t) + '\n'
        msg1 = "ผู้ติดเชื้อวันนี้ " + str(data["todayCases"]) + " ราย" + "\n"
        msg2 = "ผู้ติดเชื้อสะสม " + str(data["cases"]) + " ราย" + "\n"
        msg3 = "ผู้เสียชีวิตวันนี้ " + str(data["todayDeaths"]) + " ราย" + "\n"
        msg4 = "ผู้เสียชีวิตสะสม " + str(data["deaths"]) + " ราย" + "\n"
        msg5 = "หายป่วยวันนี้ " + str(data["todayRecovered"]) + " ราย" + "\n"
        msg6 = "หายป่วยสะสม " + str(data["recovered"]) + " ราย"
        msg = msg0 + msg1 + msg2 + msg3 + msg4 + msg5 + msg6
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

    else:
        msg1 = "สถานการณ์ covid-19 โดย กรมควบคุมโรค" + "\n" + "https://ddc.moph.go.th/viralpneumonia/index.php"
        msg2 = "วิธีป้องกัน covid-19 โดย โรงพยาบาลศิครินทร์" + '\n' + "https://www.sikarin.com/content/detail/408/%E0%B8%A7%E0%B8%B4%E0%B8%98%E0%B8%B5%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9B%E0%B9%89%E0%B8%AD%E0%B8%87%E0%B8%81%E0%B8%B1%E0%B8%99-%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%A1%E0%B8%B7%E0%B8%AD-%E0%B9%84%E0%B8%A7%E0%B8%A3%E0%B8%B1%E0%B8%AA-covid-19"
        msg3 = "อาการ covid-19 โดย Kapook!" + "\n" + "https://covid-19.kapook.com/view224756.html"
        msg4 = "รู้ให้ชัดก่อนฉีดวัคซีน COVID-19" + "\n" + "https://www.bangkokhospital.com/content/know-well-before-getting-the-covid-19-vaccine"
        msg5 = 'หากต้องการทราบรายละเอียดผู้ติดเชื้อวันนี้พิมพ์ "covid" หรือกด menu "covid"'
        msg6 = 'หากต้องการทราบรายงานความก้าวหน้าการให้บริการฉีดวัคซีนโควิด 19 กด menu "vaccine"'
        mylist = [msg1,msg2,msg3,msg4,msg5,msg6]
        msg = random.choice(mylist)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
            
if __name__ == '__main__':
    app.run(debug=True)