import telebot
from telebot import types
from Modules import module
from Modules import builder
from Modules import sorting
from Modules.like import get_alikes
bot = telebot.TeleBot(module.getToken())


def answerMarkup(id,num,num2):

    from Modules.like import get_alikes
    board = types.InlineKeyboardMarkup()
    l = telebot.types.InlineKeyboardButton(text=str(get_alikes(num,num2)) + " 👍", callback_data="alike " + str(num) + " " + str(num2) + " " + str(id), row_width=4)


    board.add(l)
    return board

def openanswer(call,numb,i):
    task = builder.getTask()
    tab = task[numb]["answers"][i]
    board = answerMarkup(call.from_user.id,numb,i)
    if len(tab["attachments"])==1:
        board = answerMarkup(call.from_user.id,numb,i)
        tab = task[numb]["answers"][i]
        if len(tab["attachments"])==1:
            module.send_file(call.message,tab["attachments"][0]["typ"],tab["attachments"][0]["id"],reply_markup=board,caption="Ответ от пользователя: " + tab["name"] + "\n" + tab["text"])

    else:
        for c in tab["attachments"]:
            module.send_file(call.message,c["typ"],c["id"])
        a = False
        if a:
            if builder.getTask()[numb]["answers"][i]["id"] == call.message.chat.id:
                    print("jr")
                    x = telebot.types.InlineKeyboardButton(text="Изменить", callback_data="newanswer " + str(numb))
                    y = telebot.types.InlineKeyboardButton(text="Удалить", callback_data="delite " + str(numb))

                    board.add(x, y)
        mess = bot.send_message(call.message.chat.id, text="Ответ от пользователя: " + tab["name"] + "\n" + tab["text"], reply_markup=board)




def openquestion(call,numb):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num = 0
    spl = call.data.split()
    board = types.InlineKeyboardMarkup()
    temptab = []
    task = builder.getTask()

    if len(builder.getTask()[numb]["answers"]) != 0:
        for i in task[numb]["answers"]:
            temptab.append({"n":num,"likes":get_alikes(numb,num)})
            num+=1
        sorting.likesort(temptab)
        for i in temptab:


            openanswer(call,numb,i["n"])

    else:
        mess = bot.send_message(call.message.chat.id, text="Ответов нет".format(call.message.from_user), reply_markup=board)

