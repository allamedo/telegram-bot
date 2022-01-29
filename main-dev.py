import main

class Request:

    def __init__(self):
        self.telegram_message_json = {"update_id": 171356370, 
                        "message": {
                            "message_id": 63051,
                            "from": {
                                "id": 10532106, "is_bot": False, "first_name": "Dum User", "username": "dummy", "language_code": "es"},
                                "chat": {
                                     "id": 10532102, "first_name": "Dum Chat", "username": "dummy", "type": "private"},
                                "date": 1641592478, "text": "Portatil i7 con SSD <300€ https://es.wallapop.com/app/search?category_ids=15000&keywords=ssd%20portatil%20i7&latitude=43.3627&longitude=-5.84768&order_by=newest&filters_source=search_box&max_sale_price=300&min_sale_price=20",
                                "entities": [{"offset": 26, "length": 197, "type": "url"}]}}
    
    def get_json(self):
        return self.telegram_message_json

#main.parse_message(Request())

print( main.TelegramMessage(Request().get_json()).username() )