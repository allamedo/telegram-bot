import requests
import config, firestore

telegram_message_json = {"update_id": 171356370, 
                        "message": {
                            "message_id": 63051,
                            "from": {
                                "id": 10532106, "is_bot": False, "first_name": "Dum User", "username": "dummy", "language_code": "es"},
                                "chat": {
                                     "id": 10532102, "first_name": "Dum Chat", "username": "dummy", "type": "private"},
                                "date": 1641592478, "text": "Portatil i7 con SSD <300€ https://es.wallapop.com/app/search?category_ids=15000&keywords=ssd%20portatil%20i7&latitude=43.3627&longitude=-5.84768&order_by=newest&filters_source=search_box&max_sale_price=300&min_sale_price=20",
                                "entities": [{"offset": 26, "length": 197, "type": "url"}]}}

class TelegramMessage():
    def __init__(self, telegram_request_message_json):
        try:
            self.update_id = telegram_request_message_json["update_id"]
            self.text = telegram_request_message_json["message"]["text"]
            self.chat_id = telegram_request_message_json["message"]["chat"]["id"]
            self.username = telegram_request_message_json["message"]["from"]["username"]
            self.valid = True
        except:
            self.valid = False

    def url(self) -> str:
        if self.valid and "http" in self.text:
            return self.text[self.text.index("http"):].rstrip()
        else:
            return ""
    def name(self) -> str:
        if self.valid and "http" in self.text:
            return self.text[:self.text.index("http")].rstrip()
        else:
            return ""
    def store(self) -> str:
        if 'wallapop.' in self.url()[:30]:
            return 'wallapop'
        elif 'zalando.' in self.url()[:30]:
            return 'zalando'
        else:
            return ''

def parse_message():

    #request_json = request.get_json()
    request_json = telegram_message_json
    message = TelegramMessage(request_json)

    if message.valid:

        if len(message.store()) > 0 and len(message.url()) > 0:

            if firestore.url_exists(message.url()):
                deleted_name = firestore.url_delete(message.url())
                print("Deleted Search URL: "+message.url()+" Chat ID: "+str(message.chat_id)+" Name: "+message.name()+ " Username: "+message.username)
                send_telegram_reply("He borrado tu búsqueda: "+deleted_name, message.chat_id)

            else:
                firestore.url_insert(message.url(),message.name(),message.chat_id,message.store(), message.username)
                print("Inserted Search URL: "+message.url()+" Chat ID: "+str(message.chat_id)+" Name: "+message.name()+ " Username: "+message.username)
                send_telegram_reply("He creado tu búsqueda: "+message.name(), message.chat_id)

        elif len(message.store()) == 0 and len(message.url()) > 0:
            send_telegram_reply("No reconozco la tienda que me has enviado. Puede que aún no la haya implementado...", message.chat_id)
        
        print("Telegram Bot parsed message. Update ID: "+str(message.update_id)+" Chat ID: "+str(message.chat_id)+" Message: "+message.text)
    
    else:
        print("Telegram sent invalid JSON")

def send_telegram_reply(reply,chat_id):
    requests.post("https://api.telegram.org/bot"+config.TELEGRAM_BOT_TOKEN+"/sendMessage",{'chat_id': chat_id, 'text' : reply})

parse_message()