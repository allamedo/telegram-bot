#Google Cloud Function
import requests
import config, firestore

class TelegramMessage():
    def __init__(self, message_json):
        self.raw_message = message_json
        try:
            self.update_id = self.raw_message["update_id"]
            self.text = self.raw_message["message"]["text"]
            self.chat_id = self.raw_message["message"]["chat"]["id"]
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
    def username(self) -> str:
        try:
            return self.raw_message["message"]["from"]["username"]
        except:
            return ""

def parse_message(request):

    request_json = request.get_json()
    print(request_json)
    message = TelegramMessage(request_json)

    if message.valid:
        if len(message.store()) > 0 and len(message.url()) > 0:

            if firestore.url_exists(message.url()):
                deleted_name = firestore.url_delete(message.url())
                print("Deleted Search URL: "+message.url()+" Chat ID: "+str(message.chat_id)+" Name: "+message.name()+ " Username: "+message.username())
                send_telegram_reply("He borrado tu búsqueda: "+deleted_name, message.chat_id)

            else:
                firestore.url_insert(message.url(),message.name(),message.chat_id,message.store(), message.username())
                print("Inserted Search URL: "+message.url()+" Chat ID: "+str(message.chat_id)+" Name: "+message.name()+ " Username: "+message.username())
                send_telegram_reply("He creado tu búsqueda: "+message.name(), message.chat_id)

        elif len(message.store()) == 0 and len(message.url()) > 0:
            send_telegram_reply("No reconozco la tienda que me has enviado. Puede que aún no la haya implementado...", message.chat_id)
        
        print("Telegram Bot parsed message. Update ID: "+str(request_json["update_id"])+" Chat ID: "+str(message.chat_id)+" Message: "+message.text)
        return "Telegram Bot parsed message. Update ID: "+str(request_json["update_id"])
    
    else:
        return "Telegram sent invalid JSON"

def send_telegram_reply(reply,chat_id):
    requests.post("https://api.telegram.org/bot"+config.TELEGRAM_BOT_TOKEN+"/sendMessage",{'chat_id': chat_id, 'text' : reply})