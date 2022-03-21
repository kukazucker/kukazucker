from . import crud
import requests
import datetime


def get_data(chapter, data):                                                                # get definitive item from table

    def getUserFL(id):                                                                      # get first and last name (Just for payments)
        r = requests.get(f"http://127.0.0.1:8000/api/users/{id}/")
        data = r.json()
        return f"{data['first_name']} {data['last_name']}"

    def get_dateDBY(data):                                                                  # converts to 1 Jan 1970
        return (datetime.datetime.strptime(data, "%Y-%m-%d")).strftime("%d %B %Y")
    
    def get_fullDate(data):                                                                 # converts to 1 Jan 1970 / mon 09:38:13
        return (datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ")).strftime("%d %B %Y / %a %H:%M:%S")

    answer = []
    params = []

    match chapter:                                                                           # data types in each table
        case 'products':       
            params = [
                      data["id"], 
                      data["name"], 
                      data["description"], 
                      data["price"], 
                     ]                         

        case 'users':
            params = [
                      data["id"], 
                      data["user_id"], 
                      data["first_name"], 
                      data["last_name"], 
                      get_dateDBY(data["birth_day"]), 
                      data["balance"]
                     ]

        case 'refs':
            params = [
                      data["name"],
                      data["description"],
                      data["link"], 
                      get_fullDate(data["date"])
                     ]
        
        case 'payments':
            params = [
                      data["id"], 
                      getUserFL(data["user"]), 
                      data["status"], 
                      data["products"], 
                      data["amount"], 
                      get_fullDate(data["date"])
                     ]

    for i in params:
        answer.append(i)

    return answer

def get_item(chapter, id):                                                                          # get definite item "Profile" in bot.py
    try:
        message = ""
        data = crud.readItem(f'{chapter}', f'{id}')
        message += data[0]
        return message
    except:
        chapter = chapter[0:-1]                                                                     # converts to singular
        return f"Sorry, i can't find this {chapter}"


def get_list(chapter, start, amount):                                                               # get difinite amount of elements in a table
    try:
        message = ""
        data = crud.readItem(f'{chapter}', '')                                                      # get all items 
        if(amount == -1):                                                                           # if user wants get all item
            amount = len(data)                                                                      # add all items in message
        while amount:                                                                               # or just 10, 20...
            message += data[start]
            start += 1
            amount -= 1
        return message
    except:                                                                                         # if 10 requested but 2 left
        return message                                                                              # get back what's left


def get_chatID():                                                                                   # get all chat_id's for sending new announcements and ref links
        all_chat_id = []
        r = requests.get(f"http://127.0.0.1:8000/api/users")
        data = r.json()
        amount = len(data)
        
        while amount:
            all_chat_id.append(data[amount-1]['user_id'])
            amount-=1
        return all_chat_id
        