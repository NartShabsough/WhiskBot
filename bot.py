import json
import requests
import re
import time
import urllib
import datetime

from random import randint
from dbhelper import DBHelper

db = DBHelper()

TOKEN = "425044369:AAHS5yc9dU8ETJL6VlSsvPDfd6orE-uW4Ug"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

restaurant_name = ""
restaurant_phone = ""
restaurant_latitude = 0
restaurant_longtitude = 0
    
menuInProgress =0
reservationInProgress=0


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def prepareResponse(text, chat, name):
    with open('word.json') as data_file:
        data = json.load(data_file)
    with open('replies.json') as data_file:
        replies = json.load(data_file)

    #Check greeting
    print("------")

    parts = text.split()
    global restaurant_name, restaurant_phone, restaurant_latitude, restaurant_longtitude
    greeting=0
    location=0
    reservation=0
    cancel=0
    contact=0
    menu=0

    for x in parts:
        word = data["greeting"]
        for y in word:
            if re.search(y, x, re.IGNORECASE):
                greeting=1

        word = data["location"]
        for y in word:
            if re.search(y, x, re.IGNORECASE):
                location=1

        word = data["reservation"]
        for y in word:
            if x == "cancel" or x == "delete":
                cancel=1
            if re.search(y, x, re.IGNORECASE):
                reservation=1

        word = data["contact"]
        for y in word:
            if re.search(y, x, re.IGNORECASE):
                contact=1

        word = data["menu"]
        for y in word:
            if y ==x:
                menu=1

    print(greeting,location,reservation,contact,menu)
    global menuInProgress,reservationInProgress
    print(reservationInProgress)

    if menuInProgress == 1:
        print("Menu in progress")
    elif reservationInProgress == 1:
        handle_reservation(text, chat, "con")
    else:
        if greeting==1 and location==0 and reservation==0 and contact==0 and menu==0:
            r = randint(0, 3)
            k = randint(0, 2)
            word1 = replies["his"]
            word2 = replies["greetingAlone"]
            reply = word1[r] + " " + name + ",\n" + word2[k]
            send_message(reply ,chat)
            return

        if greeting==0 and location==1:
            l = randint(0, 2)
            loc = replies["location"]
            send_message(loc[l],chat)
            send_location(restaurant_latitude, restaurant_longtitude, chat);
            return

        if greeting==1 and location==1:
            r = randint(0, 3)
            k = randint(0, 1)
            l = randint(0, 2)
            word1 = replies["his"]
            word2 = replies["greeting"]
            loc = replies["location"]
            reply = word1[r] + " " + name + ",\n" + word2[k] + "\n\n" + loc[l]
            send_message(reply,chat)
            send_location(restaurant_latitude, restaurant_longtitude, chat);
            greeting=0
            return

        if greeting==0 and contact==1:
            c = randint(0, 2)
            con = replies["contact"]
            reply = con[c] + " " + restaurant_phone
            send_message(reply,chat)
            return

        if greeting==1 and contact==1:
            r = randint(0, 3)
            k = randint(0, 1)
            c = randint(0, 2)
            word1 = replies["his"]
            word2 = replies["greeting"]
            con = replies["contact"]
            reply = word1[r] + " " + name + ",\n" + word2[k] + "\n\n" + con[c] + " " + restaurant_phone
            send_message(reply,chat)
            greeting=0
            return

        if greeting==0 and menu==1:
            send_message("We are still working on showing the menu",chat)
            return

        if greeting==1 and menu==1:
            send_message("Hi, /nSorry but we are still working on showing the menu",chat)
            greeting=0
            return

        if greeting==0 and reservation==1:
            reservationInProgress = 1
            if cancel==1:
                handle_reservation(text,chat, "cancel")
            else:
                handle_reservation(text, chat, "new")
            return

        if greeting==1 and reservation==1:
            r = randint(0, 3)
            k = randint(0, 1)
            l = randint(0, 2)
            word1 = replies["his"]
            word2 = replies["greeting"]
            reply = word1[r] + " " + name + ",\n" + word2[k]
            greeting=0
            send_message(reply,chat)
            reservationInProgress = 1
            if cancel==1:
                handle_reservation(text,chat, "cancel")
            else:
                handle_reservation(text, chat, "new")
            return







        #Unclear request
        if greeting==0 and location==0 and reservation==0 and contact==0 and menu==0:
            reply = "Sorry " + name + ", " + "I'm still new at this job, what did you mean ?"
            send_message(reply,chat)




#    if data["greeting"][0] in text:

#    if re.search("hi", text, re.IGNORECASE) or re.search("hey", text, re.IGNORECASE) or re.search("hello", text, re.IGNORECASE) or re.search("moin", text, re.IGNORECASE) or re.search("hallo", text, re.IGNORECASE):
#        mes = ("Hey "+clientName+"\n")
#            send_message(mes,chat)

    return 3,2,3


