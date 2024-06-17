import telebot
from telebot import types
from Modules import module
from Modules import builder
bot = telebot.TeleBot(module.getToken())

def get_form(message,adjust=False):
    from Handlers import Direct
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text = None
    if adjust==False:
        text = message.text
    else:
        text = message.caption
    id = message.chat.id
    module.send_message(message,'*Отправьте файлы если вы хотите добавить их в запрос*\nВведите тег(и) в таком формате:\n"машина двигатель"',module.getMarkup(message, tagmenu=True,definetag=True)) 
    Direct.modvars(message.from_user.id,"tags",[])
    Direct.modstep(message,"ontag",calln="text",call=text)

def attachfile(message,typ,id):
    from Handlers import Direct
    step = Direct.getStep(message.from_user.id)
    step["callf"]["files"].append({"typ":typ,"id":id})
    bot.send_message(message.chat.id, text="Файл добавлен")


def ask_user_to_insert_a_tag(message):
    if module.getExcept(message.text): 
        module.cancel(message)
        return
    from Handlers.Direct import getStep
    builder.getTask2().append({"number":len(builder.getTask2()),"uniqueid":(len(builder.getTask())+len(builder.getTask2())), "likes":[], "attachments":getStep(message.from_user.id)["callf"]["files"], "text": getStep(message.from_user.id)["callt"]["text"], "name":message.from_user.first_name, "id": message.from_user.id, "tags":getStep(message.from_user.id)["callt"]["tags"] , "answers":[]})
    builder.save_task2()
    builder.new_task2()
    module.send_message(message,"Ваш запрос зарегистрирован.",module.getMarkup(message)) 
    from Handlers.Direct import createblank
    createblank(message.from_user.id)

