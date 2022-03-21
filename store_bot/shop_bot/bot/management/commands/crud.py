import requests
from . import item as itemFormat

def createItem(chapter, response, item_data):                                           # create new user
    if(response == 'yes'):                                                              # this value just for "change profile" in bot.py
        r = requests.post(f"http://127.0.0.1:8000/api/{chapter}/", data=item_data)
        if(r.status_code == 400):
            return f"You have this item in {chapter} yet"
        return f"You have created item in {chapter}"
    else:
        return f"You cancelled the creation {chapter}"

def readItem(chapter, id):                                                               # get all or difinite item in the table

    r = requests.get(
        f"http://127.0.0.1:8000/api/{chapter}{id}/"                                      # request
    )
    data = r.json()                                                                      # creating json 
    amount_item = len(data)                                                              # amount of item. This is count form all items in a table

    if(id != ''):                                                                        # if user wants get all data then you need a wrapper
        amount_item = 1                                                                  # so that you can collect the data
        data = [data]

    message = []

    while amount_item:                                                                   # start with new items
        match chapter:
            case 'products':                                                        
                item = itemFormat.get_data(chapter, data[amount_item - 1])               # get data in array from table
                message.append(f"Product: {item[1]}\n\n"                                 # here the information is collected in a message
                               f"Description: {item[2]}\n\n"
                               f"Price: {item[3]}$\n\n")

            case 'users':
                item = itemFormat.get_data(chapter, data[amount_item - 1])
                message.append(f"ID: /{item[0]}\n"
                               f"userID: {item[1]}\n"
                               f"First Name: {item[2]}\n"
                               f"Last Name: {item[3]}\n"
                               f"Birth Day: {item[4]}\n"
                               f"Balance: {item[5]}$\n\n")

            case 'refs':
                item = itemFormat.get_data(chapter, data[amount_item - 1])
                message.append(f"Name: {item[0]}\n"
                               f"Description: {item[1]}\n"
                               f"Link: {item[2]}\n"
                               f"Created at: {item[3]}\n\n")

            case 'payments':
                item = itemFormat.get_data(chapter, data[amount_item - 1])
                message.append(f"payID: /{item[0]}\n"
                               f"User Name: {item[1]}\n"
                               f"Status: {item[2]}\n"
                               f"Products: {item[3]}\n"
                               f"Amount: {item[4]}$\n"
                               f"Date: {item[5]}\n\n")

            case _:
                "You don't have any items here\n you can go to /menu"

        amount_item -= 1

    return message


def updateItem(chapter, id, item_data):                                                         # update definite item
    try:
        r = requests.patch(f"http://127.0.0.1:8000/api/{chapter}/{id}/", data=item_data)
        return f"You have updated the data {id}"
    except:
        return "Try later..."

def deleteItem(chapter, id):                                                                    # delete definite item
    try:
        requests.delete(f"http://127.0.0.1:8000/api/{chapter}/{id}")
        return f"You deleted data {id}!"
    except:
        return "Try later..."