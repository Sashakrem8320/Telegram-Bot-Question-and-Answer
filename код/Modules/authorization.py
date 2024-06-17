import telebot
from Modules import module
from telebot import types
import json

bot = telebot.TeleBot(module.getToken())
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

def authrefresh():
    global accs
    with open('accounts.json') as a:
        accs = json.load(a)
        return accs

def addacc():
    print('not implemented yet')

def updateauth():
    with open('accounts.json', 'w') as a:
        json.dump(accs, a)

def reqrank(id):
    for a in accs:
        if id in accs[a]["logged"]:
            return accs[a]["rank"]

def checklog(id):
     for a in accs:
        if id in accs[a]["logged"]:
            return True
     return False

def getaccname(id):
    for a in accs:
        if id in accs[a]["logged"]:
            return a
    return None

def logout(id,message):
    for a in accs:
        if id in accs[a]["logged"]:
            accs[a]["logged"].remove(id)
            module.send_message(message,'Вы вышли из аккаунта ' + a + "",module.getMarkup(message))
            updateauth()
            return
    module.send_message(message,'Вы не в аккаунте.',module.getMarkup(message))


authrefresh()
with open('vars.json') as a:
    if json.load(a)["logoff"]==1:
        print("Bot restart, logging out of all accounts.")
        for i in accs:
            accs[i]["logged"].clear()
        updateauth()
        print("Cleared")

def mainauth(message):
    if checklog(message.from_user.id): 
        module.send_message(message,'Вы уже в аккаунте.',module.getMarkup(message))
        return
    if module.getExcept(message.text):
        module.cancel(message)
        return
    spl = message.text.split()
    if len(spl)>2:
         module.send_message(message,'*Использован неправильный формат.*',module.getMarkup(message))
    elif (spl[0] in accs) and accs[spl[0]]["pass"]==spl[1]:
        accs[spl[0]]["logged"].append(message.from_user.id)
        module.send_message(message,'Вы успешно вошли в аккаунт!',module.getMarkup(message))
        updateauth()
        from Handlers.Direct import createblank
        createblank(message.from_user.id)
    else:
       module.send_message(message,'*Аккаунт не найден.*',module.getMarkup(message))