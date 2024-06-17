import telebot
from telebot import types
from Modules import builder
from Modules import module
from Modules import buttons
bot = telebot.TeleBot(module.getToken())

tags =  [
    "3D печать"
    "проектирование и прототепирование",
    "технологии производства",
    "лазерная резка",
    "автоматизация",
    "инженерная разработка",
    "современные материалы",
    "автоматизация процессов",
    "робототехника",
    "автоматическое управление процессами",
    "автомобилестроение",
    "Эллектроника"
]

def in_tag(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text = message.text.lower()
    task = builder.getTask()
    no =0
    for el in range(len(task)):
        for j in text.split():
            if str(" " + j + " ") in str(" " + task[el]["tag"] + " "):
                c = telebot.types.InlineKeyboardButton(text="Ответы", callback_data="checkanswers " + str(el))
                d = telebot.types.InlineKeyboardButton(text="Ответить", callback_data="doanswer " + str(el))
                board = types.InlineKeyboardMarkup()
                board.add(c, d)
                bot.send_message(message.chat.id, text=str(task[el]["text"]).format(message.from_user), reply_markup=board)
                no = 1

    if no == 0:
        module.send_message(message,'Ничего не найдено',module.getMarkup(message))


def tagfind(message):
    from Handlers.Direct import getStep
    if message.text=="Вернуться ко всем запросам.":
        getStep(message.from_user.id)["callt"]["tags"]=[]
        from Handlers.Direct import modstep
        modstep(message,"nilfun")
        bot.send_message(message.chat.id,"вернулись", reply_markup=module.getMarkup(message,listmenu=True))
    elif message.text=="Убрать последний тег.":
        removeltag(message)
    elif message.text=="Вызвать панель.":
        buttons.newpanel(message,getStep(message.from_user.id)["callt"]["start"])
    elif message.text in tags and not (message.text in getStep(message.from_user.id)["callt"]["tags"]) and "listpanel" in getStep(message.from_user.id)["callt"]:
        getStep(message.from_user.id)["callt"]["tags"].append(message.text)
        buttons.updatepanel(message.from_user.id,message.chat.id,getStep(message.from_user.id)["callt"]["start"])

def removeltag(message):
    from Handlers.Direct import getStep
    a = getStep(message.from_user.id)["callt"]["tags"]
    if len(a)>0:
        a.pop(len(a)-1)
        if getStep(message.from_user.id)["text"]!="ontag":
            buttons.updatepanel(message.from_user.id,message.chat.id,getStep(message.from_user.id)["callt"]["start"])
        else:
            bot.send_message(message.chat.id,"cur tags: " + str(getStep(message.from_user.id)["callt"]["tags"]))

def ontag(message):
    if message.text== "Продолжить.":
        from Modules.define import ask_user_to_insert_a_tag
        ask_user_to_insert_a_tag(message)
    elif message.text=="Убрать последний тег.":
        removeltag(message)
    elif message.text in tags:
        from Handlers import Direct
        if not ( message.text in Direct.getStep(message.from_user.id)["callt"]["tags"]):
            Direct.getStep(message.from_user.id)["callt"]["tags"].append(message.text)
            bot.send_message(message.chat.id,"Ваши тег:" + str(Direct.getStep(message.from_user.id)["callt"]["tags"]))
