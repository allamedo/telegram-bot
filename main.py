#Google Cloud Function
import requests
import config, firestore

class TelegramMessage():
    def __init__(self, telegram_request_message_json):
        self.text = telegram_request_message_json["message"]["text"]
        self.chat_id = telegram_request_message_json["message"]["chat"]["id"]
        self.username = telegram_request_message_json["message"]["from"]["username"]

    def url(self) -> str:
        return self.text[self.text.index("http"):].rstrip()
    def name(self) -> str:
        return self.text[:self.text.index("http")].rstrip()
    def store(self) -> str:
        if 'wallapop.' in self.url()[:30]:
            return 'wallapop'
        elif 'zalando.' in self.url()[:30]:
            return 'zalando'
        else:
            return ''

def parse_message(request):

    request_json = request.get_json()
    print(request_json)
    requests.post("http://punder.free.beeceptor.com/my/api/gcloud-functions",data=request_json)
    if request_json["update_id"] and request_json["message"]["chat"]["id"] and request_json["message"]["text"]:
        message = TelegramMessage(request_json)

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
        
        else:
            send_telegram_reply("¿Te has acrodado de enviarme el enlace de la busqueda?", message.chat_id)
        
        print("Telegram Bot parsed message. Update ID: "+str(request_json["update_id"])+" Chat ID: "+str(message.chat_id)+" Message: "+message.text)

        return "Telegram Bot parsed message. Update ID: "+str(request_json["update_id"])

def send_telegram_reply(reply,chat_id):
    requests.post("https://api.telegram.org/bot"+config.TELEGRAM_BOT_TOKEN+"/sendMessage",{'chat_id': chat_id, 'text' : reply})