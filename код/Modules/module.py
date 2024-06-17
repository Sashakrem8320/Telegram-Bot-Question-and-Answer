import json
import telebot
from telebot import types

excepts = [
    "Отмена",
    "Назад",
    "В меню",
]


def getToken():
    with open("vars.json","r") as file:
        return json.load(file)["token"]


bot = telebot.TeleBot(getToken())

shorts = {
    "video":bot.send_video,
    "photo":bot.send_photo,
    "audio":bot.send_audio,
    "voice":bot.send_voice,
}


def cancel(message,text="Отменено"):
    from Handlers import Direct as f
    f.createblank(message.from_user.id)
   # f.modstep(message,"nilfun")
   # f.modstep(message,"nilfun",type="file")
    return send_message(message,'Возвращаем вас',getMarkup(message))

def send_message(message,text,markup,parse="Markdown"):
    id = None
    if isinstance(message,int):
        id = message
    else:
        id = message.chat.id
    return bot.send_message(id,text,reply_markup=markup,parse_mode=parse)

def send_file(message,typ, id,reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True),caption=None):
    shorts[typ](message.chat.id,id,parse_mode="Markdown",caption=caption,reply_markup=reply_markup)

def getMarkup(message,cancel=False, acc=True, listmenu=False, choice=False, tagmenu=False, definetag=False):
    from Handlers import Direct as f
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if tagmenu:
        from Modules import tags
        if definetag:
            btn = types.KeyboardButton("Продолжить.")
            btn2 = types.KeyboardButton("Убрать последний тег.")
            markup.add(btn,btn2)
        else:
            btn = types.KeyboardButton("Вернуться ко всем запросам.")
            btn2 = types.KeyboardButton("Убрать последний тег.")
            btn3 = types.KeyboardButton("Вызвать панель.")
            markup.add(btn3,btn,btn2)
        tab = []
        for i in tags.tags:
            tab.append( types.KeyboardButton(i))
            if len(tab)==3:
                markup.add(*tab)
                tab.clear()
        if len(tab)>0:
            markup.add(*tab)
        return markup

    if choice:
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        return markup
    if listmenu:
        btn1 = types.KeyboardButton("Поиск по тегам")
        btn2 = types.KeyboardButton("В меню")
        btn3 = types.KeyboardButton("Вызвать панель")
        markup.add(btn1, btn2, btn3)
        return markup
    if cancel:
        btn = types.KeyboardButton("Назад")
        markup.add(btn)
        return markup
    btn1 = types.KeyboardButton("Задать вопрос")
    btn2 = types.KeyboardButton("Посмотреть вопрсы")
    btn3 = types.KeyboardButton("Посмотреть задержанные вопросы.")
    btn4 = types.KeyboardButton("Посмотреть задержанные ответы.")
    btn5 = types.KeyboardButton("Эмитировать вопрос пользователя.")
    markup.add(btn1,btn2)
    if acc==True:
        if f.s["checklog"](message.from_user.id):
            if f.s["reqrank"](message.from_user.id)>5:
                markup.add(btn3, btn4, btn5)
            btn = types.KeyboardButton("Выйти из аккаунта: " + f.s["getaccname"](message.from_user.id))
            markup.add(btn)
    return markup



def getExcept(text):
    for s in excepts:
        if text[0:len(s)]==s:
            return True
    return None