def handle_updates(updates):
    for update in updates["result"]:
        #Get chat details
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        clientName = update["message"]["chat"]["first_name"]
        
        #Get restaurant info
        resName = db.get_restaurant("name")
        resNum = db.get_restaurant("phone")
        resLocationlong = db.get_restaurant("long")
        resLocationlat = db.get_restaurant("lat")
        
        #Analyse Response
        k = prepareResponse(text, chat, clientName)


def handle_reservation(text, chat, type):

    global Command
    if type=="new":
        showDates(chat)
        text = "/new"
        Command = text
    elif type=="cancel":
        send_message("Please enter your reservation ID to cancel:", chat, None)
        text = "/cancel"
        Command = text
    elif text=="/show" or text=="i want to see all Reservations":
        #showList(updates)
        print("show")
    else:
        handle_command(text,chat)



def new(text, chat):
    global reservationDate,reservationHour,table_ID,Command, reservationInProgress
    if reservationDate==None :
        reservationDate=text
        keyboard = build_keyboard(Hourlist)
        send_message("At what time do you prefer?", chat, keyboard)

    elif reservationHour==None :
        reservationHour = text
        freetables = db.get_freetables(reservationDate,reservationHour)
        List=[]
        for value in freetables:
            print("table:",value)
            List.append(str(value))
        keyboard = build_keyboard(List)
        if not List:
            send_message("Sorry, but we have no free tables at this time!\nYou could try a different time!", chat, keyboard)
            table_ID = None
            reservationDate = None
            reservationHour = None
            Command = None
            reservationInProgress = 0
        else:
            send_message("Perfect!\nPlease select one of our free tables:", chat, keyboard)
    
    elif table_ID == None:
        send_message("Thank you!\nAnd the reservation will be under the name of ?", chat, None)
        table_ID=text
    else:
        customerName=text
        reservation_ID = db.add_reservation(customerName,reservationDate,table_ID,reservationHour)
        reply = "Reservation is completed, Thank you!!\n\nYour reservation number is: #" + reservation_ID + "\n" + "See you then :)"
        send_message(reply, chat, None)
        table_ID = None
        reservationDate = None
        reservationHour = None
        Command = None
        
        reservationInProgress = 0

def cancel(text, chat):
    global Command
    reservation_ID = text
    db.cancel_reservation(reservation_ID)
    send_message("Your reservation is canceled!\nHope to see you soon!",chat,None)
    Command = None
    global reservationInProgress
    reservationInProgress = 0

def showDates(chat):
    items = Daylist
    keyboard=build_keyboard(items)
    send_message("Sure!\nPlease select which day...", chat, keyboard)

def showList(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        reservationsList = db.get_List()
        for value in reservationsList:
            send_message(str(value), chat, None)

def handle_command(text,chat):
    if Command=="/new" :
        new(text, chat)
    elif Command=="/cancel":
        cancel(text, chat)
    else:
        send_message("I am sorry. I did not understand you, please write again! These are possible commands: /new /cancel /show ...",chat,None)


def set_Date():
    global Daylist
    global Hourlist
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    Daylist = []
    Daylist.append(str(today))
    
    for i in range(0, 5):
        today = today + one_day
        Daylist.append(str(today))

    start_hour = datetime.timedelta(hours=9)
    one_hour = datetime.timedelta(hours=1)
    Hourlist = []
    Hourlist.append(str(start_hour))

    for i in range(0, 14):
        start_hour = start_hour + one_hour
        Hourlist.append(str(start_hour))



def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def send_location(latitude,longitude, chat_id, reply_markup=None):
    url = URL + "sendLocation?latitude={}&longitude={}&chat_id={}&parse_mode=Markdown".format(latitude,longitude, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)



def main():
    db.setup()
    last_update_id = None
    
    #Restaurant
    restaurantName = db.get_restaurant("name")
    if restaurantName == "0":
        db.create_restaurant("Vapianno","04211683847","53.078846","8.8049183")
        db.add_table(1,10,0)
        db.add_table(2,5,1)
        db.add_table(3,15,1)
        db.add_table(4,5,0)
        db.add_table(5,10,1)
        db.add_menu("Water","Small","1.5","drink")
        db.add_menu("CocaCola","Small","2","drink")
        db.add_menu("Fanta","Small","2","drink")
        db.add_menu("7up","Small","2","drink")
        db.add_menu("Orange Juice","Small","1.5","drink")
        db.add_menu("Apple Juice","Small","1.5","drink")
        db.add_menu("Pasta","Small","3.5","food")
        db.add_menu("Cesar Salad","Small","2.7","food")
        db.add_menu("Lasange","Small","5","food")
        db.add_menu("Pizza","Small","5","food")


    global restaurant_name
    restaurant_name = db.get_restaurant("name")
    global restaurant_phone
    restaurant_phone = db.get_restaurant("phone")
    global restaurant_latitude
    restaurant_latitude = db.get_restaurant("latitude")
    global restaurant_longtitude
    restaurant_longtitude = db.get_restaurant("longtitude")

    #Reservation
    set_Date()
    global Command,reservationDate, reservationHour,customerName,table_ID
    Command = None
    reservationDate = None
    reservationHour = None
    customerName = None
    table_ID = None

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
