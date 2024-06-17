import telebot
from Modules import module
from telebot import types
from Modules import builder
import json

from Handlers import workers
from Modules import sorting

bot = telebot.TeleBot(module.getToken())

def notify_all(message):
    pass

def confirmnotify(message):
    pass

def declineupload(call):
    id = int(call.data.split()[1])
    task = builder.getTask2()
    for c,i in enumerate(task):
            if i["id"]!=0 and i["uniqueid"]==id:
                bot.send_message(i["id"], text="Ваш запрос отклонил модератор:\n" + i["text"])
                task[c] = {"id":0}
                builder.save_task2()
                builder.new_task2()
                module.send_message(call.message.chat.id,"Отклонено.",types.ReplyKeyboardMarkup(resize_keyboard=True))
                bot.delete_message(call.message.chat.id,call.message.id)
                break

def confirmupload(call):
    id = int(call.data.split()[1])
    task = builder.getTask2()
    task1 = builder.getTask()
    found = None
    if not sorting.findbyunique(id,task): return
    for i in task1:
        if i["id"]!=0 and i["uniqueid"]==id:
            print('Already exists')
            found=task1.index(i)
            break
    for c,i in enumerate(task):
            if i["id"]!=0 and i["uniqueid"]==id:
                newid = None
                if found!=None:
                    task1[found]["text"]=i["text"]
                    task1[found]["attachments"]=i["attachments"].copy()

                    newid = task1[found]["number"]
                else:
                    task1.append(i)
                    newid = len(task1)
                    task1[newid-1]["number"]=newid
                    task1[newid-1]["gpt"] = 0
                print(task1, found)

                builder.save_task()
                builder.new_task()
                realid = i["id"]
                task[c] = {"id":0}

                builder.save_task2()
                builder.new_task2()
                board = types.InlineKeyboardMarkup()
                board.add(telebot.types.InlineKeyboardButton(text="Показать", callback_data="checkquestion " + str(newid-1) + " " + str(id)))
                chatid = call.message.chat.id
                bot.delete_message(call.message.chat.id,call.message.id)
                module.send_message(realid,"Ваш запрос открыт в доступ",board)

                module.send_message(call.message.chat.id,"Открыто в доступ.",board)
                break

def confirmansupload(call):
    id = int(call.data.split()[1])
    task = builder.getTask3()
    task1 = builder.getTask()
    found = None
    if not sorting.findbyunique(id,task): return
    belong = task[id]["belongs"]
    for i in task1[belong]["answers"]:
        if i["id"]!=0 and i["uniqueid"]==id:
            print('Already exists')
            found=task1[belong]["answers"].index(i)
            break
    for c,i in enumerate(task):
        if i["id"]!=0 and i["uniqueid"]==id:
                newid = None
                if found!=None:
                    task1[belong]["answers"][found]["text"]=i["text"]
                    task1[belong]["answers"][found]["attachments"]=i["attachments"].copy()
                    newid = found
                else:
                    task1[belong]["answers"].append(i)
                    newid = len(task1[belong]["answers"])
                #task1[belong]["answers"].append(i)
                #newid = len(task1[belong]["answers"])
                board = types.InlineKeyboardMarkup()
                Ans = telebot.types.InlineKeyboardButton(text="Показать ваш вопрос полностью",
                                                   callback_data="checkquestion " + str(belong) + " " + str(
                                                       task1[belong]["uniqueid"]))

                vpr = telebot.types.InlineKeyboardButton(text="Показать ответы на ваш вопрос",
                                                         callback_data="checkanswers " + str(belong) + " " + str(
                                                             task1[belong]["uniqueid"]))

                board.add(Ans)
                board.add(vpr)
                builder.save_task()
                builder.new_task()
                realid = i["id"]
                task[c] = {"id":0}
                builder.save_task3()
                builder.new_task3()
                chatid = call.message.chat.id
                bot.delete_message(call.message.chat.id,call.message.id)
                module.send_message(realid,"Ваш ответ открыт в доступ",board)
                module.send_message(task1[belong]["id"],"На ваш вопрос ответили",board)
                module.send_message(call.message.chat.id,"Открыто в доступ.",board)
                break


def declineansupload(call):
    id = int(call.data.split()[1])
    task = builder.getTask3()
    for c,i in enumerate(task):
            if i["id"]!=0 and i["uniqueid"]==id:
                bot.send_message(i["id"], text="Ваш ответ отклонили:\n" + i["text"])
                task[c] = {"id":0}
                builder.save_task3()
                builder.new_task3()
                module.send_message(call.message.chat.id,"Отклонено.",types.ReplyKeyboardMarkup(resize_keyboard=True))
                bot.delete_message(call.message.chat.id,call.message.id)
                break

def declineansupload2(call):
    from Handlers import Direct as f
    print("ok")
    module.send_message(call.message,
                       'Комментарий',
                       module.getMarkup(call.message))

    print("ok2")
    f.modstep(call.message.from_user.id, "blok", calln="calll")

def blok(message):
    from Handlers import Direct
    print("ok3")
    data = Direct.getStep(message.from_user.id)["callt"]["calll"]
    id = int(data.split()[1])
    task = builder.getTask3()
    for c, i in enumerate(task):
        if i["id"] != 0 and i["uniqueid"] == id:
            bot.send_message(i["id"], text="Ваш ответ отклонили:\n" + i["text"])
            task[c] = {"id": 0}
            builder.save_task3()
            builder.new_task3()
            module.send_message(message.chat.id, "Отклонено.", types.ReplyKeyboardMarkup(resize_keyboard=True))
            bot.delete_message(message.chat.id, message.id)
            break
