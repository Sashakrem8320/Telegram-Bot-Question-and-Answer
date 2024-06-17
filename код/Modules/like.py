import telebot
from telebot import types
from Modules import module
from Modules import builder

bot = telebot.TeleBot(module.getToken())


def upd_like(call):
    spl = call.data.split()
    id = int(spl[2])
    if not id in builder.getTask()[int(spl[1])]["likes"]:
         builder.getTask()[int(spl[1])]["likes"].append(id)
    else:
         builder.getTask()[int(spl[1])]["likes"].remove(id)
    builder.save_task()
    from Modules.buttons import questionMarkup
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=questionMarkup(id,int(spl[1]),0))
    
def upd_alike(call):
    spl = call.data.split()
    id = int(spl[3])

    if not id in builder.getTask()[int(spl[1])]["answers"][int(spl[2])]["likes"]:
         builder.getTask()[int(spl[1])]["answers"][int(spl[2])]["likes"].append(id)
    else:
         builder.getTask()[int(spl[1])]["answers"][int(spl[2])]["likes"].remove(id)
    builder.save_task()
    from Modules.read import answerMarkup
    bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=answerMarkup(id,int(spl[1]),int(spl[2])))
    

def get_likes(id):
   task = builder.getTask()
   if task[id]:
       return len(task[id]["likes"])
   return 0

def get_alikes(id,id2):
   task = builder.getTask()
   if task[id] and task[id]["answers"][id2]:
       return len(task[id]["answers"][id2]["likes"])
   return 0
