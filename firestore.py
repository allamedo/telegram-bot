import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

#Conexion a Google Cloud Firebase
cred = credentials.Certificate('googlecloud-credentials.json')
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()
searches_collection = db_firestore.collection(u'shop-scraping-searches')

def url_exists(url) -> bool: #Check if URL exists on Searches collection
    if searches_collection.where(u'url', u'==', url).get():
        return True
    else:
        return False

def url_insert(url,name,telegram_chat_id,store,username)  -> bool:
    searches_collection.document().set({'url': url, 'name': name, 'telegram_chat_id': telegram_chat_id, 'created': datetime.datetime.now(), 'store' : store, 'username' : username})
    return True

def url_delete(url) -> str:
    for search in searches_collection.where(u'url', u'==', url).stream():
        name = search.to_dict()["name"]
        search.reference.delete()
        return name
    return ''

def list_searches(telegram_chat_id) -> dict:
    urls = {}
    for search in searches_collection.where(u'telegram_chat_id', u'==', telegram_chat_id).stream():
        urls[search.to_dict()["url"]] = search.to_dict()["name"]
    return urls

if __name__ == "__main__": #Unit test
    #print(url_exists("https://es.wallapop.com/search?time_filter=lastWeek&keywords=thinkcentre%20ssd&max_sale_price=100&latitude=40.41956&longitude=-3.69196&filters_source=quick_filters"))

    #url_insert("test","test2",33)

    #url_delete("test")

    searches = list_searches(-353268130)
    for url in searches:
        print(searches[url]+" "+url)