import json,urllib
import requests
import pandas as pd
from matn import namangan,andijon,samarqand,toshkent,qqr,xorazm,fargona,buxoro,jizzax,sirdaryo,surxondaryo,qashqadaryo,tosh_vil,navoiy
telegramniki= "https://api.telegram.org/bot1950870462:AAEXoqj1Pgl89TnJS8y2rv_aueKggqBH9Eg/"
from flask import Flask
from flask import request,Response
from flask_sslify import SSLify
app=Flask(__name__)
sslify=SSLify(app)
def get_url(url):
    content = requests.get(url).content.decode("utf8")
    return content
def build_keyboard(keyboard):
    return json.dumps({"keyboard":keyboard,"resize_keyboard":True, "one_time_keyboard": True})
def inline_keyboard(in_keyboard):
    return json.dumps({"inline_keyboard":in_keyboard})
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = telegramniki + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
def send_location(chat_id,latitude,longitude):
    url = telegramniki + "sendLocation?chat_id={}&latitude={}&longitude={}".format(chat_id,latitude,longitude)
    get_url(url)
@app.route("/",methods=["POST","GET"])
def index():
    if request.method=="POST":
        data=request.get_json()
        print(data)
        if list(data)[1]=="callback_query":
            keyboard=[["↩️ Bosh sahifaga qaytish"]]
            m=build_keyboard(keyboard)
            print(data['callback_query']['data'])
            chat_id=data['callback_query']["message"]['chat']["id"]
            print(chat_id)
            if data['callback_query']['data']=="andijon":
                send_message(andijon,chat_id)
            elif data['callback_query']['data']=="namangan":
                send_message(namangan,chat_id)
            elif data['callback_query']['data']=="qqr":
                send_message(qqr,chat_id)
            elif data['callback_query']['data']=="fargona":
                send_message(fargona,chat_id)
            elif data['callback_query']['data']=="qashqadaryo":
                send_message(qashqadaryo,chat_id)
            elif data['callback_query']['data']=="surxondaryo":
                send_message(surxondaryo,chat_id)
            elif data['callback_query']['data']=="samarqand":
                send_message(samarqand,chat_id)
            elif data['callback_query']['data']=="buxoro":
                send_message(buxoro,chat_id)
            elif data['callback_query']['data']=="toshkent":
                send_message(toshkent,chat_id)
            elif data['callback_query']['data']=="tosh_vil":
                send_message(tosh_vil,chat_id)
            elif data['callback_query']['data']=="navoiy":
                send_message(navoiy,chat_id)
            elif data['callback_query']['data']=="sirdaryo":
                send_message(sirdaryo,chat_id)
            elif data['callback_query']['data']=="xorazm":
                send_message(xorazm,chat_id)
            elif data['callback_query']['data']=="jizzax":
                send_message(jizzax,chat_id)
            send_message("🔘 Yuqoridagi o'zingizga kerakli TETKdan kerakli TR ni lokatsiyasini "+
                        "TETK kodi+TR nomi , ya'ni Masalan:'03203-21' shaklda yozib topasiz",chat_id,m)
        elif list(data)[1]=='message':
            chat_id = data['message']['chat']['id']
            message_text = data['message']['text']
            print(message_text)
            print(chat_id)
            keyboard2 = [[{"text":"📍 Андижанское ПТЭС","callback_data":"andijon"},{"text":"📍 Бухарское ПТЭС","callback_data": "buxoro"}],
            [{"text":"📍 Джизакское ПТЭС","callback_data": "jizzax"},{"text":"📍 Кашкадарьинское ПТЭС","callback_data": "qashqadaryo"}],
            [{"text":"📍 Навоийское ПТЭС","callback_data": "navoiy"},{"text":"📍 Наманганское ПТЭС","callback_data": "namangan"}],
            [{"text":"📍 Самаркандское ПТЭС","callback_data": "samarqand"},{"text":"📍 Сурхандарьинское ПТЭС","callback_data": "surxondaryo"}],
            [{"text":"📍 Сырдарьинское ПТЭС","callback_data": "sirdaryo"},{"text":"📍 Таш ГорПЭС","callback_data": "toshkent"}],
            [{"text":"📍 Ташкентское ПТЭС","callback_data": "tosh_vil"},{"text":"📍 Ферганское ПТЭС","callback_data": "fargona"}],
            [{"text":"📍 Хорезмское ПТЭС","callback_data": "xorazm"},{"text":"📍 Каракалпакское ПТЭС","callback_data": "qqr"}]]
            if message_text=="/start" or message_text=="↩️ Bosh sahifaga qaytish":
                m=inline_keyboard(keyboard2)
                send_message("⭕️ Assalomu alaykum 'Hududiy Elektr Tarmoqlari Korxonasi'ni tanlang",chat_id,m)
            elif message_text[0:1]=="0" or message_text[0:1]=="1" or message_text[0:1]=="2" or message_text[0:1]=="3":
                send_message("🔎 Qidirilmoqda ...📂📂📂",chat_id)
                df = pd.read_excel("/home/datacenternuriddin/bot/17000.xlsx")
                #c=pd.DataFrame(df,columns=["TR_ESP","Manager Name","Substation","Feeder","Mobile","DCU No.","Latitude","Longitude"])
                filt=(df["TR_ESP"]==message_text)
                tr_check=df.loc[filt]
                if tr_check.empty:
                    send_message("🟤 Bu Transformatorga lokatsiya kiritilmagan!",chat_id)
                else:
                    print(filt)
                    print("sam="+str(tr_check))
                    lat=df.loc[filt,"Latitude"]
                    lon=df.loc[filt,"Longitude"]
                    dcu=df.loc[filt,"DCU No."]
                    balans=df.loc[filt,"Balans_Meter"]
                    master=df.loc[filt,"Manager Name"]
                    telefon=df.loc[filt,"Mobile"]
                    fider=df.loc[filt,"Feeder"]
                    podstansiya=df.loc[filt,"Substation"]
                    print(dcu)
                    print(master)
                    print(telefon)
                    send_location(chat_id,float(lat),float(lon))
                    send_message("🟡 TR: "+message_text[6:]+"\n"+"🟡 Podstansiyasi: "+podstansiya.to_string(index=False)+"\n"+"🅱️ Balans Hisoblagich: "+balans.to_string(index=False)+"\n"+"🟡 Fideri: "+fider.to_string(index=False)+"\n"+"🟡 Konsentrator: "+dcu.to_string(index=False)+"\n"+"🟡 Biriktirilgan Master: "+master.to_string(index=False)+"\n"+"📞 Telefon raqami: "+telefon.to_string(index=False),chat_id)
            else:
                send_message("⚠️ Siz xato ma'lumot yubordingiz bazada mavjudmas!",chat_id)
        else:
            print("nothing")
        return  Response("OK",status=200)
    else:
        return "<h1>Telegram_Bot</h1>"
if __name__ == '__main__':
    app.run(debug=True)
